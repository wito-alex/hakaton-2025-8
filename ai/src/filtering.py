import os
import numpy as np
import pydicom
from scipy.stats import pearsonr, wasserstein_distance
# import matplotlib.pyplot as plt
from data_processing import load_dicom_series


def read_dicom_series(folder, apply_rescale=True):
    files = [os.path.join(folder, f) for f in os.listdir(folder)]
    # print(files)
    slices = []
    for f in files:
        try:
            ds = pydicom.dcmread(f, force=True)
        except Exception:
            continue
        if not hasattr(ds, 'PixelData'):
            continue
        slices.append(ds)
    if not slices:
        raise RuntimeError(f"No DICOM images in {folder}")

    def keyfn(s):
        if hasattr(s, 'SliceLocation'):
            return float(s.SliceLocation)
        if hasattr(s, 'InstanceNumber'):
            return float(s.InstanceNumber)
        return 0.0
    slices.sort(key=keyfn)
    arr = np.stack([s.pixel_array for s in slices]).astype(np.float32)
    if apply_rescale:
        for i, s in enumerate(slices):
            slope = float(getattr(s, 'RescaleSlope', 1.0))
            intercept = float(getattr(s, 'RescaleIntercept', 0.0))
            if slope != 1.0 or intercept != 0.0:
                arr[i] = arr[i] * slope + intercept
    #################
    # air, water = find_air_water_peaks_clean(arr)
    # arr = shift_hu(arr, air, water, eps=10)
    #################
    return arr, slices

def histogram_mode(data, bins=2000, value_range=None):
    if value_range is None:
        hist, edges = np.histogram(data, bins=bins)
    else:
        hist, edges = np.histogram(data, bins=bins, range=value_range)
    idx = np.argmax(hist)
    return 0.5 * (edges[idx] + edges[idx+1])


def estimate_transform_modes(volume,
                             border_frac=0.06,
                             tissue_range=(-300, 300),
                             bins=2000,
                             expected_air=-1000.0,
                             expected_tissue=40.0):

    z, y, x = volume.shape
    bx = max(1, int(x * border_frac))
    by = max(1, int(y * border_frac))
    bz = max(1, int(z * border_frac))
    parts = []
    parts.append(volume[:, :by, :].ravel())
    parts.append(volume[:, -by:, :].ravel())
    parts.append(volume[:, :, :bx].ravel())
    parts.append(volume[:, :, -bx:].ravel())
    parts.append(volume[:bz, :, :].ravel())
    parts.append(volume[-bz:, :, :].ravel())
    border = np.concatenate(parts)
    border = border[np.isfinite(border)]
    air_raw = histogram_mode(border, bins=bins)


    cz0, cz1 = int(0.25*z), int(0.75*z)
    cy0, cy1 = int(0.25*y), int(0.75*y)
    cx0, cx1 = int(0.25*x), int(0.75*x)
    crop = volume[cz0:cz1, cy0:cy1, cx0:cx1].ravel()
    crop = crop[np.isfinite(crop)]
    mask = (crop >= tissue_range[0]) & (crop <= tissue_range[1])
    sel = crop[mask]
    if sel.size == 0:
        tissue_raw = float(np.median(crop))
    else:
        tissue_raw = histogram_mode(sel, bins=bins, value_range=tissue_range)

    if abs(tissue_raw - air_raw) < 1e-6:
        raise RuntimeError("Cannot estimate transform: air and tissue are equal")

    a = (expected_tissue - expected_air) / (tissue_raw - air_raw)
    b = expected_air - a * air_raw
    return float(a), float(b), float(air_raw), float(tissue_raw)

def estimate_transform_quantiles(volume,
                                 q_air=0.02, q_tissue=0.5,
                                 expected_air=-1000.0,
                                 expected_tissue=40.0):
    flat = volume.ravel()
    flat = flat[np.isfinite(flat)]
    if flat.size == 0:
        raise RuntimeError("Empty volume")
    air_raw = float(np.quantile(flat, q_air))
    tissue_raw = float(np.quantile(flat, q_tissue))
    if abs(tissue_raw - air_raw) < 1e-6:
        raise RuntimeError("Cannot estimate transform: air==tissue quantiles")
    a = (expected_tissue - expected_air) / (tissue_raw - air_raw)
    b = expected_air - a * air_raw
    return float(a), float(b), air_raw, tissue_raw


def body_mask_from_hu(volume_hu, threshold=-950):
    # mask for air extract
    mask = (volume_hu > threshold)
    if mask.sum() < 1000:
        mask = (volume_hu > (threshold - 200))
    return mask

def compute_hist(volume_hu, bins=np.arange(-1200,3000,10), mask=None):
    if mask is None:
        flat = volume_hu.ravel()
    else:
        flat = volume_hu[mask].ravel()
    flat = flat[np.isfinite(flat)]
    hist, edges = np.histogram(flat, bins=bins)
    s = hist.sum()
    if s > 0:
        hist = hist.astype(np.float64) / s
    else:
        hist = hist.astype(np.float64)
    centers = 0.5 * (edges[:-1] + edges[1:])
    return hist, centers

# Similarity
def js_divergence(p, q, eps=1e-12):
    p = np.asarray(p, dtype=np.float64) + eps
    q = np.asarray(q, dtype=np.float64) + eps
    p /= p.sum()
    q /= q.sum()
    m = 0.5*(p+q)
    kl = lambda a,b: np.sum(a * np.log(a/b))
    return 0.5*kl(p,m) + 0.5*kl(q,m)

def chi2_distance(p, q, eps=1e-12):
    p = np.asarray(p, dtype=np.float64)
    q = np.asarray(q, dtype=np.float64)
    denom = p + q + eps
    return 0.5 * np.sum(((p-q)**2) / denom)

def cosine_similarity(p, q, eps=1e-12):
    p = np.asarray(p, dtype=np.float64)
    q = np.asarray(q, dtype=np.float64)
    num = float(np.dot(p, q))
    den = np.linalg.norm(p) * np.linalg.norm(q) + eps
    return num / den

def compare_hists(h, ref_h, centers):
    # pearson on vectors
    try:
        pearson = float(pearsonr(h, ref_h)[0])
    except Exception:
        pearson = float('nan')
    cosine = cosine_similarity(h, ref_h)
    js = js_divergence(h, ref_h)
    chi2 = chi2_distance(h, ref_h)
    # wasserstein using centers and weights
    try:
        w = float(wasserstein_distance(centers, centers, u_weights=h, v_weights=ref_h))
    except Exception:
        w = float('nan')
    return {'pearson':pearson, 'cosine':cosine, 'js':js, 'chi2':chi2, 'wasserstein':w}


def build_reference_hist(folders, bins=np.arange(-1200,3000,10),
                         apply_transform_to_refs=True,
                         transform_method='modes'):
    hists = []
    centers = None
    for f in folders:
        try:
            # vol, slices = read_dicom_series(f, apply_rescale=True)
            vol, _, _ = load_dicom_series(f)
        except Exception as e:
            print("Warning, skipping", f, ":", e)
            continue

        if apply_transform_to_refs:
            try:
                if transform_method == 'modes':
                    a,b,_,_ = estimate_transform_modes(vol)
                else:
                    a,b,_,_ = estimate_transform_quantiles(vol)
                vol = vol * a + b
            except Exception as e:

                print("Warning transform for ref", f, "failed:", e)
        mask = body_mask_from_hu(vol)
        hist, centers = compute_hist(vol, bins=bins, mask=mask)
        if hist.sum() > 0:
            hists.append(hist)
    if not hists:
        raise RuntimeError("No valid reference histograms")
    hists = np.stack(hists)
    mean_hist = hists.mean(axis=0)
    mean_hist /= mean_hist.sum()
    return mean_hist, centers


def check_study_against_reference(folder, ref_hist, centers,
                                  bins=np.arange(-1200,3000,10),
                                  transform_try_order=('modes','quantiles'),
                                  verbose=True):
    # vol, slices = read_dicom_series(folder, apply_rescale=True)
    vol, _, _ = load_dicom_series(folder)
    # try transforms in order, but keep diagnostics
    transforms = []
    for method in transform_try_order:
        try:
            if method == 'modes':
                a,b,air_raw,tissue_raw = estimate_transform_modes(vol)
            else:
                a,b,air_raw,tissue_raw = estimate_transform_quantiles(vol)
            transforms.append({'method':method,'a':a,'b':b,'air_raw':air_raw,'tissue_raw':tissue_raw})
        except Exception as e:
            transforms.append({'method':method,'error':str(e)})

    chosen = None
    for t in transforms:
        if 'a' in t:
            chosen = t
            break
    if chosen is None:

        vol_hu = vol.copy()
        chosen = {'method':'none','a':1.0,'b':0.0}
    else:
        vol_hu = vol * chosen['a'] + chosen['b']

    mask = body_mask_from_hu(vol_hu)
    hist, centers_local = compute_hist(vol_hu, bins=bins, mask=mask)
    comp = compare_hists(hist, ref_hist, centers)

    flat = vol_hu[mask].ravel()
    N = flat.size if flat.size>0 else 1
    p_air = np.logical_and(flat >= -2000, flat <= -300).sum() / N
    p_soft = np.logical_and(flat > -300, flat <= 200).sum() / N
    p_bone = (flat > 200).sum() / N

    issues = []

    if comp['pearson'] != comp['pearson'] or comp['pearson'] < 0.50:
        issues.append(f"low_pearson_{comp['pearson']:.3f}")
    if comp['js'] > 0.25:
        issues.append(f"high_js_{comp['js']:.3f}")
    if p_air < 0.02:
        issues.append(f"low_air_frac_{p_air:.3f}")
    if p_soft < 0.03:
        issues.append(f"low_soft_frac_{p_soft:.3f}")

    verdict = "OK" if not issues else "WARN"

    result = {
        'verdict':verdict,
        'issues':issues,
        'comparison':comp,
        'hist':hist,
        'centers':centers,
        'mask_fraction': mask.sum() / vol_hu.size,
        'proportions':{'air':p_air,'soft':p_soft,'bone':p_bone},
        'transform_chosen': chosen,
        'all_transform_attempts': transforms
    }

    if verbose:
        print("Verdict:", result['verdict'])
        print("Comparison metrics:", result['comparison'])
        print("Mask fraction:", result['mask_fraction'])
        print("Proportions (air/soft/bone):", result['proportions'])
        print("Transform chosen:", result['transform_chosen'])
        if issues:
            print("Issues:", issues)

        # # plot
        # plt.figure(figsize=(8,4))
        # plt.plot(centers, ref_hist, label='reference')
        # plt.plot(centers, hist, label='test')
        # plt.xlabel('HU'); plt.ylabel('probability'); plt.legend()
        # plt.title(f"pearson={comp['pearson']:.3f}, js={comp['js']:.3f}, wasserstein={comp['wasserstein']:.2f}")
        # plt.show()

    return result


def evaluate_reference_consistency(ref_folders, bins=np.arange(-1200,3000,10),
                                   apply_transform_to_refs=True,
                                   transform_method='modes'):

    per_hist = []
    centers = None
    good_folders = []
    for f in ref_folders:
        try:
            # vol, _ = read_dicom_series(f, apply_rescale=True)
            vol, _ , _ = load_dicom_series(f)
            if apply_transform_to_refs:
                try:
                    if transform_method=='modes':
                        a,b,_,_ = estimate_transform_modes(vol)
                    else:
                        a,b,_,_ = estimate_transform_quantiles(vol)
                    vol = vol * a + b
                except Exception as e:
                    print("Ref transform failed for", f, ":", e)
            mask = body_mask_from_hu(vol)
            hist, centers = compute_hist(vol, bins=bins, mask=mask)
            if hist.sum() > 0:
                per_hist.append(hist)
                good_folders.append(f)
        except Exception as e:
            print("Skipping ref", f, ":", e)
    if not per_hist:
        raise RuntimeError("No valid refs")
    per_hist = np.stack(per_hist)
    # compute leave-one-out similarities
    pears = []
    js = []
    cosines = []
    for i in range(len(per_hist)):
        others = np.delete(per_hist, i, axis=0)
        mean_others = others.mean(axis=0)
        mean_others /= mean_others.sum()
        comp = compare_hists(per_hist[i], mean_others, centers)
        pears.append(comp['pearson'])
        js.append(comp['js'])
        cosines.append(comp['cosine'])
    pears = np.array(pears)
    js = np.array(js)
    cosines = np.array(cosines)
    print("Reference consistency (leave-one-out):")
    print("Pearson median {:.3f}, 5% {:.3f}, 95% {:.3f}".format(np.median(pears), np.percentile(pears,5), np.percentile(pears,95)))
    print("JS median {:.3f}, 5% {:.3f}, 95% {:.3f}".format(np.median(js), np.percentile(js,5), np.percentile(js,95)))
    print("Cosine median {:.3f}, 5% {:.3f}, 95% {:.3f}".format(np.median(cosines), np.percentile(cosines,5), np.percentile(cosines,95)))
    return {'pearson':pears, 'js':js, 'cosine':cosines, 'centers':centers, 'good_folders':good_folders}

import os
import numpy as np
import pydicom
import cv2
import pandas as pd
import uuid
from pydicom.errors import InvalidDicomError 


def load_dicom_series(path):
    """
    Load CT image and return numpy pixel array with shape (num_slices, H, W).

    path: path to folder with input DICOM file or files.
    """
    if os.path.isdir(path):
        files = os.listdir(path)
        if len(files) > 1:
            dicom_files = [os.path.join(path, f) for f in os.listdir(path)] # if f.endswith(".dcm")]
            datasets = [pydicom.dcmread(f) for f in dicom_files]

            try:
                datasets.sort(key=lambda d: int(d.InstanceNumber))
            except AttributeError:
                datasets.sort(key=lambda d: float(d.ImagePositionPatient[2]))

            volume = np.stack([ds.pixel_array for ds in datasets])
            ds = datasets[1]
            study_uid = ds.StudyInstanceUID
            series_uid = ds.SeriesInstanceUID

            return volume.astype(np.int16), study_uid, series_uid
        elif len(files) == 1:
            # elif os.path.isfile(path):
            ds = pydicom.dcmread(os.path.join(path, files[0]))

            study_uid = ds.StudyInstanceUID
            series_uid = ds.SeriesInstanceUID

            if hasattr(ds, "NumberOfFrames") and ds.NumberOfFrames > 1:
                # multiframe dicom
                volume = ds.pixel_array
                return volume.astype(np.int16), study_uid, series_uid
            else:
                # one slice
                return ds.pixel_array[np.newaxis, ...].astype(np.int16), study_uid, series_uid

    else:
        raise ValueError(f"Path {path} does not exist")


import os
import numpy as np
import pydicom

def load_dicom_series(path):
    """
    Load CT image and return numpy pixel array with shape (num_slices, H, W).

    path: path to folder with input DICOM file or files.
    """
    if os.path.isdir(path):
        files = os.listdir(path)
        if len(files) > 1:
            dicom_files = [os.path.join(path, f) for f in os.listdir(path)] # if f.endswith(".dcm")]
            datasets = []
            for f in dicom_files:
                if not f.split('/')[-1].startswith('.'):
                    try:
                        datasets.append(pydicom.dcmread(f))
                    except InvalidDicomError:
                        print(f'Cannot read file {f}: File is missing DICOM File Meta Information header or the DICM prefix is missing from the header. ')

            try:
                datasets.sort(key=lambda d: int(d.InstanceNumber))
            except AttributeError:
                datasets.sort(key=lambda d: float(d.ImagePositionPatient[2]))

            volume = np.stack([ds.pixel_array for ds in datasets])
            ds = datasets[1]
            try:
                study_uid = ds.StudyInstanceUID
            except AttributeError:
                # print('FileDataset object has no attribute StudyInstanceUID')
                study_uid = None
            try:
                series_uid = ds.SeriesInstanceUID
            except AttributeError:
                # print('FileDataset object has no attribute SeriesInstanceUID')
                series_uid = None

            return volume.astype(np.int16), study_uid, series_uid
        elif len(files) == 1:
            # elif os.path.isfile(path):
            ds = pydicom.dcmread(os.path.join(path, files[0]))

            study_uid = ds.StudyInstanceUID
            series_uid = ds.SeriesInstanceUID

            if hasattr(ds, "NumberOfFrames") and ds.NumberOfFrames > 1:
                # multiframe dicom
                volume = ds.pixel_array
                return volume.astype(np.int16), study_uid, series_uid
            else:
                # one slice
                return ds.pixel_array[np.newaxis, ...].astype(np.int16), study_uid, series_uid

    else:
        raise ValueError(f"Path {path} does not exist")


def find_air_water_peaks_clean(pixels,
                               bin_width=4,
                               reserved_values=(-2048, 0), 
                               min_fraction=0.001,
                               target_distance=1000,
                               tolerance=200,
                               verbose=False):
    """
    Find air peak and water peak
    """
    pixels = np.asarray(pixels).ravel()

    mask = np.ones_like(pixels, dtype=bool)
    for rv in reserved_values:
        mask &= pixels != rv
    valid = pixels[mask]
    if valid.size == 0:
        raise ValueError("No valid pixels")

    vmin, vmax = np.percentile(valid, [0.5, 99.5]) 
    bins = int((vmax - vmin) / bin_width)
    hist, edges = np.histogram(valid, bins=bins, range=(vmin, vmax))
    centers = (edges[:-1] + edges[1:]) / 2

    sorted_idx = np.argsort(hist)[::-1]
    candidates = [(centers[idx], hist[idx]) for idx in sorted_idx if hist[idx] > min_fraction * hist.max()]

    best_pair = None
    best_diff = float("inf")
    for i in range(len(candidates)):
        for j in range(i + 1, len(candidates)):
            d = abs(candidates[i][0] - candidates[j][0])
            diff = abs(d - target_distance)
            if diff < best_diff and (target_distance - tolerance) <= d <= (target_distance + tolerance):
                best_diff = diff
                best_pair = (candidates[i][0], candidates[j][0])

    if best_pair is not None:
        air, water = sorted(best_pair)
        if verbose:
            print(f"Pair chosen by distance≈{target_distance}: {air}, {water}")
    elif len(candidates) >= 2:
        air, water = sorted([candidates[0][0], candidates[1][0]])
        if verbose:
            print(f"Fallback: top2 peaks {air}, {water}")
    else:
        air, water = np.percentile(valid, [1, 90])
        if verbose:
            print(f"Percentile fallback: {air}, {water}")

    return float(air), float(water)


def shift_hu(pixels, air, water, water_point=0, eps=30):
    pixels = np.copy(pixels)
    if not -eps <= water <= eps:
        pixels = pixels - water
    return pixels


def clip_hu(pixels, hu_min=-1024, hu_max=3000):
    pixels = np.copy(pixels)
    pixels = np.clip(pixels, hu_min, hu_max)
    return pixels


def normalize_hu_minmax(pixels, hu_min=-1024, hu_max=3000, out_range=(0.0, 1.0)):
    min_out, max_out = out_range
    norm = (pixels - hu_min) / (hu_max - hu_min)
    norm = norm * (max_out - min_out) + min_out
    return norm

def normalize_hu_zscore(pixels, mean=None, std=None, clip_percentiles=(0.5, 99.5)):
    """
    Z-score normalization HU: (x - mean) / std.
    If no mean/std provided, they are calculated by data.
    """
    pixels = np.asarray(pixels, dtype=np.float32).ravel()
    
    vmin, vmax = np.percentile(pixels, clip_percentiles)
    pixels_clipped = np.clip(pixels, vmin, vmax)
    
    if mean is None:
        mean = pixels_clipped.mean()
    if std is None:
        std = pixels_clipped.std()
        if std == 0:
            std = 1.0  
    
    norm = (pixels_clipped - mean) / std
    return norm


# def preprocess_dicom(path: str):
#     pixels, study_uid, series_uid = load_dicom_series(path)
#     air, water = find_air_water_peaks_clean(pixels)
#     hu_pixels = shift_hu(pixels, air, water)
#     hu_pixels = clip_hu(hu_pixels, hu_min=-1024, hu_max=3000)
#     return hu_pixels


def preprocess_ct(path: str, hu_min=-1024, hu_max=3000, eps=100):
    pixels, study_uid, series_uid = load_dicom_series(path)
    hu_pixels = pixels
    air, water = find_air_water_peaks_clean(pixels)
    hu_pixels = shift_hu(pixels, air, water, eps=eps)
    hu_pixels = clip_hu(hu_pixels, hu_min=hu_min, hu_max=hu_max)
    normalized_pixels = normalize_hu_minmax(hu_pixels)
    return normalized_pixels, study_uid, series_uid
    

def load_dicom_and_split2npy(path: str, output_folder: str, df_folder: str, df_name: str, label: int):
    os.makedirs(output_folder, exist_ok=True)
    os.makedirs(df_folder, exist_ok=True)
    data = {
        'dicom_path': [],
        'slice_num': [],
        'study_uid': [],
        'series_uid': [],
        'file_uid': [],
        'filepath': [],
        'label': []
    }
    pixel_array, study_uid, series_uid = preprocess_ct(path)
    patient_id = os.path.splitext(os.path.basename(path))[0]

    for i in range(pixel_array.shape[0]):
        image_uuid = str(uuid.uuid4())
        slice = pixel_array[i]
        
        out_path = os.path.join(output_folder, f"{patient_id}_slice_{i:03d}_{image_uuid}.npy")
        np.save(out_path, slice)
        data['dicom_path'].append(path)
        data['slice_num'].append(i)
        data['study_uid'].append(study_uid)
        data['series_uid'].append(series_uid)
        data['file_uid'].append(image_uuid)
        data['filepath'].append(os.path.join(output_folder, f"{patient_id}_slice_{i:03d}_{image_uuid}.npy"))
        data['label'].append(label)
    
    temp_df = pd.DataFrame(data)
    if os.path.exists(os.path.join(df_folder, df_name + '.csv')):
        df = pd.read_csv(os.path.join(df_folder, df_name + '.csv'))
        df = pd.concat([df, temp_df], ignore_index=True)
    else:
        df = temp_df
    df.to_csv(os.path.join(df_folder, df_name + '.csv'), index=False)


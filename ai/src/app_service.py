import torch
import numpy as np
from src.model import AE
from src.data_processing import preprocess_ct
from time import time
from src.transforms import get_transform
from src.criterion import AELoss
import uuid
import json



INPUT_SIZE = 512
WEIGHTS_PATH = 'weights/model_1.3.4_10.pth'

transform = get_transform(target_size=INPUT_SIZE)
criterion = AELoss(anomaly_score=True, keepdim=False)

model = AE(input_size=INPUT_SIZE)
weights = torch.load(WEIGHTS_PATH, weights_only=True)
model.load_state_dict(weights)
model.eval()
print('Model weights loaded')



def predict_sample(ct, model, criterion, agg='mean'):
    scores = []
    for sl in range(len(ct)):
        ct_tensor = transform(ct[sl].astype(np.float32))
        result = model(ct_tensor.unsqueeze(0))
        score = criterion(ct_tensor, result)
        scores.append(score)
    scores = torch.stack(scores)
    if agg == 'mean':
        res_score = scores.mean()
    elif agg == 'max':
        res_score = scores.max()
    else:
        raise NotImplementedError('Aggregation type is wronge')
    del scores
    return res_score



class AppService:
    """
    Detector plus OCR service.

    Returns response dictionary for FastAPI.
    """
    def __init__(self, model=model):
        self._model = model

    def predict(self, path: str):
        current_status_id = uuid.uuid4()
        with open('status.json', 'w') as f:
            data = {
                'current_status_id': current_status_id,
                'path': path
            }
            json.dump(data, f)
        start = time()
        ct, study_uid, series_uid = preprocess_ct(path)
        res = predict_sample(ct, model, criterion=criterion, agg='mean')
        proba = float(res.detach().numpy())
        cls = round(proba)
        end = time()
        time_of_processing = end - start
        result = {
            'path_to_study': path,
            'study_uid': study_uid,
            'series_uid': [series_uid],
            'probability_of_pathology': round(proba, 2),
            'pathology': cls,
            'processing_status': 'Success',
            'time_of_processing': round(time_of_processing, 2),
            'most_dangerous_pathology_type': None,
            'pathology_localization': None
        }
        return result

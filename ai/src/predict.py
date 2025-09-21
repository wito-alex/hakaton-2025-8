import torch
import numpy as np
from ai.src.model import DummyModel
from ai.src.data_processing import preprocess_ct
from time import time

model = DummyModel()


def predict(path: str):
    start = time()
    normalized_pixels, study_uid, series_uid = preprocess_ct(path)
    predict, proba = model(normalized_pixels)
    predict, proba = predict.int().item(), proba
    class_proba = proba[predict].item()
    end = time()
    time_of_processing = end - start
    
    result = {
        'path_to_study': path,
        'study_uid': study_uid,
        'series_uid': series_uid,
        'probability_of_pathology': round(class_proba, 2),
        'pathology': predict,
        'processing_status': 'Success',
        'time_of_processing': round(time_of_processing, 2),
        'most_dangerous_pathology_type': 'cancer',
        'pathology_localization': None
    }
    return result


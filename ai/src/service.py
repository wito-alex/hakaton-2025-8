import numpy as np
from src.app_service import AppService
from src.routers import router
import json


service = AppService()


@router.post('/predict')
def predict(path: str):
    result = service.predict(path)
    return result


@router.get('/status')
def get_status():
    with open('status.json', 'r') as f:
        status = json.load(f)
    return status
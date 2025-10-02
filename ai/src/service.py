import numpy as np
from ai.src.app_service import AppService
from ai.src.routers import router
import json


service = AppService()


@router.post('/predict')
def predict(
        path: str,
        service: AppService = service):
    result = service.predict(path)
    return result


@router.get('/status')
def get_status():
    with open('status.json', 'r') as f:
        status = json.load(f)
    return status
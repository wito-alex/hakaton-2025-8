import numpy as np
from ai.src.app_service import AppService
from ai.src.routers import router
import json
import os
import subprocess


def unzip_and_remove(zip_path):
    folder = os.path.splitext(zip_path)[0]

    os.makedirs(folder, exist_ok=True)

    subprocess.run(["unzip", "-q", zip_path, "-d", folder], check=True)
    os.remove(zip_path)
    return folder


service = AppService()


@router.post('/predict')
def predict(
        path: str,
        service: AppService = service):
    path = unzip_and_remove(path)
    result = service.predict(path)
    return result


@router.get('/status')
def get_status():
    with open('status.json', 'r') as f:
        status = json.load(f)
    return status
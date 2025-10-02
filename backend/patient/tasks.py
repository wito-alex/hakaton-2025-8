import time
import requests
from pathlib import Path

from django.core.files import File

from src.celery import app
from .models import Scan, DicomInfo, Slice

AI_SERVICE_URL = "http://hk_ai:8000/api/predict"


@app.task
def process_scan_with_ai(scan_id):
    """
    Celery-задача для обработки скана с помощью AI.
    """
    try:
        scan = Scan.objects.get(id=scan_id)
        if not scan.path_to_study:
            raise ValueError("Scan has no file to process.")

        scan.work_ai_status = Scan.WorkType.in_processing
        scan.save()

        # --- Вызов реального AI-сервиса ---
        print(f"Sending file path to AI service: {scan.path_to_study.path}")
        response = requests.post(AI_SERVICE_URL, params={"path": scan.path_to_study.path})
        response.raise_for_status()  # Вызовет исключение для кодов 4xx/5xx
        ai_response = response.json()
        print("AI processing finished. Parsing results...")
        # ---

        # Обновляем основной скан данными из ответа AI
        scan.study_uid = ai_response.get("study_uid")
        scan.series_uid = ai_response.get("series_uid", [None])[0]
        scan.probability_of_pathology = ai_response.get("probability_of_pathology")
        scan.pathology = ai_response.get("pathology")
        scan.processing_status = ai_response.get("processing_status")
        scan.time_of_processing = ai_response.get("time_of_processing")
        scan.work_ai_status = Scan.WorkType.worked_out
        scan.save()

        # В вашем примере ответа от AI нет информации по срезам, поэтому
        # этот блок пока не будет создавать объекты Slice.
        # Если AI будет возвращать срезы, логику нужно будет добавить сюда.

        print(f"Successfully processed and saved AI data for scan_id: {scan_id}")

    except Scan.DoesNotExist:
        print(f"Scan with id={scan_id} not found.")
    except Exception as e:
        print(f"Error processing scan_id: {scan_id}. Error: {e}")
        try:
            scan = Scan.objects.get(id=scan_id)
            scan.work_ai_status = Scan.WorkType.in_work # Возвращаем в исходное для повторной попытки
            scan.processing_status = Scan.ProcessingStatusType.FAILURE
            scan.save()
        except Scan.DoesNotExist:
            pass # нечего обновлять, если скан не найден


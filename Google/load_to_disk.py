from __future__ import print_function

from google.oauth2 import service_account

from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

from config import CONFIG

import os
import time



# Если меняете набор прав — удалите файл token.json, чтобы заново пройти авторизацию
SCOPES = ['https://www.googleapis.com/auth/drive']

def _get_drive_service():
    creds = service_account.Credentials.from_service_account_file(
        'Google\\credentials.json',
        scopes=SCOPES
    )
    service = build('drive', 'v3', credentials=creds)
    return service


def _upload_file(local_path: str, drive_name: str, mime_type: str = 'application/octet-stream'):
    """
    Загружает файл в корневую папку Google Drive.

    :param local_path: путь к файлу на локальной машине
    :param drive_name: имя файла в Drive
    :param mime_type: MIME-тип загружаемого файла
    """
    drive_service = _get_drive_service()

    file_metadata = {
        'name': drive_name,
        # можно указать 'parents': ['<folder_id>'] для загрузки в конкретную папку
    }
    media = MediaFileUpload(local_path, resumable=True)

    created_file = (
        drive_service.files()
        .create(body=file_metadata, media_body=media, fields='id')
        .execute()
    )
    print(f"Uploaded file {created_file.get('name')} (ID: {created_file.get('id')})")
    return created_file



def load_to_disk_module():
    file_path = CONFIG['PATH_TO_HAND_HISTORY']
    while True:
        files = os.listdir(file_path)
        
        for file in files:
            if 'COMPLETE' in file:
                _upload_file(
                    file_path + file,
                    file
                )
            os.remove(file_path + file)
        
        time.sleep(5)



from __future__ import print_function

from google.oauth2 import service_account

from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

from config import CONFIG

import os
import time
import traceback

# Если меняете набор прав — удалите файл token.json, чтобы заново пройти авторизацию
SCOPES = ['https://www.googleapis.com/auth/drive']

print("Google Drive модуль инициализирован")
print(f"Путь к истории рук: {CONFIG['PATH_TO_HAND_HISTORY']}")

def _get_drive_service():
    try:
        print("Получение сервиса Google Drive")
        creds = service_account.Credentials.from_service_account_file(
            'Google\\credentials.json',
            scopes=SCOPES
        )
        service = build('drive', 'v3', credentials=creds)
        print("Сервис Google Drive получен успешно")
        return service
    except Exception as e:
        print(f"Ошибка при получении сервиса Google Drive: {e}")
        raise

def _upload_file(local_path: str, drive_name: str, mime_type: str = 'application/octet-stream'):
    """
    Загружает файл в корневую папку Google Drive.

    :param local_path: путь к файлу на локальной машине
    :param drive_name: имя файла в Drive
    :param mime_type: MIME-тип загружаемого файла
    """
    try:
        print(f"Начинаем загрузку файла: {local_path} -> {drive_name}")
        
        if not os.path.exists(local_path):
            print(f"Файл не найден: {local_path}")
            return None
            
        file_size = os.path.getsize(local_path)
        print(f"Размер файла: {file_size} байт")
        
        drive_service = _get_drive_service()

        file_metadata = {
            'name': drive_name,
            # можно указать 'parents': ['<folder_id>'] для загрузки в конкретную папку
        }
        media = MediaFileUpload(local_path, resumable=True)
        print("Медиа объект создан")

        print(f"Загружаем файл в Google Drive: {drive_name}")
        created_file = (
            drive_service.files()
            .create(body=file_metadata, media_body=media, fields='id')
            .execute()
        )
        
        file_id = created_file.get('id')
        print(f"Файл {drive_name} успешно загружен (ID: {file_id})")
        return created_file
        
    except Exception as e:
        print(f"Ошибка при загрузке файла {local_path}: {e}")
        print(f"Traceback: {traceback.format_exc()}")
        return None

def load_to_disk_module():
    print("Запуск модуля загрузки в Google Drive")
    file_path = CONFIG['PATH_TO_HAND_HISTORY']
    twelve_hours_seconds = CONFIG['files_wait_time'] * 60 * 60

    print(f"Мониторинг директории: {file_path}")

    while True:
        try:
            print("Начинаем цикл проверки файлов для загрузки")

            if not os.path.exists(file_path):
                print(f"Директория не существует: {file_path}")
                time.sleep(5)
                continue

            files = os.listdir(file_path)
            print(f"Найдено файлов в директории: {len(files)}")

            if not files:
                print("Файлы для обработки не найдены, ожидание 5 секунд")
                time.sleep(5)
                continue

            now = time.time()
            # Файлы с 'COMPLETE' в имени
            complete_files = [f for f in files if 'COMPLETE' in f]

            # Файлы старше 12 часов (неважно, есть ли 'COMPLETE' в имени)
            old_files = []
            for f in files:
                try:
                    full_path = os.path.join(file_path, f)
                    if not os.path.isfile(full_path):
                        continue
                    mtime = os.path.getmtime(full_path)
                    if now - mtime > twelve_hours_seconds:
                        old_files.append(f)
                except Exception as e:
                    print(f"Не удалось получить время изменения файла {f}: {e}")

            # Объединяем списки, избегая дубликатов
            files_to_upload = list(set(complete_files + old_files))
            print(f"Найдено файлов для загрузки: {len(files_to_upload)}")

            for file in files_to_upload:
                try:
                    full_path = os.path.join(file_path, file)
                    print(f"Обрабатываем файл: {file}")

                    # Загружаем файл в Google Drive
                    result = _upload_file(full_path, file)

                    if result:
                        # Удаляем файл после успешной загрузки
                        print(f"Удаляем локальный файл: {file}")
                        os.remove(full_path)
                        print(f"Файл {file} удален успешно")
                    else:
                        print(f"Файл {file} не был загружен, оставляем для повторной попытки")

                except Exception as e:
                    print(f"Ошибка при обработке файла {file}: {e}")
                    print(f"Traceback: {traceback.format_exc()}")
                    continue

            print("Цикл обработки файлов завершен, ожидание 5 секунд")
            time.sleep(5)

        except Exception as e:
            print(f"Критическая ошибка в основном цикле загрузки: {e}")
            print(f"Traceback: {traceback.format_exc()}")
            print("Ожидание 30 секунд перед повторной попыткой")
            time.sleep(30)



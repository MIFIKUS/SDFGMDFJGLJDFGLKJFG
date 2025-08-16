from __future__ import print_function

from google.oauth2 import service_account

from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

from config import CONFIG
from logger import get_logger

import os
import time
import traceback

# Получаем логгер для Google модуля
logger = get_logger('GoogleDrive')

# Если меняете набор прав — удалите файл token.json, чтобы заново пройти авторизацию
SCOPES = ['https://www.googleapis.com/auth/drive']

logger.info("Google Drive модуль инициализирован")
logger.info(f"Путь к истории рук: {CONFIG['PATH_TO_HAND_HISTORY']}")

def _get_drive_service():
    try:
        logger.debug("Получение сервиса Google Drive")
        creds = service_account.Credentials.from_service_account_file(
            'Google\\credentials.json',
            scopes=SCOPES
        )
        service = build('drive', 'v3', credentials=creds)
        logger.debug("Сервис Google Drive получен успешно")
        return service
    except Exception as e:
        logger.error(f"Ошибка при получении сервиса Google Drive: {e}")
        raise

def _upload_file(local_path: str, drive_name: str, mime_type: str = 'application/octet-stream'):
    """
    Загружает файл в корневую папку Google Drive.

    :param local_path: путь к файлу на локальной машине
    :param drive_name: имя файла в Drive
    :param mime_type: MIME-тип загружаемого файла
    """
    try:
        logger.info(f"Начинаем загрузку файла: {local_path} -> {drive_name}")
        
        if not os.path.exists(local_path):
            logger.error(f"Файл не найден: {local_path}")
            return None
            
        file_size = os.path.getsize(local_path)
        logger.debug(f"Размер файла: {file_size} байт")
        
        drive_service = _get_drive_service()

        file_metadata = {
            'name': drive_name,
            # можно указать 'parents': ['<folder_id>'] для загрузки в конкретную папку
        }
        media = MediaFileUpload(local_path, resumable=True)
        logger.debug("Медиа объект создан")

        logger.info(f"Загружаем файл в Google Drive: {drive_name}")
        created_file = (
            drive_service.files()
            .create(body=file_metadata, media_body=media, fields='id')
            .execute()
        )
        
        file_id = created_file.get('id')
        logger.info(f"Файл {drive_name} успешно загружен (ID: {file_id})")
        return created_file
        
    except Exception as e:
        logger.error(f"Ошибка при загрузке файла {local_path}: {e}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        return None

def load_to_disk_module():
    logger.info("Запуск модуля загрузки в Google Drive")
    file_path = CONFIG['PATH_TO_HAND_HISTORY']
    
    logger.info(f"Мониторинг директории: {file_path}")
    
    while True:
        try:
            logger.debug("Начинаем цикл проверки файлов для загрузки")
            
            if not os.path.exists(file_path):
                logger.warning(f"Директория не существует: {file_path}")
                time.sleep(5)
                continue
                
            files = os.listdir(file_path)
            logger.debug(f"Найдено файлов в директории: {len(files)}")
            
            if not files:
                logger.debug("Файлы для обработки не найдены, ожидание 5 секунд")
                time.sleep(5)
                continue
            
            complete_files = [f for f in files if 'COMPLETE' in f]
            logger.info(f"Найдено файлов для загрузки: {len(complete_files)}")
            
            for file in complete_files:
                try:
                    full_path = os.path.join(file_path, file)
                    logger.info(f"Обрабатываем файл: {file}")
                    
                    # Загружаем файл в Google Drive
                    result = _upload_file(full_path, file)
                    
                    if result:
                        # Удаляем файл после успешной загрузки
                        logger.info(f"Удаляем локальный файл: {file}")
                        os.remove(full_path)
                        logger.info(f"Файл {file} удален успешно")
                    else:
                        logger.warning(f"Файл {file} не был загружен, оставляем для повторной попытки")
                        
                except Exception as e:
                    logger.error(f"Ошибка при обработке файла {file}: {e}")
                    logger.error(f"Traceback: {traceback.format_exc()}")
                    continue
            
            logger.debug("Цикл обработки файлов завершен, ожидание 5 секунд")
            time.sleep(5)
            
        except Exception as e:
            logger.error(f"Критическая ошибка в основном цикле загрузки: {e}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            logger.info("Ожидание 30 секунд перед повторной попыткой")
            time.sleep(30)



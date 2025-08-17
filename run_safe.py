#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Безопасная версия основного файла для тестирования логирования
"""

from logger import get_logger
import multiprocessing
import sys
import time
import traceback

# Получаем логгер для основного процесса
logger = get_logger('MainProcess')

def mock_open_tables_process():
    """Имитация процесса открытия таблиц"""
    logger = get_logger('OpenTables')
    logger.info("Запуск имитации процесса открытия таблиц")
    
    for i in range(5):
        try:
            logger.info(f"Имитация обработки турнира {i+1}")
            time.sleep(1)
            logger.debug(f"Турнир {i+1} обработан успешно")
        except Exception as e:
            logger.error(f"Ошибка при обработке турнира {i+1}: {e}")
    
    logger.info("Имитация процесса открытия таблиц завершена")

def mock_close_tables_process():
    """Имитация процесса закрытия таблиц"""
    logger = get_logger('CloseTables')
    logger.info("Запуск имитации процесса закрытия таблиц")
    
    for i in range(3):
        try:
            logger.info(f"Имитация проверки таблицы {i+1}")
            time.sleep(0.5)
            logger.debug(f"Таблица {i+1} проверена")
        except Exception as e:
            logger.error(f"Ошибка при проверке таблицы {i+1}: {e}")
    
    logger.info("Имитация процесса закрытия таблиц завершена")

def mock_google_drive_process():
    """Имитация процесса Google Drive"""
    logger = get_logger('GoogleDrive')
    logger.info("Запуск имитации процесса Google Drive")
    
    try:
        logger.info("Проверка директории на наличие файлов")
        time.sleep(1)
        logger.info("Файлы для загрузки не найдены")
    except Exception as e:
        logger.error(f"Ошибка в процессе Google Drive: {e}")
    
    logger.info("Имитация процесса Google Drive завершена")

if __name__ == '__main__':
    try:
        logger.info("=" * 60)
        logger.info("ЗАПУСК БЕЗОПАСНОЙ ВЕРСИИ WPNCOLLECTOR")
        logger.info("=" * 60)
        logger.info(f"Версия Python: {sys.version}")
        logger.info(f"Платформа: {sys.platform}")
        
        multiprocessing.freeze_support()    
        logger.info("Поддержка многопроцессорности включена")

        # Создаем процессы
        open_tables_thread = multiprocessing.Process(
            target=mock_open_tables_process,
            name="OpenTables"
        )
        close_tables_thread = multiprocessing.Process(
            target=mock_close_tables_process,
            name="CloseTables"
        )
        google_drive_thread = multiprocessing.Process(
            target=mock_google_drive_process,
            name="GoogleDrive"
        )

        logger.info("Процессы созданы, запускаем...")

        # Запускаем процессы
        open_tables_thread.start()
        logger.info(f"Процесс OpenTables запущен (PID: {open_tables_thread.pid})")
        
        close_tables_thread.start()
        logger.info(f"Процесс CloseTables запущен (PID: {close_tables_thread.pid})")
        
        google_drive_thread.start()
        logger.info(f"Процесс GoogleDrive запущен (PID: {google_drive_thread.pid})")

        logger.info("Все основные процессы запущены успешно")
        
        # Ждем завершения процессов
        try:
            open_tables_thread.join()
            logger.info("Процесс OpenTables завершен")
        except KeyboardInterrupt:
            logger.warning("Получен сигнал прерывания для OpenTables")
            
        try:
            close_tables_thread.join()
            logger.info("Процесс CloseTables завершен")
        except KeyboardInterrupt:
            logger.warning("Получен сигнал прерывания для CloseTables")
            
        try:
            google_drive_thread.join()
            logger.info("Процесс GoogleDrive завершен")
        except KeyboardInterrupt:
            logger.warning("Получен сигнал прерывания для GoogleDrive")

        logger.info("=" * 60)
        logger.info("ВСЕ ПРОЦЕССЫ УСПЕШНО ЗАВЕРШЕНЫ")
        logger.info("=" * 60)
        
    except Exception as e:
        logger.error(f"Критическая ошибка в основном процессе: {e}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        sys.exit(1) 
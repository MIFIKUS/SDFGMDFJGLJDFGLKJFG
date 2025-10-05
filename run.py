from InLobby.Collect import open_tables_module
from InLobby.Close import close_tables_module
from Google import load_to_disk
from logger import get_logger

import multiprocessing
import sys
import traceback

# Получаем логгер для основного процесса
logger = get_logger('MainProcess')

if __name__ == '__main__':
    try:
        logger.info("Запуск приложения WPNCollector")
        logger.info(f"Версия Python: {sys.version}")
        logger.info(f"Платформа: {sys.platform}")
        
        multiprocessing.freeze_support()    
        logger.info("Поддержка многопроцессорности включена")

        # Создаем процессы
        open_tables_thread = multiprocessing.Process(
            target=open_tables_module.run,
            name="OpenTables"
        )
        close_tables_thread = multiprocessing.Process(
            target=close_tables_module.run,
            name="CloseTables"
        )
        close_bugged_lobbies_thread = multiprocessing.Process(
            target=close_tables_module.close_bugged_lobbies,
            name="CloseBuggedLobbies"
        )
        google_drive_thread = multiprocessing.Process(
            target=load_to_disk.load_to_disk_module,
            name="GoogleDrive"
        )

        logger.info("Процессы созданы, запускаем...")

        # Запускаем процессы
        open_tables_thread.start()
        logger.info(f"Процесс OpenTables запущен (PID: {open_tables_thread.pid})")
        
        close_tables_thread.start()
        logger.info(f"Процесс CloseTables запущен (PID: {close_tables_thread.pid})")
        
        close_bugged_lobbies_thread.start()
        logger.info(f"Процесс CloseBuggedLobbies запущен (PID: {close_bugged_lobbies_thread.pid})")
        
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
            close_bugged_lobbies_thread.join()
            logger.info("Процесс CloseBuggedLobbies завершен")
        except KeyboardInterrupt:
            logger.warning("Получен сигнал прерывания для CloseBuggedLobbies")
            
        #if google_drive_thread.is_alive():
        #    google_drive_thread.terminate()
        #    logger.info("Процесс GoogleDrive остановлен")

        logger.info("Приложение завершено")
        
    except Exception as e:
        logger.error(f"Критическая ошибка в основном процессе: {e}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        sys.exit(1)



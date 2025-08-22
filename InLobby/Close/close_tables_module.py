from InLobby.Close.Windows import tables
from InLobby.Close.Proceses import tables_proceses
from InLobby.Close.Files import rename
from InLobby.Extensions.database.update import update_table_status
from logger import get_logger

import time
import traceback

# Получаем логгер для модуля закрытия таблиц
logger = get_logger('CloseTables')

logger.info("Модуль закрытия таблиц инициализирован")

def run():
    logger.info("Запуск процесса закрытия таблиц")
    
    while True:
        try:
            logger.debug("Начинаем цикл проверки таблиц для закрытия")
            
            tables_windows = tables_proceses.get_tables_hwnd()
            logger.debug(f"Найдено окон таблиц: {len(tables_windows)}")

            if not tables_windows:
                logger.debug("Окна таблиц не найдены, ожидание 5 секунд")
                time.sleep(5)
                continue

            for i, table_window in enumerate(tables_windows):
                try:
                    logger.debug(f"Обрабатываем таблицу {i+1}/{len(tables_windows)} (HWND: {table_window})")
                    
                    # Получаем изображение таблицы
                    logger.debug(f"Получаем изображение таблицы {table_window}")
                    tables.get_table_img(table_window)
                    logger.debug("Изображение таблицы получено")

                    # Проверяем, закрыта ли таблица
                    if tables.table_closed():
                        logger.info(f"Таблица {table_window} закрыта, обрабатываем")
                        
                        # Получаем информацию о таблице
                        tournament_id = tables.get_table_tournament_id(table_window)
                        table_num = tables.get_table_num(table_window)
                        
                        logger.info(f"Таблица {table_window}: Tournament ID: {tournament_id}, Номер: {table_num}")
                        
                        # Закрываем таблицу
                        logger.info(f"Закрываем таблицу {table_window}")
                        tables_proceses.close_table(table_window)
                        logger.info(f"Таблица {table_window} закрыта успешно")
                        
                        # Переименовываем файл
                        logger.info(f"Переименовываем файл для Tournament ID: {tournament_id}, Table: {table_num}")
                        rename.set_file_to_complete(tournament_id, table_num)
                        logger.info(f"Файл переименован успешно")

                        update_table_status(str(tournament_id), str(table_num), 'collected')
                        
                    else:
                        logger.debug(f"Таблица {table_window} еще открыта, пропускаем")
                        
                except Exception as e:
                    logger.error(f"Ошибка при обработке таблицы {table_window}: {e}")
                    logger.error(f"Traceback: {traceback.format_exc()}")
                    continue
                    
            logger.debug("Цикл проверки таблиц завершен, ожидание 5 секунд")
            time.sleep(5)
            
        except Exception as e:
            logger.error(f"Критическая ошибка в основном цикле закрытия таблиц: {e}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            logger.info("Ожидание 30 секунд перед повторной попыткой")
            time.sleep(30)  

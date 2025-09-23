from InLobby.Close.Windows import tables
from InLobby.Close.Proceses import tables_proceses
from InLobby.Close.Files import rename
from InLobby.Extensions.database.update import update_table_status
from logger import get_logger

import time
import traceback

import win32gui
import win32con


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

def close_bugged_lobbies():
    logger.info("Запуск процесса закрытия зависших лобби")
    lobby_windows = {}

    def is_pokerking_lobby(hwnd):
        if not win32gui.IsWindowVisible(hwnd):
            return False
        title = win32gui.GetWindowText(hwnd)
        if "PokerKing Lobby Logged in as" in title:
            rect = win32gui.GetWindowRect(hwnd)
            width = rect[2] - rect[0]
            height = rect[3] - rect[1]
            if width == 996 and height == 720:
                return True
            return False
        return False

    while True:
        try:
            current_time = time.time()
            found_lobbies = []

            def enum_handler(hwnd, _):
                if is_pokerking_lobby(hwnd):
                    found_lobbies.append(hwnd)
            win32gui.EnumWindows(enum_handler, None)

            logger.debug(f"Найдено лобби: {len(found_lobbies)}")

            # Добавляем новые окна в память
            for hwnd in found_lobbies:
                if hwnd not in lobby_windows:
                    lobby_windows[hwnd] = current_time
                    logger.info(f"Добавлено новое лобби в мониторинг (HWND: {hwnd})")

            # Проверяем окна, которые уже в памяти
            to_remove = []
            for hwnd, added_time in lobby_windows.items():
                # Если окно больше не существует, удаляем из памяти
                if not win32gui.IsWindow(hwnd):
                    to_remove.append(hwnd)
                    logger.debug(f"Лобби {hwnd} больше не существует, удаляем из мониторинга")
                    continue
                # Если прошло больше 3 минут, закрываем окно
                if current_time - added_time >= 180:
                    try:
                        logger.warning(f"Закрываем зависшее лобби (HWND: {hwnd}) после 3 минут ожидания")
                        win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
                        logger.info(f"Команда закрытия отправлена для лобби {hwnd}")
                    except Exception as e:
                        logger.error(f"Ошибка при закрытии лобби {hwnd}: {e}")
                    to_remove.append(hwnd)

            for hwnd in to_remove:
                lobby_windows.pop(hwnd, None)

            logger.debug(f"Активных лобби в мониторинге: {len(lobby_windows)}")
            time.sleep(5)
        except Exception as e:
            logger.error(f"Ошибка в процессе закрытия зависших лобби: {e}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            logger.info("Ожидание 10 секунд перед повторной попыткой")
            time.sleep(10)
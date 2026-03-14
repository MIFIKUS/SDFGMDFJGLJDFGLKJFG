from InLobby.Close.Windows import tables
from InLobby.Close.Proceses import tables_proceses
from InLobby.Close.Files import rename
from InLobby.Extensions.database.update import update_table_status
import time
import traceback

import win32gui
import win32con


print("Модуль закрытия таблиц инициализирован")

def run():
    print("Запуск процесса закрытия таблиц")
    
    # Словарь для хранения времени первого обнаружения окна таблицы
    table_open_times = {}

    while True:
        try:
            print("Начинаем цикл проверки таблиц для закрытия")
            
            tables_windows = tables_proceses.get_tables_hwnd()
            print(f"Найдено окон таблиц: {len(tables_windows)}")

            current_time = time.time()

            # Удаляем из словаря окна, которых больше нет
            table_open_times = {hwnd: t for hwnd, t in table_open_times.items() if hwnd in tables_windows}

            if not tables_windows:
                print("Окна таблиц не найдены, ожидание 5 секунд")
                time.sleep(5)
                continue

            for i, table_window in enumerate(tables_windows):
                try:
                    # Если окно только что появилось — запоминаем время
                    if table_window not in table_open_times:
                        table_open_times[table_window] = current_time
                        print(f"Таблица {table_window} впервые обнаружена, запоминаем время открытия")
                        continue  # Пропускаем обработку в этот цикл

                    # Проверяем, прошло ли 20 секунд с момента открытия
                    open_duration = current_time - table_open_times[table_window]
                    if open_duration < 20:
                        print(f"Таблица {table_window} открыта только {open_duration:.1f} секунд, пропускаем")
                        continue

                    print(f"Обрабатываем таблицу {i+1}/{len(tables_windows)} (HWND: {table_window})")
                    
                    # Получаем изображение таблицы
                    print(f"Получаем изображение таблицы {table_window}")
                    tables.get_table_img(table_window)
                    print("Изображение таблицы получено")

                    # Проверяем, закрыта ли таблица
                    if tables.table_closed():
                        print(f"Таблица {table_window} закрыта, обрабатываем")
                        
                        # Получаем информацию о таблице
                        tournament_id = tables.get_table_tournament_id(table_window)
                        table_num = tables.get_table_num(table_window)
                        
                        print(f"Таблица {table_window}: Tournament ID: {tournament_id}, Номер: {table_num}")
                        
                        # Закрываем таблицу
                        print(f"Закрываем таблицу {table_window}")
                        tables_proceses.close_table(table_window)
                        print(f"Таблица {table_window} закрыта успешно")
                        
                        # Переименовываем файл
                        print(f"Переименовываем файл для Tournament ID: {tournament_id}, Table: {table_num}")
                        rename.set_file_to_complete(tournament_id, table_num)
                        print(f"Файл переименован успешно")

                        update_table_status(str(tournament_id), str(table_num), 'collected')
                        
                        # После закрытия удаляем из словаря
                        if table_window in table_open_times:
                            del table_open_times[table_window]
                        
                    else:
                        print(f"Таблица {table_window} еще открыта, пропускаем")
                        
                except Exception as e:
                    print(f"Ошибка при обработке таблицы {table_window}: {e}")
                    print(f"Traceback: {traceback.format_exc()}")
                    continue
                    
            print("Цикл проверки таблиц завершен, ожидание 5 секунд")
            time.sleep(5)
            
        except Exception as e:
            print(f"Критическая ошибка в основном цикле закрытия таблиц: {e}")
            print(f"Traceback: {traceback.format_exc()}")
            print("Ожидание 30 секунд перед повторной попыткой")
            time.sleep(30)  

def close_bugged_lobbies():
    print("Запуск процесса закрытия зависших лобби")
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

            print(f"Найдено лобби: {len(found_lobbies)}")

            # Добавляем новые окна в память
            for hwnd in found_lobbies:
                if hwnd not in lobby_windows:
                    lobby_windows[hwnd] = current_time
                    print(f"Добавлено новое лобби в мониторинг (HWND: {hwnd})")

            # Проверяем окна, которые уже в памяти
            to_remove = []
            for hwnd, added_time in lobby_windows.items():
                # Если окно больше не существует, удаляем из памяти
                if not win32gui.IsWindow(hwnd):
                    to_remove.append(hwnd)
                    print(f"Лобби {hwnd} больше не существует, удаляем из мониторинга")
                    continue
                # Если прошло больше 3 минут, закрываем окно
                if current_time - added_time >= 180:
                    try:
                        print(f"Закрываем зависшее лобби (HWND: {hwnd}) после 3 минут ожидания")
                        win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
                        print(f"Команда закрытия отправлена для лобби {hwnd}")
                    except Exception as e:
                        print(f"Ошибка при закрытии лобби {hwnd}: {e}")
                    to_remove.append(hwnd)

            for hwnd in to_remove:
                lobby_windows.pop(hwnd, None)

            print(f"Активных лобби в мониторинге: {len(lobby_windows)}")
            time.sleep(5)
        except Exception as e:
            print(f"Ошибка в процессе закрытия зависших лобби: {e}")
            print(f"Traceback: {traceback.format_exc()}")
            print("Ожидание 10 секунд перед повторной попыткой")
            time.sleep(10)



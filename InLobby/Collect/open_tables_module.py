from fileinput import close
from InLobby.Collect.main_lobby import main_lobby
from InLobby.Collect.tournament_lobby import tournament_lobby
from InLobby.Extensions.proceses.tables import get_amount_of_opened_tables
from InLobby.Collect.tournament_lobby.extensions.win_actions import lobby_loaded, close_exit_from_lobby_window, there_is_one_lobby_window
from InLobby.Extensions.proceses.tables import *

from Google.Sheets import get, add, statuses
from pywinauto.findwindows import ElementAmbiguousError

import time
import traceback
import win32gui

AMOUNT_OF_TABLES = get.get_max_tables()

print(f"Модуль открытия таблиц инициализирован. Максимальное количество таблиц: {AMOUNT_OF_TABLES}")

main_lobby_window = main_lobby.get_main_lobby()
print("Главное окно лобби получено")

def run():
    print("Запуск процесса открытия таблиц")
    
    while True:
        try:
            if not is_pokerking_running():
                run_app_windows(r'C:\PokerKing\PokerKing.exe')
                time.sleep(60)
            if check_disconect_banner():
                close_disconect_banner()
                time.sleep(15)
                login()
                time.sleep(10)
                go_to_tournaments()
                time.sleep(15)
            elif check_reconect_banner():
                reconect()
                time.sleep(15)
                go_to_tournaments()
                time.sleep(15)
                
            current_tables = get_amount_of_opened_tables()
            print(f"Текущее количество открытых таблиц: {current_tables}")
            
            if current_tables >= AMOUNT_OF_TABLES:
                add.set_status(statuses.WAIT_TABLES_TO_CLOSE)
                print(f"Достигнут лимит таблиц ({AMOUNT_OF_TABLES}), ожидание...")
                time.sleep(10)
                continue
                
            # Проверяем, что главное окно лобби все еще доступно
            while True:
                try:
                    main_lobby_window.set_focus()
                    break
                except Exception as e:
                    print(f"Не удается получить доступ к главному окну лобби: {e}")
                    print("Попытка переинициализации главного окна лобби...")
                    try:
                        main_lobby_window = main_lobby.get_main_lobby()
                        print("Главное окно лобби переинициализировано")
                        break
                    except Exception as reinit_error:
                        add.set_status(statuses.EROOR)
                        print(f"Не удалось переинициализировать главное окно лобби: {reinit_error}")
                        time.sleep(30)
                        continue
                
            print(f"Начинаем поиск турниров для открытия таблиц. Доступно мест: {AMOUNT_OF_TABLES - current_tables}")
            
            if not is_pokerking_running():
                run_app_windows(r'C:\PokerKing\PokerKing.exe')
                time.sleep(60)
            if check_disconect_banner():
                close_disconect_banner()
                time.sleep(15)
                login()
                time.sleep(10)
                go_to_tournaments()
                time.sleep(15)
            elif check_reconect_banner():
                reconect()
                time.sleep(15)
                go_to_tournaments()
                time.sleep(15)

            try:
                tournaments, tournaments_raw = main_lobby.get_list_of_tournaments(main_lobby_window)
                print(f"Найдено турниров: {len(tournaments)}")
            except ElementAmbiguousError:
                add.set_status(statuses.LOBBY)
                print("Ошибка при получении списка турниров: ElementAmbiguousError")
                print("Ожидание 10 секунд перед повторной попыткой")
                time.sleep(10)
                continue
            except Exception as e:
                add.set_status(statuses.EROOR)
                print(f"Ошибка при получении списка турниров: {e}")
                print("Ожидание 10 секунд перед повторной попыткой")
                time.sleep(10)
                continue

            for i, (tournament, tournament_raw) in enumerate(zip(tournaments, tournaments_raw)):
                
                if not is_pokerking_running():
                    run_app_windows(r'C:\PokerKing\PokerKing.exe')
                    time.sleep(60)
                if check_disconect_banner():
                    close_disconect_banner()
                    time.sleep(15)
                    login()
                    time.sleep(10)
                    go_to_tournaments()
                    time.sleep(15)
                elif check_reconect_banner():
                    reconect()
                    time.sleep(15)
                    go_to_tournaments()
                    time.sleep(15)

                try:
                    current_tables = get_amount_of_opened_tables()
                    add.set_amount_of_opened_tables(current_tables)
                    if current_tables >= AMOUNT_OF_TABLES:
                        print(f"Достигнут лимит таблиц ({AMOUNT_OF_TABLES}), останавливаем поиск")
                        break
                        
                    print(f"Обрабатываем турнир {i+1}/{len(tournaments)}: {tournament}")
                    
                    time.sleep(0.5)
                    main_lobby_window.set_focus()
                    close_exit_from_lobby_window(main_lobby_window)
                    print("Фокус установлен на главное окно лобби")

                    tournament_status = main_lobby.get_tournament_status(tournament_raw)
                    if not tournament_status:
                        continue
                    print(f"Статус турнира: {tournament_status}")

                    try:
                        print(f"Переключаемся на турнир: {tournament}")
                        main_lobby.switch_tournament(tournament)
                        print("Переключение на турнир выполнено")
                        
                        print(f"Открываем турнир: {tournament}")
                        if not main_lobby.open_tournament(tournament):
                            print(f"Не удалось открыть турнир {tournament}, пропускаем")
                            continue
                        print(f"Турнир {tournament} открыт успешно")
                    

                    except Exception as e:
                        add.set_status(statuses.EROOR)
                        print(f"Ошибка при работе с турниром {tournament}: {e}")
                        print(f"Traceback: {traceback.format_exc()}")
                        for _ in range(1):
                            try:
                                tournament_lobby_window.close()
                            except:
                                pass
                        continue

                    #print(f"Ожидание загрузки турнира {tournament} (15 секунд)")
                    #time.sleep(15)

                    tournament_lobby_window = tournament_lobby._get_lobby_window()
                    print("Окно лобби турнира получено")

                    print(f"Открываем таблицы для турнира {tournament} со статусом {tournament_status}")
                    add.set_status(statuses.OPENING)
                    tournament_lobby.open_tables(tournament_status)
                    print(f"Таблицы для турнира {tournament} открыты")
                    
                    while not there_is_one_lobby_window():
                        for _ in range(1):
                            try:
                                try:
                                    hwnd = tournament_lobby_window.handle
                                    win32gui.PostMessage(hwnd, 0x0010, 0, 0)  # 0x0010 = WM_CLOSE
                                except Exception as e:
                                    print(f"Ошибка при попытке закрыть окно через win32: {e}")
                            except Exception as e:
                                print(f"Ошибка при закрытии окна лобби турнира {tournament}: {e}")
                                pass
                        print(f"Окно лобби турнира {tournament} закрыто")
                        time.sleep(0.5)

                    current_tables = get_amount_of_opened_tables()
                    print(f"Турнир {tournament} обработан. Текущее количество таблиц: {current_tables}")


                except Exception as e:
                    add.set_status(statuses.EROOR)
                    print(f"Ошибка при обработке турнира {tournament}: {e}")
                    print(f"Traceback: {traceback.format_exc()}")
                    continue

            print("Все доступные турниры обработаны, ожидание 10 секунд перед следующим циклом")
            time.sleep(10)
        
        except ElementAmbiguousError:
            add.set_status(statuses.LOBBY)
            print("Критическая ошибка в основном цикле открытия таблиц: ElementAmbiguousError")
            print(f"Traceback: {traceback.format_exc()}")
            print("Ожидание 30 секунд перед повторной попыткой")
            time.sleep(30)
        except Exception as e:
            add.set_status(statuses.EROOR)
            print(f"Критическая ошибка в основном цикле открытия таблиц: {e}")
            print(f"Traceback: {traceback.format_exc()}")
            print("Ожидание 30 секунд перед повторной попыткой")
            time.sleep(30)
from InLobby.Collect.tournament_lobby.extensions.in_lobby import get_table_num, get_table_num_by_element, get_table_nums_from_elements_list, get_tournament_id, get_tournament_name
from InLobby.Collect.tournament_lobby.extensions.win_actions import set_focus_on_window
from InLobby.Extensions.proceses.tables import get_amount_of_opened_tables
from InLobby.Collect.tournament_lobby.extensions.win_actions import close_top_window, wait_table_for_loading, close_loading_window

from InLobby.Extensions.database import get, add


from pywinauto import Desktop
from pywinauto import mouse

import pyautogui
import win32gui
import time
import traceback

def _get_lobby_window():
    hwnd = win32gui.GetForegroundWindow()
    return Desktop(backend="uia").window(handle=hwnd)


def _is_there_tables_players_button(win):
    for btn in win.descendants(control_type="Button"):
        if btn.element_info.name == "Tables/Players":
            return btn
    return None


def _click_players_button(button):
    button.click_input()


def _get_list_of_tables(win) -> list:
    all_buttons = win.descendants(control_type="Button")
    # Фильтруем подходящие кнопки
    matching_buttons = []
    for btn in all_buttons:
        name = btn.element_info.name or ""
        if "Table" in name and len(name.split()) == 5:
            matching_buttons.append(btn)
    return matching_buttons


def _open_table(table_button):
    while True:
        try:
            pyautogui.FAILSAFE = False
            rect = table_button.rectangle()
            x = (rect.left + rect.right) // 2
            y = (rect.top + rect.bottom) // 2 - 5
    
            for _ in range(2):
                pyautogui.click(x=x, y=y)
            break
        except:
            pass


def _switch_table(table_button):
    table_button.invoke()


def open_tables(tournament_status: str):
    #TODO: Сделать чтобы выяснял сколько столов открыто
    lobby_window = _get_lobby_window()

    if table_players_button := _is_there_tables_players_button(lobby_window):
        _click_players_button(table_players_button)

    seen_tables = set()
    
    counter = 0
    tournament_id = None
    
    while True:
        wheels_counter = 0
        tables = _get_list_of_tables(lobby_window)

        tables_text_list = get_table_nums_from_elements_list(tables)

        if set(tables_text_list).issubset(seen_tables):
            break
        
        counter == 0
        for table in tables:
            amount_of_opened_tables = get_amount_of_opened_tables()
            print("amount_of_opened_tables", amount_of_opened_tables)
            if amount_of_opened_tables == 20:
                return
            
            set_focus_on_window(lobby_window)
            try:
                table_num = get_table_num_by_element(table)
                print(table_num)
            except:
                print("Ошибка получения номера стола")
                traceback.print_exc()
                continue

            if table_num in seen_tables:
                continue
            if tournament_id:
                if tournament_id and get.get_table_status(tournament_id, table_num):
                    seen_tables.add(table_num)
                    continue

            counter += 1

            table_opened = False
            fail_to_open_table_counter = 0

            while not table_opened:
                try:
                    if tournament_id:
                        if tournament_id and get.get_table_status(tournament_id, table_num):
                            continue
                    _switch_table(table)
                    time.sleep(5)

                    _open_table(table)
                    if wait_table_for_loading() is not False:
                        table_opened = True
                    else:
                        print("table not opened")
                        close_loading_window()
                        time.sleep(0.5)
                        fail_to_open_table_counter += 1
                        if fail_to_open_table_counter == 4:
                            print('Не удалось открыть стол. Пропуск')
                            break
                except:
                    print('Ошибка открытия стола')
                    traceback.print_exc()
                    break
            if not table_opened:
                continue
            
            if counter == 1:
                tournament_id = get_tournament_id()
                tournament_name = get_tournament_name()
                if tournament_id and get.get_table_status(tournament_id, table_num):
                    close_top_window()
                    time.sleep(0.5)
                    continue

            add.add_table_info(tournament_id, tournament_name, table_num, "opened")

            seen_tables.add(table_num)
        
        wheels_counter += 1


def close_tournament_lobby(win):
    win.close()



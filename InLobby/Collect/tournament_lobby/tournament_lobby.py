from InLobby.Collect.tournament_lobby.extensions.in_lobby import get_table_num, get_table_num_by_element, get_table_nums_from_elements_list
from InLobby.Collect.tournament_lobby.extensions.win_actions import set_focus_on_window

from pywinauto import Desktop
from pywinauto import mouse

import pyautogui
import win32gui
import time

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


def _is_table_visible(win, table_num) -> bool:
    #Проверяет что стол видно и что его можно открыть
    #TODO:Сделать чтобы стол был одним из первых в списке
    #TODO: Сделать чтобы передавался список столов
    tables_nums_clear = []
    for i in _get_list_of_tables(win):
        print(i)
        if i.element_info.visible:
            tables_nums_clear.append(get_table_num_by_element(i))

    if table_num in tables_nums_clear:
        return True
    return False


def _open_table(table_button):
    while True:
        try:
            pyautogui.FAILSAFE = False
            rect = table_button.rectangle()
            x = (rect.left + rect.right) // 2
            y = (rect.top + rect.bottom) // 2 - 3
    
            for _ in range(2):
                pyautogui.click(x=x, y=y)
            break
        except:
            pass


def _switch_table(table_button):
    table_button.invoke()



def _scroll_down():
    pyautogui.scroll(-183)


def open_tables():
    #TODO: Сделать чтобы выяснял сколько столов открыто
    lobby_window = _get_lobby_window()

    if table_players_button := _is_there_tables_players_button(lobby_window):
        _click_players_button(table_players_button)

    seen_tables = set()
    
    counter = 0
    
    while True:
        wheels_counter = 0
        tables = _get_list_of_tables(lobby_window)

        tables_text_list = get_table_nums_from_elements_list(tables)

        if set(tables_text_list).issubset(seen_tables):
            break
        

        for table in tables:
            set_focus_on_window(lobby_window)
            table_num = get_table_num_by_element(table)
            print(table_num)

            if table_num in seen_tables:
                continue

            _switch_table(table)
            _open_table(table)

            time.sleep(1.2)

            seen_tables.add(table_num)
        
        wheels_counter += 1





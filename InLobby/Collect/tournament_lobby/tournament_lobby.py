from InLobby.Collect.tournament_lobby.extensions.in_lobby import get_table_num

from pywinauto import Desktop

import win32gui
import time

def _get_lobby_window():
    hwnd = win32gui.GetForegroundWindow()
    return Desktop(backend="uia").window(handle=hwnd)


def _is_there_tables_players_button(win) -> bool:
    #TODO: Сделать чтобы если нет этой кнопки ничего не ломалось
    all_buttons = win.descendants(control_type="Button")
    print(all_buttons)
    matching = [btn for btn in all_buttons
            if btn.element_info.name == "Tables/Players"]

    return matching[0]


def _click_players_button(button):
    button.click_input()


def _get_list_of_tables(win) -> list:
    all_buttons = win.descendants(control_type="Button")
    # Фильтруем подходящие кнопки
    matching_buttons = []
    for btn in all_buttons:
        name = btn.element_info.name or ""
        print(name)
        if "Table" in name and len(name.split()) == 5:
            matching_buttons.append(btn)


def _is_table_visible(win, table_num) -> bool:
    #Проверяет что стол видно и что его можно открыть
    #TODO:Сделать чтобы стол был одним из первых в списке
    tables_nums_clear = []
    for i in _get_list_of_tables(win):
        tables_nums_clear.append(get_table_num(i))

    if table_num in tables_nums_clear:
        return True
    return False


def _open_table(table_button):
    for _ in range(2):
        table_button.click_input()


def open_tables():
    #TODO: Сделать чтобы выяснял сколько столов открыто
    lobby_window = _get_lobby_window()

    if table_players_button := _is_there_tables_players_button(lobby_window):
        _click_players_button(table_players_button)




time.sleep(5)
#open_tables()
lobby_window = _get_lobby_window()
print(_get_list_of_tables(lobby_window))


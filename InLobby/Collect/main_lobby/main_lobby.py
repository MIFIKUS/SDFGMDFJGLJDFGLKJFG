from pywinauto import Desktop
from InLobby.Collect.tournament_lobby.tournament_lobby import _get_list_of_tables
import pyautogui
import time


def get_main_lobby():
    return Desktop(backend="uia").window(title_re="PokerKing Lobby Logged in as.*")


def get_list_of_tournaments(win) -> list:
    all_buttons = win.descendants(control_type="Button")


    matching_raw = []
    matching = []
    for btn in all_buttons:
        name = btn.element_info.name or ""
        if 'Add this event to "Yours" section.' in name and len(btn.descendants()) > 2:
            matching_raw.append(btn)
            matching.append(btn.descendants()[2])
    return matching, matching_raw


def switch_tournament(tournament_button):
    tournament_button.invoke()


def open_tournament(tournament_button):
    while True:
        try:
            pyautogui.FAILSAFE = False
            rect = tournament_button.rectangle()
            x = (rect.left + rect.right) // 2
            y = (rect.top + rect.bottom) // 2 - 3
    
            for _ in range(2):
                pyautogui.click(x=x, y=y)
            break
        except:
            pass
    tournament_lobby_opened()


def get_tournament_status(tournament_button) -> str:
    #LateReg или Running 
    status_raw = tournament_button.descendants()[1].element_info.name

    if 'Late Reg' in status_raw:
        return 'Late Reg'
    return 'Running'


def tournament_lobby_opened() -> bool:
    """
    Проверяет, открыт ли лобби турнира, ожидая появления кнопки "Players/Tables" или наличия столов.
    Возвращает True, если лобби открыто, иначе False.
    """

    while True:
        try:
            # Используем win32gui для получения активного окна
            import win32gui
            hwnd = win32gui.GetForegroundWindow()
            win = Desktop(backend="uia").window(handle=hwnd)
            
            # Ищем кнопку "Players/Tables"
            buttons = win.descendants(control_type="Button")
            for btn in buttons:
                name = btn.element_info.name or ""
                if "Tables" in name:
                    return True
            # Либо ищем наличие столов (например, по control_type="DataItem" или "ListItem")
            tables = _get_list_of_tables(win)
            if tables:
                return True
        except Exception as e:
            print(e)
            pass
        time.sleep(0.1)  # Небольшая задержка для снижения нагрузки на CPU

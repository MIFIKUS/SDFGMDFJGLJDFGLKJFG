from pywinauto import Desktop
from InLobby.Collect.tournament_lobby.tournament_lobby import _get_list_of_tables
import pyautogui
import time


def get_main_lobby():
    return Desktop(backend="uia").window(title_re="PokerKing Lobby Logged in as.*")

def get_tournament_status(tournament_button) -> bool:
    #LateReg или Running 
    status_raw = tournament_button.descendants()[1].element_info.name

    if 'Late Reg' in status_raw or 'Running' in status_raw:
        return True
    return False


def get_list_of_tournaments(win) -> list:
    all_buttons = win.descendants(control_type="Button")

    matching_raw = []
    matching = []
    for btn in all_buttons:
        name = btn.element_info.name or ""
        if 'Add this event to "Yours" section.' in name and len(btn.descendants()) > 2:
            if not get_tournament_status(btn):
            #    continue
            matching_raw.append(btn)
            matching.append(btn.descendants()[2])
    return matching, matching_raw


def switch_tournament(tournament_button):
    tournament_button.invoke()


def open_tournament(tournament_button):
    max_attempts = 5
    attempt = 0
    
    while attempt < max_attempts:
        try:
            pyautogui.FAILSAFE = False
            rect = tournament_button.rectangle()
            x = (rect.left + rect.right) // 2
            y = (rect.top + rect.bottom) // 2 - 3
    
            for _ in range(2):
                pyautogui.click(x=x, y=y)
            break
        except Exception as e:
            print(f"Попытка {attempt + 1} открытия турнира не удалась: {e}")
            attempt += 1
            time.sleep(1)
    
    if attempt >= max_attempts:
        print("Не удалось открыть турнир после всех попыток")
        return False
    
    return tournament_lobby_opened()



def tournament_lobby_opened() -> bool:
    """
    Проверяет, открыт ли лобби турнира, ожидая появления кнопки "Players/Tables" или наличия столов.
    Возвращает True, если лобби открыто, иначе False.
    """
    max_wait_time = 30  # Максимальное время ожидания 30 секунд
    counter = 0
    
    while counter < max_wait_time:
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
            print(f"Ошибка при проверке открытия лобби турнира: {e}")
            pass
        time.sleep(0.1)  # Небольшая задержка для снижения нагрузки на CPU
        counter += 1
    
    print("Таймаут ожидания открытия лобби турнира")
    return False

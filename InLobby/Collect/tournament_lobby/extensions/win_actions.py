import win32gui
import win32con
import time
from pywinauto import Desktop
import traceback

def set_focus_on_window(win):
    for _ in range(3):
        win.set_focus()

def close_top_window():
    win32gui.SetForegroundWindow(win32gui.GetTopWindow(win32gui.GetForegroundWindow()))
    win32gui.PostMessage(win32gui.GetForegroundWindow(), win32con.WM_CLOSE, 0, 0)



def close_loading_window():
    """
    Функция ищет среди всех окон то, в заголовке которого есть 'Loading'.
    Если текущее активное окно не содержит 'Loading' в заголовке, переключается на первое найденное окно с 'Loading' и закрывает его.
    Если окно с 'Loading' не найдено, ничего не делает.
    """
    current_hwnd = win32gui.GetForegroundWindow()
    current_title = win32gui.GetWindowText(current_hwnd)
    target_hwnd = None

    if "Loading" in current_title:
        target_hwnd = current_hwnd
    else:
        def enum_windows_callback(hwnd, result):
            title = win32gui.GetWindowText(hwnd)
            if "Loading" in title:
                result.append(hwnd)
        windows_with_loading = []
        win32gui.EnumWindows(enum_windows_callback, windows_with_loading)
        if windows_with_loading:
            target_hwnd = windows_with_loading[0]

    if target_hwnd:
        win32gui.SetForegroundWindow(target_hwnd)
        win32gui.PostMessage(target_hwnd, win32con.WM_CLOSE, 0, 0)

def lobby_loaded():
    """
    Функция ожидает, пока не появятся два окна с текстом 'PokerKing Lobby Logged in as' в заголовке.
    Как только такие два окна найдены, возвращает их список.
    """

    while True:
        windows = Desktop(backend="uia").windows()
        matching = [w for w in windows if "PokerKing Lobby Logged in as" in (w.window_text() or "")]
        if len(matching) >= 2:
            return 
        time.sleep(0.5)

def wait_table_for_loading():
    counter = 0
    while True:
        title = win32gui.GetWindowText(win32gui.GetForegroundWindow()).lower()
        if "table" in title.lower():
            return
        time.sleep(1)
        counter += 1
        if counter > 10:
            return False
    
def close_exit_from_lobby_window(win):
    try:
        btn = win.child_window(auto_id="errorpopup-2btn-cancel", control_type="Button")
        btn.invoke()
    except:
        traceback.print_exc()
        pass


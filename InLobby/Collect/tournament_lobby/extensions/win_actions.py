import win32gui
import win32con
import time

def set_focus_on_window(win):
    for _ in range(3):
        win.set_focus()

def close_top_window():
    win32gui.SetForegroundWindow(win32gui.GetTopWindow(win32gui.GetForegroundWindow()))
    win32gui.PostMessage(win32gui.GetForegroundWindow(), win32con.WM_CLOSE, 0, 0)


def wait_table_for_loading():
    while True:
        title = win32gui.GetWindowText(win32gui.GetForegroundWindow()).lower()
        if "table" in title.lower():
            return
        time.sleep(1)
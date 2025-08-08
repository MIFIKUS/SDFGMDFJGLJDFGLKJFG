import win32gui
import win32con


def get_tables_hwnd():
    hwnds = []

    def callback(hwnd, _):
        title = win32gui.GetWindowText(hwnd).lower()
        if 'table' in title:
            hwnds.append(hwnd)

    win32gui.EnumWindows(callback, None)
    
    return hwnds


def close_table(hwnd):
    win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
import win32gui


def get_amount_of_opened_tables() -> int:
    w = []
    win32gui.EnumWindows(lambda h,_: w.append(win32gui.GetWindowText(h))
                        if win32gui.IsWindowVisible(h) else None,
                        None)
    return sum('table' in t.lower() in t.lower() for t in w)


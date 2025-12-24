import win32gui
import pyautogui  # type: ignore
import psutil
import os
import sys

def get_amount_of_opened_tables() -> int:
    w = []
    win32gui.EnumWindows(lambda h,_: w.append(win32gui.GetWindowText(h))
                        if win32gui.IsWindowVisible(h) else None,
                        None)
    return sum('table' in t.lower() in t.lower() for t in w)


def check_disconect_banner():
    """
    Проверяет наличие баннера потери соединения на экране.
    Возвращает True, если найдена `disconect_banner.png` или `diconect_banner_1.png`.
    """
    pyautogui.FAILSAFE = False
    try:
        banners = (
            r'InLobby\Collect\imgs\disconect_banner.png',
            r'InLobby\Collect\imgs\diconect_banner_1.png',
        )
        for banner_path in banners:
            if pyautogui.locateOnScreen(banner_path, confidence=0.7):
                return True
        return False
    except Exception:
        # Если поиск картинки по какой‑то причине не удался, считаем что баннера нет
        return False


def check_reconect_banner():
    """
    Проверяет наличие баннера потери соединения на экране.
    Возвращает True, если найдена `disconect_banner.png` или `diconect_banner_1.png`.
    """
    pyautogui.FAILSAFE = False
    try:
        banners = (
            r'InLobby\Collect\imgs\disconect_banner_2.png',
        )
        for banner_path in banners:
            if pyautogui.locateOnScreen(banner_path, confidence=0.7):
                return True
        return False
    except Exception:
        # Если поиск картинки по какой‑то причине не удался, считаем что баннера нет
        return False


def close_disconect_banner():
    """
    Закрывает баннер потери соединения кликом по координатам внутри
    активного окна (x=630, y=585 относительно левого верхнего угла окна).
    """
    pyautogui.FAILSAFE = False

    hwnd = win32gui.GetForegroundWindow()
    if not hwnd:
        return False

    left, top, _, _ = win32gui.GetWindowRect(hwnd)
    target_x = left + 630
    target_y = top + 585

    pyautogui.click(target_x, target_y)

def login():
    pyautogui.FAILSAFE = False

    hwnd = win32gui.GetForegroundWindow()
    if not hwnd:
        return False

    left, top, _, _ = win32gui.GetWindowRect(hwnd)
    target_x = left + 1025
    target_y = top + 455

    pyautogui.click(target_x, target_y)

def go_to_tournaments():
    pyautogui.FAILSAFE = False

    hwnd = win32gui.GetForegroundWindow()
    if not hwnd:
        return False

    left, top, _, _ = win32gui.GetWindowRect(hwnd)
    target_x = left + 500
    target_y = top + 125

    pyautogui.click(target_x, target_y)

def reconect():
    pyautogui.FAILSAFE = False

    hwnd = win32gui.GetForegroundWindow()
    if not hwnd:
        return False

    left, top, _, _ = win32gui.GetWindowRect(hwnd)
    target_x = left + 535
    target_y = top + 555

    pyautogui.click(target_x, target_y)

def is_pokerking_running():
    # Проходим по всем запущенным процессам
    for proc in psutil.process_iter(attrs=['pid', 'name']):
        try:
            # Сравниваем имя процесса, игнорируя регистр
            if proc.info['name'].lower() == 'pokerking.exe'.lower():
                return True
        except:
            pass
    return False

def run_app_windows(file_path, arguments=None):
    """
    Специальная функция для Windows
    """
    if sys.platform != "win32":
        print("Эта функция предназначена только для Windows")
        return False
    
    try:
        if arguments:
            # Используем subprocess для передачи аргументов
            import subprocess
            cmd = [file_path]
            if isinstance(arguments, list):
                cmd.extend(arguments)
            else:
                cmd.append(str(arguments))
            subprocess.Popen(cmd)
        else:
            # Простой запуск через os.startfile
            os.startfile(file_path)
        return True
    except Exception as e:
        print(f"Ошибка при запуске: {e}")
        return False
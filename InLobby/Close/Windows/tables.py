from InLobby.Close.Windows.img_matching import matching

from PIL import Image

import ctypes
import win32gui, win32ui, win32con

import re


def get_table_img(hwnd):
    # Получаем размеры окна
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    width, height = right - left, bottom - top

    # Контекст устройства окна
    hwnd_dc = win32gui.GetWindowDC(hwnd)
    mfc_dc  = win32ui.CreateDCFromHandle(hwnd_dc)
    save_dc = mfc_dc.CreateCompatibleDC()

    # Создаём битмап той же ширины/высоты
    bmp = win32ui.CreateBitmap()
    bmp.CreateCompatibleBitmap(mfc_dc, width, height)
    save_dc.SelectObject(bmp)

    # Печатаем содержимое окна в наш DC (ботинок даже если окно свернуто)
    # Флаг 0 — стандартная отрисовка, на Windows 8+ можно использовать 0x00000002 (PW_RENDERFULLCONTENT)
    result = ctypes.windll.user32.PrintWindow(hwnd, save_dc.GetSafeHdc(), 0x00000002)
    if result != 1:
        raise RuntimeError("Не удалось захватить окно (PrintWindow вернул %d)" % result)

    # Преобразуем в PIL Image
    bmp_info = bmp.GetInfo()
    bmp_str  = bmp.GetBitmapBits(True)
    img = Image.frombuffer(
        'RGB',
        (bmp_info['bmWidth'], bmp_info['bmHeight']),
        bmp_str, 'raw', 'BGRX', 0, 1
    )

    # Освобождаем ресурсы
    win32gui.DeleteObject(bmp.GetHandle())
    save_dc.DeleteDC()
    mfc_dc.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwnd_dc)

    img.save('Inlobby\\Close\\Windows\\imgs\\screenshots\\table.png')



def table_closed() -> bool:
    return matching('Inlobby\\Close\\Windows\\imgs\\screenshots\\table.png',
                    'Inlobby\\Close\\Windows\\imgs\\templates\\table_closed.png')


def get_table_tournament_id(hwnd):
    title = win32gui.GetWindowText(hwnd)
    return title.split()[-1].replace('(', '').replace(')', '')


def get_table_num(hwnd):
    title = win32gui.GetWindowText(hwnd)    
    return re.search(r", Table (.*?) - ", title).group(1).strip()

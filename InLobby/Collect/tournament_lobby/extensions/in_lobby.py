import win32gui
import re

#--------------Info From String--------------
def get_table_num(table_num_raw: str) -> str:
    return table_num_raw.split()[1]


#--------------Info From Element--------------
def get_table_num_by_element(element) -> str:
    text = element.element_info.name
    return get_table_num(text)


def get_table_nums_from_elements_list(elements_list: list) -> list:
    ready_list = []

    for i in elements_list:
        ready_list.append(get_table_num_by_element(i))
    
    return ready_list


#--------------Info From Window--------------
def get_tournament_id():
    hwnd = win32gui.GetForegroundWindow()      # получаем дескриптор активного окна
    title = win32gui.GetWindowText(hwnd)       # читаем его заголовок
    
    tournament_id = title.split()[-1].replace(')', '').replace('(', '')
    return tournament_id
    


def get_tournament_name():
    hwnd = win32gui.GetForegroundWindow()      # получаем дескриптор активного окна
    title = win32gui.GetWindowText(hwnd)       # читаем его заголовок
    try:
        tournament_name = re.search(r' - (.*?), Table', title).group(1).strip()
    except:
        tournament_name = re.search(r'(.*?), Table', title).group(1).strip()
    return tournament_name


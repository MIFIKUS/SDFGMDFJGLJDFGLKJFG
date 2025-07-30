def get_table_num(table_num_raw: str) -> str:
    return table_num_raw.split()[1]


def get_table_num_by_element(element) -> str:
    text = element.element_info.name
    return get_table_num(text)


def get_table_nums_from_elements_list(elements_list: list) -> list:
    ready_list = []

    for i in elements_list:
        ready_list.append(get_table_num_by_element(i))
    
    return ready_list

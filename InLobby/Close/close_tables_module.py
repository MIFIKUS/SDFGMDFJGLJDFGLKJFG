from InLobby.Close.Windows import tables
from InLobby.Close.Proceses import tables_proceses
from InLobby.Close.Files import rename

import time
import traceback

def run():
    while True:
        tables_windows = tables_proceses.get_tables_hwnd()

        for table_window in tables_windows:
            try:
                tables.get_table_img(table_window)

                if tables.table_closed():
                    tournament_id = tables.get_table_tournament_id(table_window)
                    table_num = tables.get_table_num(table_window)

                    tables_proceses.close_table(table_window)

                    rename.set_file_to_complete(tournament_id, table_num)
            except:
                print("Ошибка закрытия стола")
                traceback.print_exc()
                continue
        time.sleep(5)  

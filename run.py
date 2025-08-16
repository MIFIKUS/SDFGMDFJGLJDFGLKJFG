from InLobby.Collect import open_tables_module
from InLobby.Close import close_tables_module
from Google import load_to_disk

import multiprocessing



if __name__ == '__main__':
    multiprocessing.freeze_support()    

    open_tables_thread = multiprocessing.Process(target=open_tables_module.run)
    close_tables_thread = multiprocessing.Process(target=close_tables_module.run)
    google_drive_thread = multiprocessing.Process(target=load_to_disk.load_to_disk_module)


    open_tables_thread.start()
    close_tables_thread.start()
    #google_drive_thread.start()



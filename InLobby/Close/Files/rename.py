from config import CONFIG
import os



def set_file_to_complete(tournament_id, table_num):
    PATH_TO_HAND_HISTORY = CONFIG['PATH_TO_HAND_HISTORY']
    files = os.listdir(PATH_TO_HAND_HISTORY)
    
    for file in files:
        if file.split('_')[1] == tournament_id and file.split('_')[2] == table_num:
            old_filename = PATH_TO_HAND_HISTORY + file
            new_filename = PATH_TO_HAND_HISTORY + f'COMPLETE_{tournament_id}_{table_num}_0.data'

            os.rename(old_filename, new_filename)

            
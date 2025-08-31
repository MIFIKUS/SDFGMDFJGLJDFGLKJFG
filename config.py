import logging

CONFIG = {
    'script_name': 'TEST', 
    'cell_num': 0,
    'PATH_TO_HAND_HISTORY': 'D:\\Programs\\PokerKing\\handHistory\\',
    'logging': {
        'level': logging.INFO,  # Уровень логирования: DEBUG, INFO, WARNING, ERROR, CRITICAL
        'console_level': logging.INFO,  # Уровень для консоли
        'file_level': logging.DEBUG,    # Уровень для файлов
        'max_file_size_mb': 10,         # Максимальный размер файла лога в МБ
        'backup_count': 5,              # Количество резервных файлов
        'daily_backup_count': 30,       # Количество ежедневных резервных файлов
        'error_file_size_mb': 5,        # Максимальный размер файла ошибок в МБ
        'error_backup_count': 3         # Количество резервных файлов ошибок
    }
}


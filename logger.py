import logging
import logging.handlers
import os
import sys
from datetime import datetime
from pathlib import Path
import time

# Проверяем, существует ли config.py перед импортом
try:
    from config import CONFIG
    CONFIG_AVAILABLE = True
except ImportError:
    CONFIG_AVAILABLE = False
    # Значения по умолчанию
    CONFIG = {
        'logging': {
            'level': logging.INFO,
            'console_level': logging.INFO,
            'file_level': logging.DEBUG,
            'max_file_size_mb': 10,
            'backup_count': 5,
            'daily_backup_count': 30,
            'error_file_size_mb': 5,
            'error_backup_count': 3
        }
    }

class ColoredFormatter(logging.Formatter):
    """Форматтер с цветным выводом для консоли"""
    
    COLORS = {
        'DEBUG': '\033[36m',      # Cyan
        'INFO': '\033[32m',       # Green
        'WARNING': '\033[33m',    # Yellow
        'ERROR': '\033[31m',      # Red
        'CRITICAL': '\033[35m',   # Magenta
    }
    RESET = '\033[0m'
    
    def format(self, record):
        # Добавляем цвет к уровню логирования
        if record.levelname in self.COLORS:
            record.levelname = f"{self.COLORS[record.levelname]}{record.levelname}{self.RESET}"
        
        # Добавляем информацию о процессе и потоке
        if hasattr(record, 'processName'):
            record.process_info = f"[{record.processName}:{record.threadName}]"
        else:
            record.process_info = f"[{record.processName}:{record.threadName}]"
        
        return super().format(record)

class PrintLogger:
    """Простой логгер, печатающий сообщения через print."""
    def __init__(self, name: str = 'WPNCollector') -> None:
        self.name = name
    
    def _now(self) -> str:
        return time.strftime('%H:%M:%S')
    
    def _emit(self, level: str, message: str) -> None:
        print(f"{self._now()} | {level:<8} | {self.name} | {message}")
    
    def debug(self, message: str, *args, **kwargs) -> None:
        self._emit('DEBUG', str(message))
    
    def info(self, message: str, *args, **kwargs) -> None:
        self._emit('INFO', str(message))
    
    def warning(self, message: str, *args, **kwargs) -> None:
        self._emit('WARNING', str(message))
    
    def error(self, message: str, *args, **kwargs) -> None:
        self._emit('ERROR', str(message))
    
    def critical(self, message: str, *args, **kwargs) -> None:
        self._emit('CRITICAL', str(message))
    
    def exception(self, message: str, *args, **kwargs) -> None:
        # Совместимость с logging.exception
        self._emit('ERROR', str(message))

# Оставляем setup_logger для совместимости, но он больше не используется при получении логгера

def setup_logger(name='WPNCollector', log_level=None):
    """
    Настройка логгера с файловым и консольным выводом
    
    Args:
        name: Имя логгера
        log_level: Уровень логирования (если None, берется из конфига)
    
    Returns:
        Настроенный логгер
    """
    # Получаем настройки логирования из конфига
    if CONFIG_AVAILABLE:
        log_config = CONFIG.get('logging', {})
    else:
        log_config = CONFIG['logging']
    
    if log_level is None:
        log_level = log_config.get('level', logging.INFO)
    
    console_level = log_config.get('console_level', logging.INFO)
    file_level = log_config.get('file_level', logging.DEBUG)
    max_file_size_mb = log_config.get('max_file_size_mb', 10)
    backup_count = log_config.get('backup_count', 5)
    daily_backup_count = log_config.get('daily_backup_count', 30)
    error_file_size_mb = log_config.get('error_file_size_mb', 5)
    error_backup_count = log_config.get('error_backup_count', 3)
    
    # Создаем директорию для логов если её нет
    log_dir = Path('logs')
    log_dir.mkdir(exist_ok=True)
    
    # Создаем логгер
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    
    # Очищаем существующие обработчики
    logger.handlers.clear()
    
    # Форматы для разных типов вывода
    file_formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(process_info)s | %(name)s | %(funcName)s:%(lineno)d | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    console_formatter = ColoredFormatter(
        '%(asctime)s | %(levelname)-8s | %(process_info)s | %(name)s | %(funcName)s:%(lineno)d | %(message)s',
        datefmt='%H:%M:%S'
    )
    
    # Обработчик для консоли
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(console_level)
    console_handler.setFormatter(console_formatter)
    
    # Обработчик для файла с ротацией (по размеру и времени)
    file_handler = logging.handlers.RotatingFileHandler(
        log_dir / f'{name}.log',
        maxBytes=max_file_size_mb * 1024 * 1024,  # Конвертируем МБ в байты
        backupCount=backup_count,
        encoding='utf-8'
    )
    file_handler.setLevel(file_level)
    file_handler.setFormatter(file_formatter)
    
    # Обработчик для файла с ротацией по дням
    daily_handler = logging.handlers.TimedRotatingFileHandler(
        log_dir / f'{name}_daily.log',
        when='midnight',
        interval=1,
        backupCount=daily_backup_count,
        encoding='utf-8'
    )
    daily_handler.setLevel(file_level)
    daily_handler.setFormatter(file_formatter)
    
    # Обработчик для ошибок (только ERROR и выше)
    error_handler = logging.handlers.RotatingFileHandler(
        log_dir / f'{name}_errors.log',
        maxBytes=error_file_size_mb * 1024 * 1024,  # Конвертируем МБ в байты
        backupCount=error_backup_count,
        encoding='utf-8'
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(file_formatter)
    
    # Добавляем обработчики к логгеру
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    logger.addHandler(daily_handler)
    logger.addHandler(error_handler)
    
    return logger


def get_logger(name='WPNCollector'):
    """
    Получить настроенный логгер
    
    Args:
        name: Имя логгера
        
    Returns:
        Простой логгер на print
    """
    return PrintLogger(name)

# Создаем основной логгер при запуске модуля
main_logger = get_logger()

if __name__ == '__main__':
    # Тестируем логирование
    logger = get_logger()
    logger.debug('Это отладочное сообщение')
    logger.info('Это информационное сообщение')
    logger.warning('Это предупреждение')
    logger.error('Это ошибка')
    logger.critical('Это критическая ошибка') 
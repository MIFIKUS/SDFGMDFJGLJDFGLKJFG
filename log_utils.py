import functools
import time
import traceback
from logger import get_logger

def log_function_call(logger_name='WPNCollector'):
    """
    Декоратор для логирования вызовов функций
    
    Args:
        logger_name: Имя логгера для использования
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logger = get_logger(logger_name)
            
            # Логируем вход в функцию
            func_name = func.__name__
            logger.debug(f"Вызов функции: {func_name}")
            logger.debug(f"Аргументы: args={args}, kwargs={kwargs}")
            
            start_time = time.time()
            
            try:
                result = func(*args, **kwargs)
                execution_time = time.time() - start_time
                
                # Логируем успешное выполнение
                logger.debug(f"Функция {func_name} выполнена за {execution_time:.3f} сек")
                
                return result
                
            except Exception as e:
                execution_time = time.time() - start_time
                
                # Логируем ошибку
                logger.error(f"Ошибка в функции {func_name} после {execution_time:.3f} сек: {e}")
                logger.error(f"Traceback: {traceback.format_exc()}")
                
                raise
                
        return wrapper
    return decorator

def log_execution_time(logger_name='WPNCollector', level='DEBUG'):
    """
    Декоратор для логирования времени выполнения функций
    
    Args:
        logger_name: Имя логгера для использования
        level: Уровень логирования ('DEBUG', 'INFO', 'WARNING')
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logger = get_logger(logger_name)
            
            start_time = time.time()
            result = func(*args, **kwargs)
            execution_time = time.time() - start_time
            
            # Логируем время выполнения
            message = f"Функция {func.__name__} выполнена за {execution_time:.3f} сек"
            
            if level.upper() == 'DEBUG':
                logger.debug(message)
            elif level.upper() == 'INFO':
                logger.info(message)
            elif level.upper() == 'WARNING':
                logger.warning(message)
            
            return result
        return wrapper
    return decorator

class LogContext:
    """
    Контекстный менеджер для логирования блоков кода
    """
    
    def __init__(self, description, logger_name='WPNCollector', level='INFO'):
        self.description = description
        self.logger = get_logger(logger_name)
        self.level = level.upper()
        self.start_time = None
        
    def __enter__(self):
        self.start_time = time.time()
        
        message = f"Начало: {self.description}"
        if self.level == 'DEBUG':
            self.logger.debug(message)
        elif self.level == 'INFO':
            self.logger.info(message)
        elif self.level == 'WARNING':
            self.logger.warning(message)
            
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        execution_time = time.time() - self.start_time
        
        if exc_type is None:
            # Успешное выполнение
            message = f"Завершено: {self.description} за {execution_time:.3f} сек"
        else:
            # Произошла ошибка
            message = f"Ошибка в: {self.description} после {execution_time:.3f} сек"
            self.logger.error(f"Исключение: {exc_type.__name__}: {exc_val}")
            if exc_tb:
                self.logger.error(f"Traceback: {traceback.format_exc()}")
        
        if self.level == 'DEBUG':
            self.logger.debug(message)
        elif self.level == 'INFO':
            self.logger.info(message)
        elif self.level == 'WARNING':
            self.logger.warning(message)

def log_performance(func):
    """
    Декоратор для логирования производительности функций
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger = get_logger()
        
        start_time = time.time()
        start_memory = None
        
        try:
            # Попытка получить информацию о памяти (если доступно)
            try:
                import psutil
                process = psutil.Process()
                start_memory = process.memory_info().rss / 1024 / 1024  # МБ
            except ImportError:
                pass
            
            result = func(*args, **kwargs)
            
            execution_time = time.time() - start_time
            
            if start_memory is not None:
                end_memory = process.memory_info().rss / 1024 / 1024
                memory_diff = end_memory - start_memory
                logger.info(f"Функция {func.__name__}: время={execution_time:.3f}с, память={memory_diff:+.1f}МБ")
            else:
                logger.info(f"Функция {func.__name__}: время={execution_time:.3f}с")
            
            return result
            
        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(f"Ошибка в {func.__name__} после {execution_time:.3f}с: {e}")
            raise
            
    return wrapper

# Примеры использования:
if __name__ == '__main__':
    logger = get_logger('TestLogger')
    
    # Тест декоратора логирования вызовов
    @log_function_call('TestLogger')
    def test_function(x, y):
        time.sleep(0.1)
        return x + y
    
    # Тест декоратора времени выполнения
    @log_execution_time('TestLogger', 'INFO')
    def slow_function():
        time.sleep(0.2)
        return "done"
    
    # Тест контекстного менеджера
    with LogContext("Тестовый блок кода", 'TestLogger', 'INFO'):
        time.sleep(0.1)
        logger.info("Выполняется код внутри блока")
    
    # Тест производительности
    @log_performance
    def memory_intensive():
        data = [i for i in range(100000)]
        time.sleep(0.1)
        return len(data)
    
    # Запускаем тесты
    test_function(1, 2)
    slow_function()
    memory_intensive() 
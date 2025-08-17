#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Тестовый файл для проверки системы логирования
"""

from logger import get_logger
import time
import traceback

def test_basic_logging():
    """Тест базового логирования"""
    logger = get_logger('TestBasic')
    
    logger.info("=" * 50)
    logger.info("ТЕСТ БАЗОВОГО ЛОГИРОВАНИЯ")
    logger.info("=" * 50)
    
    logger.debug("Это отладочное сообщение")
    logger.info("Это информационное сообщение")
    logger.warning("Это предупреждение")
    logger.error("Это ошибка")
    logger.critical("Это критическая ошибка")
    
    logger.info("Базовое логирование завершено")

def test_function_logging():
    """Тест логирования функций"""
    logger = get_logger('TestFunctions')
    
    logger.info("=" * 50)
    logger.info("ТЕСТ ЛОГИРОВАНИЯ ФУНКЦИЙ")
    logger.info("=" * 50)
    
    def simple_function(x, y):
        logger.debug(f"Выполняется функция simple_function с параметрами x={x}, y={y}")
        result = x + y
        logger.debug(f"Функция simple_function вернула результат: {result}")
        return result
    
    def function_with_error():
        logger.debug("Выполняется функция function_with_error")
        try:
            # Имитируем ошибку
            result = 1 / 0
        except Exception as e:
            logger.error(f"Ошибка в function_with_error: {e}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            raise
    
    # Тестируем функции
    try:
        result = simple_function(5, 3)
        logger.info(f"simple_function(5, 3) = {result}")
        
        function_with_error()
    except Exception as e:
        logger.info(f"Ожидаемая ошибка поймана: {e}")
    
    logger.info("Тест логирования функций завершен")

def test_performance_logging():
    """Тест логирования производительности"""
    logger = get_logger('TestPerformance')
    
    logger.info("=" * 50)
    logger.info("ТЕСТ ЛОГИРОВАНИЯ ПРОИЗВОДИТЕЛЬНОСТИ")
    logger.info("=" * 50)
    
    def slow_operation():
        logger.debug("Начинаем медленную операцию")
        start_time = time.time()
        
        # Имитируем работу
        time.sleep(0.5)
        
        execution_time = time.time() - start_time
        logger.info(f"Медленная операция завершена за {execution_time:.3f} секунд")
        return "Операция выполнена"
    
    def memory_intensive_operation():
        logger.debug("Начинаем операцию с большим объемом данных")
        start_time = time.time()
        
        # Создаем большой список
        data = [i for i in range(100000)]
        result = sum(data)
        
        execution_time = time.time() - start_time
        logger.info(f"Операция с данными завершена за {execution_time:.3f} секунд, результат: {result}")
        return result
    
    # Тестируем операции
    slow_operation()
    memory_intensive_operation()
    
    logger.info("Тест производительности завершен")

def test_error_handling():
    """Тест обработки ошибок"""
    logger = get_logger('TestErrors')
    
    logger.info("=" * 50)
    logger.info("ТЕСТ ОБРАБОТКИ ОШИБОК")
    logger.info("=" * 50)
    
    try:
        # Имитируем различные типы ошибок
        logger.debug("Тестируем деление на ноль")
        result = 1 / 0
    except ZeroDivisionError as e:
        logger.error(f"Поймана ошибка деления на ноль: {e}")
        logger.debug("Это ожидаемая ошибка для тестирования")
    
    try:
        logger.debug("Тестируем обращение к несуществующему атрибуту")
        obj = object()
        obj.nonexistent_attribute
    except AttributeError as e:
        logger.error(f"Поймана ошибка атрибута: {e}")
        logger.debug("Это ожидаемая ошибка для тестирования")
    
    try:
        logger.debug("Тестируем обращение к несуществующему индексу")
        lst = [1, 2, 3]
        lst[10]
    except IndexError as e:
        logger.error(f"Поймана ошибка индекса: {e}")
        logger.debug("Это ожидаемая ошибка для тестирования")
    
    logger.info("Тест обработки ошибок завершен")

def main():
    """Основная функция тестирования"""
    main_logger = get_logger('MainTest')
    
    main_logger.info("ЗАПУСК ТЕСТИРОВАНИЯ СИСТЕМЫ ЛОГИРОВАНИЯ")
    main_logger.info(f"Время запуска: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # Запускаем все тесты
        test_basic_logging()
        time.sleep(0.1)  # Небольшая пауза между тестами
        
        test_function_logging()
        time.sleep(0.1)
        
        test_performance_logging()
        time.sleep(0.1)
        
        test_error_handling()
        
        main_logger.info("=" * 50)
        main_logger.info("ВСЕ ТЕСТЫ УСПЕШНО ЗАВЕРШЕНЫ")
        main_logger.info("=" * 50)
        
    except Exception as e:
        main_logger.critical(f"Критическая ошибка во время тестирования: {e}")
        main_logger.critical(f"Traceback: {traceback.format_exc()}")
        return 1
    
    return 0

if __name__ == '__main__':
    exit_code = main()
    print(f"\nТестирование завершено с кодом выхода: {exit_code}")
    print("Проверьте файлы в директории 'logs/' для просмотра логов") 
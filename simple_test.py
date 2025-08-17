#!/usr/bin/env python3
# -*- coding: utf-8 -*-

print("Начинаем тест логирования...")

try:
    from logger import get_logger
    print("Модуль logger успешно импортирован")
    
    # Создаем логгер
    logger = get_logger('SimpleTest')
    print("Логгер создан")
    
    # Тестируем логирование
    logger.info("Тест информационного сообщения")
    logger.warning("Тест предупреждения")
    logger.error("Тест ошибки")
    
    print("Логирование завершено успешно")
    print("Проверьте файлы в директории 'logs/'")
    
except Exception as e:
    print(f"Ошибка: {e}")
    import traceback
    traceback.print_exc() 
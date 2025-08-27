#!/usr/bin/env python3
# -*- coding: utf-8 -*-

print("Тестирование импортов...")

try:
    print("1. Импорт open_tables_module...")
    from InLobby.Collect import open_tables_module
    print("✓ open_tables_module импортирован успешно")
    
    print("2. Импорт main_lobby...")
    from InLobby.Collect.main_lobby import main_lobby
    print("✓ main_lobby импортирован успешно")
    
    print("3. Импорт tournament_lobby...")
    from InLobby.Collect.tournament_lobby import tournament_lobby
    print("✓ tournament_lobby импортирован успешно")
    
    print("\nВсе импорты работают корректно! Циклический импорт исправлен.")
    
except Exception as e:
    print(f"❌ Ошибка импорта: {e}")
    import traceback
    traceback.print_exc() 
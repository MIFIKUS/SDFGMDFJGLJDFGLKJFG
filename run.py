from InLobby.Collect import open_tables_module
from InLobby.Close import close_tables_module
from Google import load_to_disk

import multiprocessing
import sys
import traceback

if __name__ == '__main__':
    try:
        print("Запуск приложения WPNCollector")
        print(f"Версия Python: {sys.version}")
        print(f"Платформа: {sys.platform}")
        
        multiprocessing.freeze_support()    
        print("Поддержка многопроцессорности включена")

        # Создаем процессы
        open_tables_thread = multiprocessing.Process(
            target=open_tables_module.run,
            name="OpenTables"
        )
        close_tables_thread = multiprocessing.Process(
            target=close_tables_module.run,
            name="CloseTables"
        )
        close_bugged_lobbies_thread = multiprocessing.Process(
            target=close_tables_module.close_bugged_lobbies,
            name="CloseBuggedLobbies"
        )
        google_drive_thread = multiprocessing.Process(
            target=load_to_disk.load_to_disk_module,
            name="GoogleDrive"
        )

        print("Процессы созданы, запускаем...")

        # Запускаем процессы
        open_tables_thread.start()
        print(f"Процесс OpenTables запущен (PID: {open_tables_thread.pid})")
        
        close_tables_thread.start()
        print(f"Процесс CloseTables запущен (PID: {close_tables_thread.pid})")
        
        close_bugged_lobbies_thread.start()
        print(f"Процесс CloseBuggedLobbies запущен (PID: {close_bugged_lobbies_thread.pid})")
        
        google_drive_thread.start()
        print(f"Процесс GoogleDrive запущен (PID: {google_drive_thread.pid})")

        print("Все основные процессы запущены успешно")
        
        # Ждем завершения процессов
        try:
            open_tables_thread.join()
            print("Процесс OpenTables завершен")
        except KeyboardInterrupt:
            print("Получен сигнал прерывания для OpenTables")
            
        try:
            close_tables_thread.join()
            print("Процесс CloseTables завершен")
        except KeyboardInterrupt:
            print("Получен сигнал прерывания для CloseTables")
            
        try:
            close_bugged_lobbies_thread.join()
            print("Процесс CloseBuggedLobbies завершен")
        except KeyboardInterrupt:
            print("Получен сигнал прерывания для CloseBuggedLobbies")
            
        #if google_drive_thread.is_alive():
        #    google_drive_thread.terminate()
        #    print("Процесс GoogleDrive остановлен")

        print("Приложение завершено")
        
    except Exception as e:
        print(f"Критическая ошибка в основном процессе: {e}")
        print(f"Traceback: {traceback.format_exc()}")
        sys.exit(1)



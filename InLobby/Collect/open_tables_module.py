from InLobby.Collect.main_lobby import main_lobby
from InLobby.Collect.tournament_lobby import tournament_lobby
from InLobby.Extensions.proceses.tables import get_amount_of_opened_tables
from InLobby.Collect.tournament_lobby.extensions.win_actions import lobby_loaded, close_exit_from_lobby_window
from logger import get_logger
import time
import traceback

# Получаем логгер для модуля открытия таблиц
logger = get_logger('OpenTables')

AMOUNT_OF_TABLES = 20

logger.info(f"Модуль открытия таблиц инициализирован. Максимальное количество таблиц: {AMOUNT_OF_TABLES}")

main_lobby_window = main_lobby.get_main_lobby()
logger.info("Главное окно лобби получено")

def run():
    logger.info("Запуск процесса открытия таблиц")
    
    while True:
        try:
            current_tables = get_amount_of_opened_tables()
            logger.debug(f"Текущее количество открытых таблиц: {current_tables}")
            
            if current_tables >= AMOUNT_OF_TABLES:
                logger.debug(f"Достигнут лимит таблиц ({AMOUNT_OF_TABLES}), ожидание...")
                time.sleep(10)
                continue
                
            logger.info(f"Начинаем поиск турниров для открытия таблиц. Доступно мест: {AMOUNT_OF_TABLES - current_tables}")
            
            tournaments, tournaments_raw = main_lobby.get_list_of_tournaments(main_lobby_window)
            logger.info(f"Найдено турниров: {len(tournaments)}")

            for i, (tournament, tournament_raw) in enumerate(zip(tournaments, tournaments_raw)):
                try:
                    current_tables = get_amount_of_opened_tables()
                    if current_tables >= AMOUNT_OF_TABLES:
                        logger.info(f"Достигнут лимит таблиц ({AMOUNT_OF_TABLES}), останавливаем поиск")
                        break
                        
                    logger.info(f"Обрабатываем турнир {i+1}/{len(tournaments)}: {tournament}")
                    
                    time.sleep(0.5)
                    main_lobby_window.set_focus()
                    close_exit_from_lobby_window(main_lobby_window)
                    logger.debug("Фокус установлен на главное окно лобби")

                    tournament_status = main_lobby.get_tournament_status(tournament_raw)
                    logger.debug(f"Статус турнира: {tournament_status}")

                    try:
                        logger.info(f"Переключаемся на турнир: {tournament}")
                        main_lobby.switch_tournament(tournament)
                        logger.debug("Переключение на турнир выполнено")
                        
                        logger.info(f"Открываем турнир: {tournament}")
                        main_lobby.open_tournament(tournament)
                        logger.info(f"Турнир {tournament} открыт успешно")
                        
                    except Exception as e:
                        logger.error(f"Ошибка при работе с турниром {tournament}: {e}")
                        logger.error(f"Traceback: {traceback.format_exc()}")
                        continue

                    logger.info(f"Ожидание загрузки турнира {tournament} (15 секунд)")
                    time.sleep(15)

                    tournament_lobby_window = tournament_lobby._get_lobby_window()
                    logger.debug("Окно лобби турнира получено")

                    logger.info(f"Открываем таблицы для турнира {tournament} со статусом {tournament_status}")
                    tournament_lobby.open_tables(tournament_status)
                    logger.info(f"Таблицы для турнира {tournament} открыты")

                    tournament_lobby_window.close()
                    logger.debug(f"Окно лобби турнира {tournament} закрыто")
                    
                    current_tables = get_amount_of_opened_tables()
                    logger.info(f"Турнир {tournament} обработан. Текущее количество таблиц: {current_tables}")

                except Exception as e:
                    logger.error(f"Ошибка при обработке турнира {tournament}: {e}")
                    logger.error(f"Traceback: {traceback.format_exc()}")
                    continue

            logger.info("Все доступные турниры обработаны, ожидание 10 секунд перед следующим циклом")
            time.sleep(10)
            
        except Exception as e:
            logger.error(f"Критическая ошибка в основном цикле открытия таблиц: {e}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            logger.info("Ожидание 30 секунд перед повторной попыткой")
            time.sleep(30)
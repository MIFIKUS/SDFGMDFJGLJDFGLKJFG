from InLobby.Collect.main_lobby import main_lobby
from InLobby.Collect.tournament_lobby import tournament_lobby
from InLobby.Extensions.proceses.tables import get_amount_of_opened_tables
import time


AMOUNT_OF_TABLES = 20


main_lobby_window = main_lobby.get_main_lobby()

def run():
    while True:
        if get_amount_of_opened_tables() >= AMOUNT_OF_TABLES:
            continue
        tournaments, tournaments_raw = main_lobby.get_list_of_tournaments(main_lobby_window)

        for tournament, tournament_raw in zip(tournaments, tournaments_raw):
            if get_amount_of_opened_tables() >= AMOUNT_OF_TABLES:
                continue
            time.sleep(0.5)
            main_lobby_window.set_focus()

            tournament_status = main_lobby.get_tournament_status(tournament_raw)

            main_lobby.switch_tournament(tournament)
            main_lobby.open_tournament(tournament)

            time.sleep(10)

            tournament_lobby_window = tournament_lobby._get_lobby_window()

            tournament_lobby.open_tables(tournament_status)

            tournament_lobby_window.close()


        time.sleep(10)
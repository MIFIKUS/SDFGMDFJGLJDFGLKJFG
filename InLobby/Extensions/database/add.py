from InLobby.Extensions.database.general import get_cursor
from config import CONFIG

def add_tournament_info(tournament_id: str, name: str, status: str):
    cursor = get_cursor()

    query = f"INSERT INTO wpn.opened_tournaments (tournament_id, name, status, date) VALUES ('{tournament_id}', '{name}', '{status}', NOW());"

    cursor.execute(query)


def add_table_info(tournament_id: str, name: str, table_num: str, status: str):
    cursor = get_cursor()

    query = f"INSERT INTO wpn.opened_tables (tournament_id, name, table_num, status, script_name, date) VALUES ('{tournament_id}', '{name}', '{table_num}', '{status}', '{CONFIG['script_name']}', NOW());"

    cursor.execute(query)

    
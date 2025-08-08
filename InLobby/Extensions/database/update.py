from InLobby.Extensions.database.general import get_cursor


def update_tournament_status(tournament_id: str, status: str):
    cursor = get_cursor()

    query = f"UPDATE wpn.opened_tournaments SET status = '{status}' WHERE tournament_id = '{tournament_id}'"

    cursor.execute(query)


def update_table_status(tournament_id: str, table_num: str, status: str):
    cursor = get_cursor()

    query = f"UPDATE wpn.opened_tables SET status = '{status}' WHERE tournament_id = '{tournament_id}' AND table_num = '{table_num}'"

    cursor.execute(query)


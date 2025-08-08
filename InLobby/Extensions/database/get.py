from InLobby.Extensions.database.general import get_cursor


def get_tournament_status(tournament_id: str) -> str:
    cursor = get_cursor()

    query = f"SELECT status FROM wpn.opened_tournaments where tournament_id = '{tournament_id}'"

    cursor.execute(query)

    result = cursor.fetchone()

    if result:
        return result[0]
    return None


def get_table_status(tournament_id: str, table_num: str) -> str:
    cursor = get_cursor()

    query = f"SELECT status FROM wpn.opened_tables where tournament_id = '{tournament_id}' and table_num = '{table_num}'"

    cursor.execute(query)

    result = cursor.fetchone()

    if result:
        return result[0]
    return None


import mysql.connector

# --- глобальные переменные ---
_conn = None
_cursor = None

def get_cursor():
    """
    Возвращает один и тот же курсор на протяжении жизни процесса.
    При первом вызове открывает соединение и создаёт курсор.
    """
    global _conn, _cursor
    if _conn is None or not _conn.is_connected():
        # настраиваем соединение один раз
        _conn = mysql.connector.connect(
            host="147.78.67.17",
            user="poker",
            password="root",
            autocommit=True         # или False, если нужен ручной commit
        )
        _cursor = _conn.cursor(buffered=True)

    return _cursor


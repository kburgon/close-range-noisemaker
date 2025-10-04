import sqlite3
from datetime import datetime

def ensureCreated(conn: sqlite3.Connection) -> None:
    creation_query = """
    CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        event TEXT,
        distance INTEGER
    );
    """

    cursor = conn.cursor()
    cursor.execute(creation_query)
    conn.commit()

def log_event(event: str, distance: int, dbName: str = ":memory:") -> None:
    try:
        insertQuery = '''
            INSERT INTO events (timestamp, event, distance)
            VALUES (?, ?, ?)
        '''
        timestamp = datetime.now().isoformat(timespec='milliseconds')
        params = (timestamp, event, distance)
        print(timestamp + ': ' + event)

        with sqlite3.connect(dbName) as conn:
            ensureCreated(conn)
            cur = conn.cursor()
            cur.execute(insertQuery, params)
            conn.commit()

    except sqlite3.Error as ex:
        print(ex)

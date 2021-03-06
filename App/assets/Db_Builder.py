import sqlite3 as sql

conn = sql.connect('data_base.db')


def build(test=True):  # If you need a new database
    conn.execute("""CREATE TABLE IF NOT EXISTS config (
            alarm BOOL NOT NULL,
            delay FLOAT NOT NULL)""")
    conn.execute("INSERT INTO config (alarm, delay) \
          Values (False, 0.5)")
    conn.commit() if not test else None


print([row for row in conn.execute('SELECT delay FROM config')][0][0])

import sqlite3 as sql

conn = sql.connect('data_base')


def build(test=True):
    conn.execute("""CREATE TABLE IF NOT EXISTS config (
            alarm BOOL NOT NULL,
            delay FLOAT NOT NULL)""")
    conn.execute("INSERT INTO config (alarm, delay) \
          Values (False, 0)")
    conn.commit() if not test else None


def update_db(alarm=False, delay=0):
    conn.execute(f'UPDATE config SET alarm = {alarm}, delay = {delay}')


build()
update(True, 5)
config = conn.execute('SELECT alarm, delay FROM config')
[print(row) for row in config]

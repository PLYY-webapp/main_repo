import sqlite3

DB = '../Gen/db/plyy.db'

def connect_db():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    return conn, cur


def get_query(query, params=None, sum=None):
    conn, cur = connect_db()

    if params:
        cur.execute(query, params)
    else:
        cur.execute(query)
        
    if sum == 'one':
        result = cur.fetchone()
    else:
        result = cur.fetchall()

    conn.close()

    return result


def execute_query(query, params):
    conn, cur = connect_db()
    cur.execute(query, params)
    conn.commit()
    conn.close

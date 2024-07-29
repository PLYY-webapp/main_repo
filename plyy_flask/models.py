# models.py
from uuid import uuid4
import sqlite3
import os

def connect_db():
    database_path = os.path.join(os.path.dirname(__file__), 'plyy.db')
    conn = sqlite3.connect(database_path)
    conn.execute('PRAGMA foreign_keys = ON')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    return conn, cur

def curator_info(id):
    curator_info = []
    curator_tags = []
    conn, cur = connect_db()

    cur.execute('SELECT * FROM CURATOR WHERE c_uuid = ?', (id,))
    curator = cur.fetchone()
    curator_info.extend([curator[i] for i in range(len(curator))])
    
    cur.execute('''
                SELECT TAG.tag_name
                FROM CURATOR
                JOIN TAG_CURATOR ON CURATOR.c_uuid = TAG_CURATOR.c_uuid
                JOIN TAG ON TAG_CURATOR.tag_uuid = TAG.tag_uuid
                WHERE CURATOR.c_uuid = ?
                ''', (id,))
    
    ctags = cur.fetchall()
    conn.close()

    curator_tags.extend([ctags[i]['tag_name'] for i in range(len(ctags))])
    curator_info.append(curator_tags)
    return curator_info

def cu_plyy_tag(id, pid):
    plyy_tags = []
    conn, cur = connect_db()
    
    cur.execute('''
                SELECT TAG_GENRE.gtag_name
                FROM TAG_GENRE
                JOIN PLYY ON PLYY.gtag_uuid = TAG_GENRE.gtag_uuid
                WHERE PLYY.c_uuid = ? and PLYY.plyy_uuid = ?
                ''', (id, pid))
    
    cu_pgtag = cur.fetchall()
    for pgtag in cu_pgtag:
        plyy_tags.append(pgtag['gtag_name'])

    cur.execute('''    
            SELECT tag.tag_name
            FROM PLYY
            JOIN TAG_PLYY ON PLYY.plyy_uuid = TAG_PLYY.plyy_uuid
            JOIN TAG ON TAG_PLYY.tag_uuid = TAG.tag_uuid
            WHERE PLYY.c_uuid = ? and PLYY.plyy_uuid = ?''', (id, pid))
    
    cu_ptag = cur.fetchall()
    conn.close()

    for t in cu_ptag:
        plyy_tags.append(t['tag_name'])
    return plyy_tags

def cu_plyy(id):
    plyy_list = []
    conn, cur = connect_db()

    cur.execute('SELECT * FROM PLYY WHERE c_uuid = ?', (id,))
    plyy = cur.fetchall()
    conn.close()

    for p in plyy:  # 플리 객체
        each_plyy = [p[i] for i in range(len(p))]
        each_plyy.append(cu_plyy_tag(id, each_plyy[0]))
        plyy_list.append(each_plyy)
    return plyy_list

def curatorlike_status(c_uuid, u_uuid):
    conn, cur = connect_db()
    cur.execute('SELECT * FROM CURATOR_LIKE WHERE c_uuid = ? and u_uuid = ?', (c_uuid, u_uuid))
    likes = cur.fetchone()
    conn.close()
    return bool(likes)

def curator_like(c_uuid, u_uuid):
    conn, cur = connect_db()
    cl_uuid = str(uuid4())
    try:
        cur.execute('SELECT * FROM CURATOR_LIKE WHERE u_uuid = ? AND c_uuid = ?', (u_uuid, c_uuid))
        row = cur.fetchone()
        if not row:
            cur.execute('INSERT INTO CURATOR_LIKE (cl_uuid, u_uuid, c_uuid) VALUES (?, ?, ?)', (cl_uuid, u_uuid, c_uuid))
            conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error inserting like: {e}")
        conn.rollback()
        conn.close()
        return False

def curator_unlike(c_uuid, u_uuid):
    conn, cur = connect_db()
    try:
        cur.execute('SELECT * FROM CURATOR_LIKE WHERE u_uuid = ? AND c_uuid = ?', (u_uuid, c_uuid))
        row = cur.fetchone()
        if row:
            cur.execute('DELETE FROM CURATOR_LIKE WHERE u_uuid = ? AND c_uuid = ?', (u_uuid, c_uuid))
            conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error deleting like: {e}")
        conn.rollback()
        conn.close()
        return False

def plyylike_status(pidlist, u_uuid):
    conn, cur = connect_db()
    plikestatus = []
    for pid in pidlist:
        cur.execute('SELECT * FROM PLYY_LIKE WHERE plyy_uuid = ? and u_uuid = ?', (pid, u_uuid))
        likes = cur.fetchone()
        plikestatus.append(bool(likes))
    conn.close()
    return dict(zip(pidlist, plikestatus))

def plyy_like(plyy_uuid, u_uuid):
    conn, cur = connect_db()
    pl_uuid = str(uuid4())
    try:
        cur.execute('SELECT * FROM PLYY_LIKE WHERE u_uuid = ? AND plyy_uuid = ?', (u_uuid, plyy_uuid))
        row = cur.fetchone()
        if not row:
            cur.execute('INSERT INTO PLYY_LIKE (pl_uuid, u_uuid, plyy_uuid) VALUES (?, ?, ?)', (pl_uuid, u_uuid, plyy_uuid))
            conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error inserting like: {e}")
        conn.rollback()
        conn.close()
        return False

def plyy_unlike(plyy_uuid, u_uuid):
    conn, cur = connect_db()
    try:
        cur.execute('SELECT * FROM PLYY_LIKE WHERE u_uuid = ? AND plyy_uuid = ?', (u_uuid, plyy_uuid))
        row = cur.fetchone()
        if row:
            cur.execute('DELETE FROM PLYY_LIKE WHERE u_uuid = ? AND plyy_uuid = ?', (u_uuid, plyy_uuid))
            conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error deleting like: {e}")
        conn.rollback()
        conn.close()
        return False

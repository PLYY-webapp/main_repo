def extract_user_uuid(u_email):
    from models import connect_db
    conn, cur = connect_db()
    cur.execute('SELECT u_uuid FROM USER WHERE u_email = ?', (u_email,))
    u_uuid = cur.fetchone()
    conn.close()
    return u_uuid['u_uuid'] if u_uuid else None

import sqlite3

def connect_db():
    conn = sqlite3.connect('plyy.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    return conn, cur

def fetch():
			# * 플리 제목 <-- PLYY.plyy_title
			# * 큐레이터 이름 <-- CURATOR.c_name
			# * 플리에 담긴 총 곡수 (0곡) <-- SONG.song_uuid
			# * 총 플리 런타임 (0시간 0분) <-- SRC_src_rtime

            # 내 plyy_uuid : plyy_ab9cf7fc-0319-4098-a9ca-6b0caee858d0
            # 내 c_uuid : c_a1d1e40b-5867-47eb-aac6-fbc1a2acbdc4

            # Chill
            # 효림님 plyy_uuid : plyy_2f01c5df-fac1-499e-9cfd-4ce3b540ddfd
            # 효림님 c_uuid : c_2866e59a-fcc3-4ca8-a1ec-681feb9a0c26

            # Bronze
            # 민희님 plyy_uuid : plyy_2a8cc702-67ee-4377-8310-cd9689b98c19
            # 민희님 c_uuid : c_0401890c-3fe2-4142-a74e-e81fee61a7aa

# 서부고용센터 모니터링 : 2077-3493
# SELECT plyy_title, COUNT(song_uuid) FROM PLYY
# 	JOIN SONG ON PLYY.plyy_uuid = SONG.plyy_id
# 	GROUP BY PLYY.plyy_title

    conn, cur = connect_db()
    cur.execute('''
        SELECT plyy_title, c_name, COUNT(song_uuid) as count FROM PLYY
            JOIN CURATOR ON PLYY.c_uuid = CURATOR.c_uuid
            JOIN SONG ON PLYY.plyy_uuid = SONG.plyy_id
            GROUP BY SONG.song_uuid
    ''')
    raw_data = cur.fetchall()
    data = []
    for rd in raw_data:
        data.append(dict(rd))
    conn.close()

    return data


if __name__ == '__main__':
    pass
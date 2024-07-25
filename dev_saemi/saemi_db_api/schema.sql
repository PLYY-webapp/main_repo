-- PLYY 테이블
CREATE TABLE IF NOT EXISTS 'PLYY' (
    'plyy_id' INTEGER PRIMARY KEY AUTOINCREMENT,
    'plyy_title' TEXT NOT NULL,
    'plyy_img' TEXT NOT NULL,
    'plyy_gen_date' DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    'plyy_update_date' DATETIME,
    'plyy_cmt' TEXT NOT NULL,
    'c_id' TEXT NOT NULL,
    'gtag_id' TEXT NOT NULL,
    FOREIGN KEY ('c_id') REFERENCES 'CURATOR.c_id' ON DELETE CASCADE, -- ON DELETE CASCADE 삭제 필요!
    FOREIGN KEY ('gtag_id') REFERENCES 'GENRE.gtag_id'
)

-- SONG 테이블
CREATE TABLE IF NOT EXISTS 'SONG' (
    'song_id' INTEGER PRIMARY KEY AUTOINCREMENT,
    'song_cmt' TEXT,
    'song_vid' TEXT NOT NULL,
    'song_index' INTEGER NOT NULL,
    'plyy_id' INTEGER NOT NULL,
    'track_id' TEXT NOT NULL,
    FOREIGN KEY ('plyy_id') REFERENCES 'PLYY.plyy_id' ON DELETE CASCADE,
    FOREIGN KEY ('track_id') REFERENCES 'TRACK.track_id' ON DELETE CASCADE
)

-- TRACK 테이블
CREATE TABLE IF NOT EXISTS 'TRACK' (
    'track_id' TEXT PRIMARY KEY,
    'track_title' TEXT NOT NULL,
    'track_artist' TEXT NOT NULL,
    'track_album' TEXT NOT NULL,
    'track_album_img' TEXT NOT NULL,
    'track_rtime' INTEGER NOT NULL
)

-- CURATOR 테이블
CREATE TABLE IF NOT EXISTS 'CURATOR' (
    'c_id' INTEGER PRIMARY KEY AUTOINCREMENT,
    'c_name' TEXT NOT NULL UNIQUE,
    'c_img' TEXT NOT NULL,
    'c_intro' TEXT NOT NULL
)

-- USER 테이블
CREATE TABLE IF NOT EXISTS 'USER' (
    'u_id' INTEGER PRIMARY KEY AUTOINCREMENT,
    'u_email' TEXT NOT NULL UNIQUE,
    'u_pw' TEXT NOT NULL,
    'u_nickname' TEXT,
    'u_img' TEXT
)

-- P_LIKE 테이블 : PRIMARY KEY 특이사항 확인해 봐야함
CREATE TABLE IF NOT EXISTS 'P_LIKE' (
    'u_id' INTEGER,
    'plyy_id' INTEGER,
    PRIMARY KEY ('u_id', 'plyy_id'),
    FOREIGN KEY ('u_id') REFERENCES 'USER.u_id' ON DELETE CASCADE,
    FOREIGN KEY ('plyy_id') REFERENCES 'PLYY.plyy_id' ON DELETE CASCADE
)

-- C_LIKE 테이블 : PRIMARY KEY 특이사항 확인해 봐야함
CREATE TABLE IF NOT EXISTS 'C_LIKE' (
    'u_id' INTEGER,
    'c_id' INTEGER,
    PRIMARY KEY ('u_id', 'c_id'),
    FOREIGN KEY ('u_id') REFERENCES 'USER.u_id' ON DELETE CASCADE,
    FOREIGN KEY ('c_id') REFERENCES 'CURATOR.c_id' ON DELETE CASCADE
)

-- TAG 테이블
CREATE TABLE IF NOT EXISTS 'TAG' (
    'tag_id' INTEGER PRIMARY KEY AUTOINCREMENT,
    'tag_name' TEXT NOT NULL
)

-- GENRE 테이블
CREATE TABLE IF NOT EXISTS 'GENRE' (
    'gtag_id' INTEGER PRIMARY KEY AUTOINCREMENT,
    'gtag_name' TEXT NOT NULL
)

-- P_TAG 테이블
CREATE TABLE IF NOT EXISTS 'P_TAG' (
    'tag_id' INTEGER,
    'plyy_id' INTEGER,
    PRIMARY KEY ('tag_id', 'plyy_id'),
    FOREIGN KEY ('tag_id') REFERENCES 'TAG.tag_id' ON DELETE CASCADE,
    FOREIGN KEY ('plyy_id') REFERENCES 'PLYY.plyy_id' ON DELETE CASCADE
)

-- C_TAG 테이블
CREATE TABLE IF NOT EXISTS 'C_TAG' (
    'tag_id' INTEGER,
    'c_id' INTEGER,
    PRIMARY KEY ('tag_id', 'c_id'),
    FOREIGN KEY ('tag_id') REFERENCES 'TAG.tag_id' ON DELETE CASCADE,
    FOREIGN KEY ('c_id') REFERENCES 'CURATOR.c_id' ON DELETE CASCADE
)
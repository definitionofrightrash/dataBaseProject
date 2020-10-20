from sqlite3 import connect
queries = [
     """ CREATE TABLE IF NOT EXISTS USER (
                                    ID INTEGER NOT NULL,
                                    NAME TEXT NOT NULL,
                                    EMAIL TEXT NOT NULL,
                                    LAND TEXT NOT NULL,
                                    HASHED_PASSWORD TEXT NOT NULL,
                                    IMAGE_REFERENCE TEXT NOT NULL,
                                    PRIMARY KEY(EMAIL ,ID)
                                    );""",
    """ CREATE TABLE IF NOT EXISTS ARTIST (
                                    USERNAME TEXT NOT NULL,
                                    HASHED_PASSWORD TEXT NOT NULL,
                                    IS_VERIFIED BOOLEAN NOT NULL,
                                    ABOUT TEXT ,
                                    ID INTEGER ,
                                    PRIMARY KEY(ID,USERNAME) 
                                    ); """ ,
    """ CREATE TABLE IF NOT EXISTS POPULAR(
                                    USERNAME TEXT,
                                    ID INTEGER,
                                    POPULAR TEXT NOT NULL
                                    )""",
    """ CREATE TABLE IF NOT EXISTS ALBUM(
                                    ID INTEGER ,
                                    TITLE TEXT NOT NULL,
                                    RELEASE_YEAR TEXT NOT NULL,
                                    COPYRIGHT TEXT NOT NULL,
                                    IS_SIGLE_OR_EP BOOLEAN NOT NULL,
                                    PRIMARY KEY (ID)
    )""",
    """ CREATE TABLE IF NOT EXISTS MUSIC(
                                    TITLE TEXT NOT NULL,
                                    DURATION INTEGER NOT NULL,
                                    NUMBER_OF_PLAYS INTEGER NOT NULL,
                                    FILE_REFERENCE TEXT NOT NULL,
                                    IS_ACTIVE BOOLEAN NOT NULL,
                                    IS_EXPIRED BOOLEAN NOT NULL,
                                    ID INTEGER ,
                                    COVER_REFERENCE TEXT NOT NULL,
                                    ALBUM_ID INTEGER NOT NULL,
                                    FOREIGN KEY (ALBUM_ID) REFERENCES ALBUM(ID),
                                    PRIMARY KEY(ID)
      )""",
    """ CREATE TABLE IF NOT EXISTS PLAYLIST(
                                    NAME TEXT NOT NULL,
                                    DESCRIPTION TEXT NOT NULL,
                                    IMAGE_REFERENCE TEXT NOT NULL,
                                    ID INTEGER ,
                                    OWNER INTEGER NOT NULL,
                                    PRIMARY KEY (ID),
                                    FOREIGN KEY (OWNER) REFERENCES USER(ID)
                                    
    )""",
    """ CREATE TABLE IF NOT EXISTS ARTIST_FALLOW(
                                    ARTIST_USERNAME TEXT ,
                                    ARTIST_ID INTEGER ,
                                    USER_ID INTEGER ,
                                    USER_EMAIL TEXT ,
                                    PRIMARY KEY(ARTIST_USERNAME,ARTIST_ID,USER_ID,USER_EMAIL)
                                    FOREIGN KEY (ARTIST_USERNAME) REFERENCES ARTIST(USERNAME),
                                    FOREIGN KEY (ARTIST_ID) REFERENCES ARTIST(ID),
                                    FOREIGN KEY (USER_ID) REFERENCES USER(ID),
                                    FOREIGN KEY (USER_EMAIL) REFERENCES USER(EMAIL)
                                    
    
    )""",
    """ CREATE TABLE IF NOT EXISTS USER_FALLOW(
                                    E1 TEXT ,
                                    E2 TEXT ,
                                    ID1 INTEGER ,
                                    ID2 INTEGER ,
                                    FOREIGN KEY (E1) REFERENCES USER(EMAIL),
                                    FOREIGN KEY (E2) REFERENCES USER(EMAIL),
                                    FOREIGN KEY (ID1) REFERENCES USER(ID),
                                    FOREIGN KEY (ID2) REFERENCES USER(ID),
                                    PRIMARY KEY (E1,E2,ID1,ID2)
    )""",
    """ CREATE TABLE IF NOT EXISTS LIKED(
                                    USER_ID INTEGER,
                                    USER_EMAIL TEXT,
                                    MUSIC_ID INTEGER,
                                    DATE TEXT NOT NULL,
                                    FOREIGN KEY (USER_ID) REFERENCES USER(ID),
                                    FOREIGN KEY (USER_EMAIL) REFERENCES USER(EMAIL),
                                    FOREIGN KEY (MUSIC_ID) REFERENCES MUSIC(ID),
                                    PRIMARY KEY(USER_ID,MUSIC_ID) 
    )""",
    """ CREATE TABLE IF NOT EXISTS INTABLE(
                                    ARTIST_ID INTEGER  ,
                                    ARTIST_USERNAME TEXT ,
                                    IS_OWNER BOOLEAN NOT NULL,
                                    ALBUM_ID INTEGER ,
                                    FOREIGN KEY (ARTIST_ID) REFERENCES ARTIST(ID),
                                    FOREIGN KEY (ARTIST_USERNAME) REFERENCES ARTIST(USERNAME),
                                    FOREIGN KEY (ALBUM_ID) REFERENCES ALBUM(ID)
                                    
    )""",
    """ CREATE TABLE IF NOT EXISTS PLAYLIST_FALLOW(
                                    USER_ID INTEGER ,
                                    USER_EMAIL TEXT ,
                                    PLAYLIST_ID INTEGER ,
                                    FOREIGN KEY (USER_ID) REFERENCES USER(ID),
                                    FOREIGN KEY (USER_EMAIL) REFERENCES USER(EMAIL),
                                    FOREIGN KEY (PLAYLIST_ID) REFERENCES PLAYLIST(ID),
                                    PRIMARY KEY(USER_ID,USER_EMAIL,PLAYLIST_ID)
    )""",
    """ CREATE TABLE IF NOT EXISTS ON_PLAYLIST(
                                    MUSIC_ID INTEGER ,
                                    DATE_OF_ADD TEXT NOT NULL,
                                    PLAYLIST_ID INTEGER ,
                                    FOREIGN KEY (MUSIC_ID) REFERENCES MUSIC(ID),
                                    FOREIGN KEY (PLAYLIST_ID) REFERENCES PLAYLIST(ID)
                                    PRIMARY KEY(MUSIC_ID,PLAYLIST_ID)
                                    
    )"""
]
conn = connect('dataBase.db')
cur = conn.cursor()
for query in queries:
    print(query)
    cur.execute(query)
conn.close()
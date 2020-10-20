from os import system
from hashlib import md5
from cryptography.fernet import Fernet
from sqlite3 import connect
from User import User
from Artist import Artist
from PlayList import PlayList
def generate_key():
    key = int(open("secret.key", "r").read())
    with open("secret.key", "w") as key_file:
        key_file.write(str(key+1))
    return key

def queryExecute(query,parameters):
    conn = connect('dataBase.db')
    cur = conn.cursor()
    cur.execute(query,parameters)
    rows = cur.fetchall()
    conn.close()
    return rows

def nqueryExecute(query,parameters):
    conn = connect('dataB   ase.db')
    cur = conn.cursor()
    cur.execute(query,parameters)
    conn.commit()
    conn.close()

def initilizaion():
    system('clear')
    print("1.sign in as user")
    print("2.sign in as artist")
    print("3.sign up as user")
    print("4.sign up as artist")
    choice = input()
    print(choice)
    if choice == '1':
        userSignIn()
    elif choice == '2':
        artistSignIn()
    elif choice == '3':
        userSignUp()
    elif choice == '4':
        artistSignUp()
    else:
        initilizaion()
def userSignIn():
    system('clear')
    email = input('Email: ')
    password = md5(input("Password: ").encode()).hexdigest()
    query = """ 
    SELECT *
    FROM USER
     WHERE EMAIL = ? AND HASHED_PASSWORD = ?
    """
    rows = queryExecute(query,[email,password])
    if not rows:
        userSignIn()
        return
    (id,name,email,land,hashedPassword,imageReference) = rows.pop()
    userDashboard(User(id,name,email,land,hashedPassword,imageReference))
def userSignUp():
    system('clear')
    name = input('Name: ')
    email = input('Email: ')
    land = input('Land: ')
    hashed_password = input('Password: ')
    image_reference = input("image_reference: ")
    query = """
            INSERT INTO USER(ID,NAME,EMAIL,LAND,HASHED_PASSWORD,IMAGE_REFERENCE)
            VALUES (?,?,?,?,?,?)
    """
    id = generate_key()
    nqueryExecute(query,[id,name,email,land,md5(hashed_password.encode()).hexdigest() ,image_reference])
    userDashboard(User(id,name,email,land,hashed_password,image_reference))
def fallowUser(user):
    system('clear')
    query = """
            SELECT ID,EMAIL
            FROM USER
    """
    print("id - email")
    for (id,email) in queryExecute(query,[]):
        print (str(id) + " " + email)
        #enter the id and the name
    id = input("id: ")
    email = input('email: ')
    #fill the user_fallow
    query = """
        INSERT INTO USER_FALLOW(E1,E2,ID1,ID2)
        VALUES(?, ?, ?,?)
    """
    nqueryExecute(query,[user.email,email,user.id,id])
    #back to the Dashboard
    userDashboard(user)

def unfallowUser(user):
    system('clear')
    #list the email and the id of the users we are fallowing
    query = """
        SELECT ID2,E2
        FROM USER_FALLOW
        WHERE ID1 = ? AND E1 = ?
        """
    print("id - email")
    for (id,email) in queryExecute(query,[user.id,user.email]):
        print (str(id) + " " + email)
        #input the one we want to unfallow
    id = input("id: ")
    email = input("email: ")
        #delete it from user_fallow
    query = """
        DELETE FROM USER_FALLOW
        WHERE E1 = ? AND E2 = ? AND ID1 = ? AND ID2 = ?
        """
    nqueryExecute(query,[user.email,email,user.id,id])
        #back to the dashboard
    userDashboard(user)


def fallowArtist(user):
    system('clear')
    #show all artists
    query = """
            SELECT USERNAME,ID
            FROM ARTIST
        """
    print("username - id")
    for (username,id) in queryExecute(query,[]):
        print (username + " " + str(id))

    #input the id and the username of the artist to unfallow
    id = input("id: ")
    username = input("username: ")
    #delete it from artist_fallow
    query = """
            INSERT INTO ARTIST_FALLOW(ARTIST_USERNAME,ARTIST_ID,USER_ID,USER_EMAIL)
            VALUES(?,?,?,?)
        """
    nqueryExecute(query,[username,id,user.id,user.email])
    #back to dashboard
    userDashboard(user)

def unfallowArtist(user):
    system('clear')
    #show all the artists are fallowing
    query = """
            SELECT ARTIST_USERNAME , ARTIST_ID
            FROM ARTIST_FALLOW 
            WHERE USER_ID = ? AND USER_EMAIL = ?
        """
    print("id - email")
    for (email,id) in queryExecute(query , [user.id,user.email]):
        print (str(id) + " " + email)
    #input the username and the id of the artist
    username = input('username: ')
    id = input("id: ")
    #delte it
    query = """ 
        DELETE FROM ARTIST_FALLOW
        WHERE ARTIST_USERNAME = ? AND ARTIST_ID = ? AND USER_ID = ? AND USER_EMAIL = ?
    """
    nqueryExecute(query,[username,id,user.id,user.email])
    #go back to the dashboar
    userDashboard(user)

def fallowing(user):
    system('clear')
    print("1.fallow user: ")
    print("2.unfallow user: ")
    print("3.fallow artist")
    print("4.unfallow artist")
    print("5.showing fallowing users")
    print("6.showing fallowing artists")
    choice = input("enter the choice: ")
    if choice == '1':
        fallowUser(user)
    elif choice == '2':
        unfallowUser(user)
    elif choice == '3':
        fallowArtist(user)
    elif choice == '4':
        unfallowArtist(user)
    elif choice == '6':
        showFallowingArtists(user)
    elif choice == '5':
        showFallowingUsers(user)
    else:
        userDashboard(user)
def showFallowingArtists(user):
    system('clear')
    query = """SELECT ARTIST_ID,ARTIST_USERNAME
                FROM ARTIST_FALLOW INNER JOIN ARTIST ON ARTIST_FALLOW.ARTIST_ID = ARTIST.ID
                WHERE USER_ID = ?
            """
    print("artists fallowing: ")
    for (id,username) in queryExecute(query,[user.id]):
        print(str(id) + " " + username)
    input("press any key to back")
    userDashboard(user)
def showFallowingUsers(user):
    system('clear')
    query = """
            SELECT ID2,E2
            FROM USER_FALLOW
            WHERE ID1 = ?
    """
    print("users fallowing: ")
    for (id,email) in queryExecute(query,[user.id]):
        print(str(id) + " " + email)
    input("press Any key to continue")
    userDashboard(user)
def userDashboard(user):
    system('clear')
    print("1.logout")
    print("2.create playList")
    print("3.fallow existing playList")
    print("4.show Created PlayLists")
    print("5.show fallowing playLists")
    print("6.delte a playlist")
    print("7.unfallow a playlist")
    print("8.adding music to a playlist")
    print("9.fallow or unfallow")
    print("10.show details of songs")
    print("11.like a song")
    print('12.search for an artist')
    print('13.search for a song')
    print('14.watchout liked songs')
    print('15.delte a song from a playList')
    choice = input()
    if(choice == '1'):
        initilizaion()
    elif choice == '2':
        createPlayList(user)
    elif choice == '3':
        showAllPlayLists()
        fallowExistingPlayList(user)
    elif choice == '4':
        showCreatedPlayLists(user)
    elif choice == '5':
        showFallowingPlayLists(user)
    elif choice == '6':
        deletePlayList(user)
    elif choice == '7':
        unfallowPlayList(user)
    elif choice == '8':
        addSongToPlayList(user)
    elif choice == '9':
        fallowing(user)
    elif choice == '10':
        showAllSongs(user)
    elif choice == '11':
        likeSong(user)
    elif choice == '12':
        system('clear')
        username = input('username of the artist: ')
        searchArtist(user,username)
    elif choice == '13':
        system('clear')
        title = input('title of the song to search: ')
        searchSong(user,title)
    elif choice == '14':
        likedSongs(user)
    elif choice == '15':
        deleteSong(user)
    else:
        userDashboard(user)
def deleteSong(user):
    system('clear')
    query = """
        SELECT ID, NAME, DESCRIPTION
        FROM PLAYLIST
        WHERE OWNER = ?
    """
    print("id name description")
    for (id,name,description) in queryExecute(query,[user.id]):
        print(str(id) + " " + name + " " + description)
    id = input('enter the playList id: ')
    system('clear')
    query = '''
        SELECT ID,TITLE,DURATION,NUMBER_OF_PLAYS
        FROM MUSIC INNER JOIN ON_PLAYLIST ON ON_PLAYLIST.MUSIC_ID = MUSIC.ID
        WHERE PLAYLIST_ID = ?
    '''
    print ("id , title, duration ,numberOfPlays")
    for (musicid,title,duration,numberOfPlays) in queryExecute(query,[id]):
        print(str(musicid) + " " + str(title) + " " + str(duration ) + " " + str(numberOfPlays))
    mid = input("id of the song to deleter: ")
    query = """ 
        DELETE FROM ON_PLAYLIST
        WHERE MUSIC_ID = ? AND PLAYLIST_ID = ?
    """
    nqueryExecute(query,[mid,id])
    userDashboard(user)

def likedSongs(user):
    system('clear')
    query = """
        SELECT ID,TITLE,DURATION,NUMBER_OF_PLAYS
        FROM MUSIC INNER JOIN LIKED ON LIKED.MUSIC_ID = MUSIC.ID
        WHERE USER_ID = ? 
    """
    print("id title duration numberOfPlays")
    print("----------------------------------")
    for (id,title,duration,number_of_plays) in queryExecute(query,[user.id]):
        print(str(id) + " " + title + " " + str(duration) + " " + str(number_of_plays) )
    a = input("press any key to quite!!! ")
    userDashboard(user)

def searchSong(user,title):
    query = """
        SELECT ID,TITLE
        FROM MUSIC
        WHERE TITLE = ? 
    """
    for (id , title) in queryExecute(query,[title]):
        print(str(id ) + " " + title)
    id = input("input the if of the song: ")
    query = """
        SELECT ID,TITLE,DURATION,NUMBER_OF_PLAYS
        FROM MUSIC
        WHERE ID = ? AND TITLE = ?
    """
    if not queryExecute(query,[id,title]):
        userDashboard(user)
    (id,title,duration,numberOfPlays) = queryExecute(query,[id,title]).pop()
    print("id = " + str(id))
    print("title " + title)
    print("duration: " + duration)
    print("numberOfPlays: " + str(numberOfPlays))
    a = input()
    userDashboard(user)


def searchArtist(user,username):
    query = """
        SELECT ID, USERNAME 
        FROM ARTIST
        WHERE USERNAME = ?
    """
    print("id - username")
    for (id,username) in queryExecute(query,[username]):
        print(str(id) + " " + username)
    id = input("enter the id to search: ")
    query = """
        SELECT * 
        FROM ARTIST
        WHERE USERNAME = ? AND ID = ?
    """
    if not queryExecute(query,[username,id]):
        userDashboard(user)
        return
    (username,hashed_password, is_verified,about,id) = queryExecute(query,[username,id]).pop()
    print ("username: " + username)
    print("about: " + about)
    print("id: " + str(id))

    query = """
        SELECT POPULAR
        FROM POPULAR
        WHERE ID = ? AND USERNAME = ?
    """
    print('populars: ')
    for popular in queryExecute(query,[id,username]):
        print(popular[0])
    a = input()
    userDashboard(user)

def likeSong(user):
    system('clear')
    query = """
        SELECT  ID , TITLE ,DURATION
        FROM MUSIC
    """
    for (id,title,duration) in queryExecute(query,[]):
        print(str(id) + " " + title + " " + str(duration))
    id = input("id of the song to like: ")
    date = input("today date: ")
    query = """
        INSERT INTO LIKED(USER_ID,USER_EMAIL,MUSIC_ID,DATE)
        VALUES(?, ?,?,?)
    """
    try:
        nqueryExecute(query,[user.id,user.email,id,date])
    finally:
        userDashboard(user)
def showAllSongs(user):
    system('clear')
    query = """
        SELECT TITLE,DURATION,NUMBER_OF_PLAYS
        FROM MUSIC
    """
    print("title - duration - nubmerOfPlays")
    for (title,duration,numberOfPlays) in queryExecute(query,[]):
        print(title + " " + str(duration) + " " + str(numberOfPlays))
    a = input()
    userDashboard(user)
def addSongToPlayList(user):
    system('clear')
    query = """
        SELECT ID , NAME
        FROM PLAYLIST
        WHERE OWNER = ?
    """
    print("PLAYLIST: ")
    for (id,name) in queryExecute(query,[user.id]):
        print(str(id) + " " + name)
    print("-------------------------------------")
    query = """
        SELECT ID ,TITLE
        FROM MUSIC
    """
    print("SONGS: ")
    for (id,title) in queryExecute(query,[]):
        print(str(id) + " " + title)
    playListId = input("id to add to playList: ")
    musicId = input("id of the song to add: ")
    dateOfAdd = input("dateOfAdd: ")
    query ="""
    INSERT INTO ON_PLAYLIST(MUSIC_ID, DATE_OF_ADD,PLAYLIST_ID)
    VALUES (?,?,?)
    """
    nqueryExecute(query,[musicId,dateOfAdd,playListId])
    userDashboard(user)

def unfallowPlayList(user):
    system('clear')
    query = """
        SELECT ID,NAME
        FROM PLAYLIST INNER JOIN PLAYLIST_FALLOW ON PLAYLIST.ID = PLAYLIST_FALLOW.PLAYLIST_ID
        WHERE USER_ID = ?
    """
    for (id,name) in queryExecute(query,[user.id]):
        print(str(id) + " " + name)
    id = input("id of the playlist to unfallow: ")
    query = """
        DELETE FROM PLAYLIST_FALLOW
        WHERE USER_ID = ? AND PLAYLIST_ID = ?
    """
    nqueryExecute(query,[user.id ,id])
    userDashboard(user)
def deletePlayList(user):
    system('clear')
    query = """
        SELECT ID ,NAME
        FROM PLAYLIST
        WHERE OWNER = ?
    """
    for (id,name) in queryExecute(query,[user.id]):
        print(str(id) + " " + name)
    id = input("id to be removed: ")
    query = """
        DELETE FROM PLAYLIST
        WHERE ID = ?
    """
    nqueryExecute(query,[id])
    userDashboard(user)

def showFallowingPlayLists(user):
    system('clear')
    query = """
        SELECT ID, NAME,DESCRIPTION
        FROM PLAYLIST INNER JOIN PLAYLIST_FALLOW ON PLAYLIST.ID = PLAYLIST_FALLOW.PLAYLIST_ID
        WHERE USER_ID = ? AND PLAYLIST_ID = ID
    """
    print("id name description")
    for (id,name,description) in queryExecute(query,[user.id]):
        print(str(id) + " " + name + " " + description)
    id = input("enter the id to show songs: ")
    system('clear')
    query = """
        SELECT ID,TITLE,DURATION,NUMBER_OF_PLAYS
        FROM MUSIC INNER JOIN ON_PLAYLIST ON (MUSIC.ID = ON_PLAYlIST.MUSIC_ID)
        WHERE PLAYLIST_ID = ?
    """
    print("id, title, duration, numberOfPlays ")
    for (id,title,duration,numberOfPlays) in queryExecute(query,[id]):
        print(str(id) + " " + title + " " + str(duration) + " " + str(numberOfPlays))
    input("press any key to continue")
    userDashboard(user)
def showCreatedPlayLists(user):
    system('clear')
    id = user.id
    query = """
        SELECT ID,NAME,DESCRIPTION
        FROM PLAYLIST
        WHERE OWNER = ?
    """
    print("id name description")
    for(id,name,description) in queryExecute(query,[id]):
        print(str(id) + " " + name + " " + description)
    id = input('enter the id of the playList to show the songs: ')
    system('clear')
    query = """
        SELECT ID , TITLE, DURATION,NUMBER_OF_PLAYS FROM
        MUSIC INNER JOIN ON_PLAYLIST ON MUSIC.ID = ON_PLAYLIST.MUSIC_ID
        WHERE PLAYLIST_ID = ?
    """
    print ("id , title, duration, numberOfPlays")
    for (id,title,duration,numberOfPlays) in queryExecute(query,[id]):
        print(str(id) + " " + title + " " + str(duration) + " " + str(numberOfPlays))
    input('press any key to back')
    userDashboard(user)
def addPopular(artist):
    system('clear')
    popular = input("popular: ")

    query = """
        INSERT INTO POPULAR(USERNAME,ID,POPULAR)
        VALUES( ? , ? , ? ) 
    """
    nqueryExecute(query,[artist.username,artist.id,popular])

    artistDashboard(artist)
def artistSignIn():
    system('clear')
    username = input('username: ')
    password = md5(input('password: ').encode()).hexdigest()
    query = """
            SELECT * 
            FROM ARTIST
            WHERE USERNAME = ? AND HASHED_PASSWORD = ?
    """
    rows = queryExecute(query,[username,password])
    if not rows:
        artistSignIn()
        return
    (username, password, is_verified, about, id) = rows.pop()
    artistDashboard(Artist(username,password,is_verified,about,id))
def artistSignUp():
    system('clear')
    username = input('username: ')
    password = input('password: ')
    about = input('about: ')
    query = """
            INSERT INTO ARTIST(USERNAME, HASHED_PASSWORD, IS_VERIFIED, ABOUT,ID)
            VALUES (?,?,?,?,?)
    """
    id = generate_key()
    nqueryExecute(query,[username,md5(password.encode()).hexdigest(),0,about,id])
    artistDashboard(Artist(username,password,0,about,id))
def createPlayList(user):
    system('clear')
    query = """
        INSERT INTO PLAYLIST(NAME,DESCRIPTION,IMAGE_REFERENCE,ID,OWNER)
        VALUES(?,?,?,?,?)
    """
    name = input("name: ")
    description = input("description: ")
    image_reference = input("image_reference: ")
    id = generate_key()

    nqueryExecute(query,[name,description,image_reference,id,user.id])
    userDashboard(user)
def artistDashboard(artist):
    system('clear')
    print("1.logout")
    print("2.add popular")
    print("3.create Album")
    print("4.add Song")
    print('5.add song to an album')
    print('6.add participate to a song')
    choice = input()
    if(choice == '1'):
        initilizaion()
    elif choice == '2':
        addPopular(artist)
    elif choice == '3':
        createAlbum(artist)
    elif choice == '4':
        addSong(artist)
    elif choice == '5':
        addSongToAlbum(artist)
    elif choice == '6':
        addParticipate(artist)
    else:
        ArtistDashboard(artist)

def addParticipate(artist):
    system('clear')
    print('id title')
    query = '''
        SELECT ID, TITLE
        FROM ALBUM INNER JOIN INTABLE ON INTABLE.ALBUM_ID = ALBUM.ID 
        WHERE ARTIST_ID = ?
    '''
    for (id,title) in queryExecute(query,[artist.id]):
        print(str(id) + " " + title)
    albumId = input('id of the album to add participate: ')
    system('clear')
    query = '''
        SELECT ID, USERNAME
        FROM ARTIST
    '''
    print("id username")
    for (id,username) in queryExecute(query,[]):
        print(str(id) + " " + username)
    artistId = input('artist to add to album: ')
    query = '''
        INSERT INTO INTABLE(ARTIST_ID,ARTIST_USERNAME,IS_OWNER,ALBUM_ID)
        VALUES(?,?,?,?)
    '''
    nqueryExecute(query,[artist.id,artist.username,0,albumId])
    artistDashboard(artist)
def addSong(artist):
    system('clear')
    query = """
        SELECT ID ,TITLE
        FROM ALBUM INNER JOIN INTABLE ON ALBUM.ID = INTABLE.ALBUM_ID
        WHERE ARTIST_ID= ?
    """
    print("id and the title of the albums")
    for (id,title) in queryExecute(query,[artist.id]):
        print (str(id) + " " + title)

    title = input('title: ')
    duration = input("duration: ")
    fileReference = input("fileReference: ")
    id = generate_key()
    coverReference = input('coverReference: ')
    albumId = input('id of the album to add: ')
    query = """
        INSERT INTO MUSIC(TITLE,DURATION,NUMBER_OF_PLAYS,FILE_REFERENCE,IS_ACTIVE,IS_EXPIRED,ID,COVER_REFERENCE,ALBUM_ID)
        VALUES(?,?,?,?,?,?,?,?,?)
        """
    nqueryExecute(query,[title,duration,0,fileReference,1,0,id,coverReference,albumId])
    artistDashboard(artist)

def createAlbum(artist):
    system('clear')
    id = generate_key()
    title = input("title: ")
    releaseYear = input("releaseYear: ")
    copyRight = input("copyright: ")
    isOwner = input("1 if you are the owner 0 o.w: ")
    query = """
        INSERT INTO ALBUM(ID,TITLE,RELEASE_YEAR,COPYRIGHT,IS_SIGLE_OR_EP)
        VALUES(?,?,?,?,?)
    """
    nqueryExecute(query,[id,title,releaseYear,copyRight,0])
    query = """
        INSERT INTO INTABLE(ARTIST_ID,ARTIST_USERNAME,IS_OWNER,ALBUM_ID)
        VALUES (?,?,?,?)
    """
    nqueryExecute(query,[artist.id,artist.username,isOwner,id])
    artistDashboard(artist)


def showAllPlayLists():
    system('clear')
    query = """
        SELECT ID,NAME
        FROM PLAYLIST 
    """
    for (id,name) in queryExecute(query,[]):
        print(str(id) + " " + name)

def fallowExistingPlayList(user):
    id = input("id: ")
    query = """
    INSERT INTO PLAYLIST_FALLOW(USER_ID,USER_EMAIL,PLAYLIST_ID)
    VALUES (?, ?, ?)
    """
    nqueryExecute(query,[user.id,user.email,id])
    userDashboard(user)
initilizaion()




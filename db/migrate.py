import sqlite3


def do_db_init():
    """
    初始化数据库
    :return:
    """

    conn = sqlite3.connect("cssrcmsg.db")
    c = conn.cursor()
    init_sql = '''
    DROP TABLE IF EXISTS CUR_USER; 
    CREATE TABLE CUR_USER(
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    WORKER_ID CHAR(100) NOT NULL,
    WORKER_NAME CHAR(100) NOT NULL, 
    TOKEN TEXT NOT NULL,
    LAST_LOGIN_TIME DATETIME
    );

    DROP TABLE IF EXISTS REMOTE_SERVER;
    CREATE TABLE REMOTE_SERVER(
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    IP CHAR(100),
    PORT CHAR(50),
    BASE_URL CHAR(500),
    SOCKET_BASE_URL CHAR(500)
    );
    INSERT INTO REMOTE_SERVER(IP, PORT, BASE_URL, SOCKET_BASE_URL) VALUES('127.0.0.1', '5000', 'http://127.0.0.1:5000', '/websocket/user_refresh')
    '''
    c.executescript(init_sql)
    conn.commit()
    conn.close()
    print(">>>初始化数据库完成>>>")

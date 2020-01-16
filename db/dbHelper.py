#!/usr/bin/env python  
# encoding: utf-8
import os
import sqlite3
import sys

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))
sys.path.append("..")


class ConnectSqlite:

    def __init__(self, dbName="./cssrcmsgbox.db"):
        """
        初始化连接--使用完记得关闭连接
        :param dbName: 连接库名字，注意，以'.db'结尾
        """
        self._conn = sqlite3.connect(dbName)
        self._cur = self._conn.cursor()
        self._time_now = "[" + sqlite3.datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S') + "]"

    def close_con(self):
        """
        关闭连接对象--主动调用
        :return:
        """
        self._cur.close()
        self._conn.close()

    def create_tabel(self, sql):
        """
        创建表初始化
        :param sql: 建表语句
        :return: True is ok
        """
        try:
            self._cur.execute(sql)
            self._conn.commit()
            return True
        except Exception as e:
            print(self._time_now, "[CREATE TABLE ERROR]", e)
            return False

    def drop_table(self, table_name):
        """
        删除表
        :param table_name: 表名
        :return:
        """
        try:
            self._cur.execute('DROP TABLE {0}'.format(table_name))
            self._conn.commit()
            return True
        except Exception as e:
            print(self._time_now, "[DROP TABLE ERROR]", e)
            return False

    def delete_table(self, sql):
        """
        删除表记录
        :param sql:
        :return: True or False
        """
        try:
            if 'DELETE' in sql.upper():
                self._cur.execute(sql)
                self._conn.commit()
                return True
            else:
                print(self._time_now, "[EXECUTE SQL IS NOT DELETE]")
                return False
        except Exception as e:
            print(self._time_now, "[DELETE TABLE ERROR]", e)
            return False

    def fetchall_table(self, sql, limit_flag=True):
        """
        查询所有数据
        :param sql:
        :param limit_flag: 查询条数选择，False 查询一条，True 全部查询
        :return:
        """
        try:
            self._cur.execute(sql)
            war_msg = self._time_now + ' The [{}] is empty or equal None!'.format(sql)
            if limit_flag is True:
                r = self._cur.fetchall()
                return r if len(r) > 0 else war_msg
            elif limit_flag is False:
                r = self._cur.fetchone()
                return r if len(r) > 0 else war_msg
        except Exception as e:
            print(self._time_now, "[SELECT TABLE ERROR]", e)

    def insert_update_table(self, sql, args):
        """
        插入/更新表记录
        :param sql:
        :return:
        """
        try:
            self._cur.execute(sql, args)
            self._conn.commit()
            return True
        except Exception as e:
            print(self._time_now, "[INSERT/UPDATE TABLE ERROR]", e)
            return False

    def insert_table_many(self, sql, value):
        """
        插入多条记录
        :param sql:
        :param value: list:[(),()]
        :return:
        """
        try:
            self._cur.executemany(sql, value)
            self._conn.commit()
            return True
        except Exception as e:
            print(self._time_now, "[INSERT MANY TABLE ERROR]", e)
            return False

    def do_db_init(self):
        """
        初始化数据库
        :return:
        """
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
        self._cur.executescript(init_sql)
        self._conn.commit()
        print(">>>初始化数据库完成>>>")


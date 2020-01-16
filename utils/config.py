from db.dbHelper import ConnectSqlite


class BasesConfig:
    """
    客户端全局配置文件
    """
    REMOTE_IP = "127.0.0.1"

    REMOTE_PORT = 5000

    REMOTE_URL_BASE = "http://127.0.0.1:5000"

    REMOTE_SOCKET_BASE = "ws://127.0.0.1:5000"

    SOCKET_URL = REMOTE_SOCKET_BASE + "/websocket/user_refresh"

    API_V = "/api/v1.0"

    @staticmethod
    def init_config():
        """
        初始化参数
        :return:
        """
        conn = ConnectSqlite()
        r = conn.fetchall_table("SELECT * FROM REMOTE_SERVER ORDER BY ID DESC LIMIT 0, 1", False)
        if r:
            BasesConfig.REMOTE_IP = r[1]
            BasesConfig.REMOTE_PORT = r[2]
            BasesConfig.REMOTE_URL_BASE = "http://%s:%s" % (r[1], r[2])
            BasesConfig.REMOTE_SOCKET_BASE = "ws://%s:%s" % (r[1], r[2])
            BasesConfig.SOCKET_URL = BasesConfig.REMOTE_URL_BASE + "/websocket/user_refresh"
        conn.close_con()

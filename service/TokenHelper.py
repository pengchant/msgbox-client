from db.dbHelper import ConnectSqlite


class MyTokenManage():
    """
    token管理
    """

    @staticmethod
    def getToken():
        """获取数据库中存储的token"""
        conn = ConnectSqlite()
        result = conn.fetchall_table("SELECT TOKEN FROM CUR_USER ORDER BY ID DESC", False)
        if result:
            return result[0]
        return None

import hashlib
from datetime import datetime

from db.dbHelper import ConnectSqlite
from utils.config import BasesConfig
from utils.myhttp import MyHttpHelper


def login(usrobj):
    """
    执行登录逻辑
    :param usrobj:  用户提交的{}
    :return:
    """
    pwd = usrobj['password']
    usrobj['password'] = hashlib.md5(pwd.encode('utf-8')).hexdigest()
    url = BasesConfig.REMOTE_URL_BASE + BasesConfig.API_V + "/passport"
    result = MyHttpHelper.http_post_json(url, usrobj, is_token=False)
    if result.get("re_code") == "0":  # 如果登录成功
        # 保存到数据库中
        conn = ConnectSqlite()
        user = result.get("usr")
        worker_id = user.get("workerid")
        worker_name = user.get("usrname")
        last_login_time = datetime.now()
        conn.insert_update_table("INSERT INTO CUR_USER (WORKER_ID, WORKER_NAME, TOKEN, LAST_LOGIN_TIME)" \
                                 "VALUES (?,?,?,?)", (worker_id, worker_name, result.get('data'), last_login_time))
        conn.close_con()
        return True
    else:
        return result.get("msg"), result.get("re_code")


def getUsrTuples():
    """
    获取当前用户的workerid和usrname元组
    :return:
    """
    conn = ConnectSqlite()
    ut = conn.fetchall_table("SELECT WORKER_ID, WORKER_NAME FROM CUR_USER ORDER BY ID DESC", False)
    return ut

import hashlib

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
    if result.get("re_code")=="0": # 如果登录成功
        pass
    else:
        pass

from utils.config import BasesConfig
from utils.myhttp import MyHttpHelper


def update_msg_read(msgid):
    """
    标记id为msgid的消息已被用户阅读
    :param msgid:
    :return:
    """
    url = BasesConfig.REMOTE_URL_BASE + BasesConfig.API_V + "/update_hasread?msgid=" + msgid
    result = MyHttpHelper.http_post_json(url, {}, is_token=True)
    return result

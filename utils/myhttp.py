import json
import requests

from service.TokenHelper import MyTokenManage


class MyHttpHelper():
    """
    http请求的封装
    """

    @staticmethod
    def http_post_json(url, data_json, is_token=False):
        """
        发起post请求
        :param url:
        :param data_json:
        :return:
        """
        headers = {"Content-Type": 'application/json'}
        if is_token:
            # 获取token
            token = MyTokenManage.getToken()
            headers['Authorization'] = token
        datas = json.dumps(data_json)
        r = requests.post(url, data=datas, headers=headers)
        return json.loads(r.text)

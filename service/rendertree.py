from PyQt5.QtCore import QThread, pyqtSignal
from socketIO_client import BaseNamespace, SocketIO

from utils.config import BasesConfig
from utils.myhttp import MyHttpHelper


class ChatNamespace(BaseNamespace):
    """命名空间"""
    WORKER_ID = None  # 用户的工号

    RENDER_THREAD = None  # 渲染的线程

    def on_connect(self):
        print('连接完成....')

    def on_disconnect(self):
        print('失去连接...')

    def on_reconnect(self):
        print('重新连接...')
        self.emit('connect_event', {"workerid": ChatNamespace.WORKER_ID})

    def on_server_response(self, *args):
        """服务器返回的消息"""
        print("服务器返回...", args)

    def on_push_message(self, *args):
        """服务器推送的消息 [单个消息]"""
        print("来自服务器的消息(单个)-->", args)
        msgid = args[0].get("msg_id")
        url = BasesConfig.REMOTE_URL_BASE + BasesConfig.API_V + "/client_update_msg"
        msglist = []
        msglist.append(msgid)
        push_data = {'workerid': ChatNamespace.WORKER_ID, 'msgs': msglist}
        result = MyHttpHelper.http_post_json(url, push_data, is_token=True)
        # 重新渲染树
        print(result)
        ChatNamespace.RENDER_THREAD.breakSignal.emit(result)  # 通知主线程修改ui

    def on_init_response(self, *args):
        """接收到系统推送的消息 [多个消息]"""
        print("接收到系统推送的消息(多个)-->", args)
        url = BasesConfig.REMOTE_URL_BASE + BasesConfig.API_V + "/client_update_msg"
        msglist = [v['id'] for v in args[0]['data']]
        push_data = {'workerid': ChatNamespace.WORKER_ID, 'msgs': msglist}
        result = MyHttpHelper.http_post_json(url, push_data, is_token=True)
        # 重新渲染树
        print(result)
        ChatNamespace.RENDER_THREAD.breakSignal.emit(result)  # 通知主线程修改ui


class TreeRenderThread(QThread):
    """节点树渲染的线程,同时负责与后台建立socket链接通信"""
    breakSignal = pyqtSignal(object)

    def __init__(self, workerid, parent=None):
        super().__init__(parent)
        self.workerid = workerid

    def run(self):
        socketIO = SocketIO(BasesConfig.REMOTE_IP, BasesConfig.REMOTE_PORT)
        chat_namespace = socketIO.define(ChatNamespace, "/websocket/user_refresh")
        ChatNamespace.WORKER_ID = self.workerid
        ChatNamespace.RENDER_THREAD = self
        chat_namespace.emit('connect_event', {"workerid": self.workerid})  # 告知服务器的sid->workerid的映射
        socketIO.wait()

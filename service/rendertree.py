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

    #
    # def createmsg_list(self, msg_info_data):
    #     """
    #     添加信息列表
    #     :param msg_info_data:  消息列表
    #     :return:
    #     """
    #     ChatNamespace.Parent.tree = QTreeWidget(ChatNamespace.Parent)  # 创建tree组件
    #     # 设置列数
    #     ChatNamespace.Parent.tree.setColumnCount(2)  # 设置列数
    #     # 设置树形控件的头部标题
    #     ChatNamespace.Parent.tree.setHeaderLabels(["消息描述", "推送时间"])  # 给treeview设置标题
    #
    #     # 设置根节点
    #     root = QTreeWidgetItem(ChatNamespace.Parent.tree)  # 设置根节点
    #     root.setText(0, "cssrc消息盒子(未读消息)")  # 设置根节点的名字
    #     root.setIcon(0, QIcon("static/msg.png"))  # 设置 根节点的图片
    #
    #     # 设置属性控件列的宽度
    #     ChatNamespace.Parent.tree.setColumnWidth(0, 280)
    #     ChatNamespace.Parent.tree.setColumnWidth(1, 80)
    #
    #     try:
    #         msg_list = msg_info_data.get('data').get('msgs')
    #         sys_list = msg_info_data.get('data').get('sys')
    #         for sys in sys_list:
    #             child = QTreeWidgetItem()
    #             child.setText(0, sys.get("sysname"))
    #             child.setText(1, "")
    #             child.setIcon(0, QIcon("static/msg.png"))
    #             # 添加到根节点上
    #             root.addChild(child)
    #             # 添加二级节点
    #             for msg in msg_list:
    #                 # 将该系统下的所有的消息加载到节点上
    #                 if msg.get("from_sys") == sys.get("id"):
    #                     sec_child = QTreeWidgetItem(child)
    #                     sec_child.setText(0, msg.get("msg_title"))
    #                     sec_child.setText(1, msg.get("msg_push_time"))
    #                     sec_child.setIcon(0, QIcon("static/msg.png"))
    #     except Exception as e:
    #         print("解析异常")
    #
    #     # 加载根节点的所有属性 与子控件
    #     ChatNamespace.Parent.tree.addTopLevelItem(root)
    #
    #     # 给节点点击添加响应事件
    #     ChatNamespace.Parent.tree.clicked.connect(ChatNamespace.Parent.onClicked)
    #
    #     # 节点全部展开看
    #     ChatNamespace.Parent.tree.expandAll()
    #
    #     # 添加到父容器中设置位置
    #     ChatNamespace.Parent.tree.setGeometry(0, 0, 400, 580)


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

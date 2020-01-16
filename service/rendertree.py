import threading

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem
from socketIO_client import BaseNamespace, SocketIO

from utils.config import BasesConfig


class ChatNamespace(BaseNamespace):
    """命名空间"""
    Parent = None  # ui的self对象
    ContainerWidget = None  # 树形组件容器

    def on_connect(self):
        print('连接完成....')

    def on_disconnect(self):
        print('失去连接...')

    def on_reconnect(self):
        print('重新连接...')

    def on_server_response(self, *args):
        """服务器返回的消息"""
        print("服务器返回...", args)

    def on_push_message(self, *args):
        """服务器推送的消息 [单个消息]"""
        print("来自服务器的消息(单个)-->", args)
        msgid = args[0].get("msg_id")

    def on_init_response(self, *args):
        """接收到系统推送的消息 [多个消息]"""
        print("接收到系统推送的消息(多个)-->", args)

    def createmsg_list(self):
        """
        添加信息列表
        :return:
        """
        ChatNamespace.Parent.tree = QTreeWidget(ChatNamespace.Parent)  # 创建tree组件
        # 设置列数
        ChatNamespace.Parent.tree.setColumnCount(2)  # 设置列数
        # 设置树形控件的头部标题
        ChatNamespace.Parent.tree.setHeaderLabels(["消息描述", "推送时间"])  # 给treeview设置标题

        # 设置根节点
        root = QTreeWidgetItem(ChatNamespace.Parent.tree)  # 设置根节点
        root.setText(0, "cssrc消息盒子(未读消息)")  # 设置根节点的名字
        root.setIcon(0, QIcon("static/msg.png"))  # 设置 根节点的图片

        # 设置属性控件列的宽度
        ChatNamespace.Parent.tree.setColumnWidth(0, 280)
        ChatNamespace.Parent.tree.setColumnWidth(1, 80)

        # todo: 设置子节点
        # for i in range(10):
        #     child = QTreeWidgetItem()
        #     child.setText(0, "数值船海系统" + str(i + 1))
        #     child.setText(1, "")
        #     child.setIcon(0, QIcon("static/msg.png"))
        #     # 添加子节点
        #     root.addChild(child)
        #     # 添加二级节点
        #     for j in range(2):
        #         sec_child = QTreeWidgetItem(child)
        #         sec_child.setText(0, "人力资源管理系统" + str(i + 1))
        #         curr = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        #         sec_child.setText(1, curr)
        #         sec_child.setIcon(0, QIcon("static/msg.png"))

        # 加载根节点的所有属性 与子控件
        ChatNamespace.Parent.tree.addTopLevelItem(root)

        # 给节点点击添加响应事件
        ChatNamespace.Parent.tree.clicked.connect(ChatNamespace.Parent.onClicked)

        # 节点全部展开看
        ChatNamespace.Parent.tree.expandAll()

        # 添加到父容器中设置位置
        ChatNamespace.Parent.tree.setGeometry(0, 0, 400, 580)


class TreeRenderThread(threading.Thread):
    """节点树渲染的线程"""

    def __init__(self, workerid):
        threading.Thread.__init__(self)
        self.workerid = workerid

    def run(self):
        socketIO = SocketIO(BasesConfig.REMOTE_IP, BasesConfig.REMOTE_PORT)
        chat_namespace = socketIO.define(ChatNamespace, "/websocket/user_refresh")
        chat_namespace.emit('connect_event', {"workerid": self.workerid})  # 告知服务器的sid->workerid的映射
        socketIO.wait()

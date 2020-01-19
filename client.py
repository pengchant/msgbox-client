import sys, os
if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']

from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5.QtWidgets import QWidget, QApplication, QAction, qApp, QMainWindow, QVBoxLayout, QLabel, QHBoxLayout, \
    QTreeWidget, QTreeWidgetItem, QMessageBox

from service.clientservice import update_msg_read
from service.loginservice import getUsrTuples
from service.rendertree import TreeRenderThread, ChatNamespace
from utils.date_util import MyDateInfoHelper


class ClientForm(QMainWindow):
    """主页面"""

    def __init__(self):
        super().__init__()
        self.init = 0  # 0 代表初始情况，需要建立websocket连接,其他不用
        self.cur_user_t = ('', '')  # 当前用户的工号和姓名
        self.initUI()

    def initUI(self):
        """
        初始化UI
        :return:
        """
        self.setObjectName("mainWindow")
        self.setStyleSheet('#mainWindow{background-color:white}')
        self.setFixedSize(400, 770)
        self.setWindowTitle("cssrc消息盒子")
        self.setWindowIcon(QIcon('static/logo_title.png'))

        # 获取屏幕信息
        desktop = QApplication.desktop()
        self.move(desktop.width() - 400 - 10, 5)
        # 创建状态栏
        self.statusBar().showMessage("copyright@cssrc")

        # 创建菜单栏
        self.create_menu()

        # 创建用户信息部分
        uwidget = QWidget(self)
        uwidget.setObjectName("usrpart")
        uwidget.setStyleSheet("#usrpart{border:1px solid #e1e2e2;border-left:none;border-right:none;}")
        uwidget.setGeometry(0, 26, 400, 80)
        hbox_user = QHBoxLayout()
        uwidget.setLayout(hbox_user)

        # 创建用户头像
        pixmap = QPixmap("static/usr.png")
        label = QLabel(self)
        label.setPixmap(pixmap)
        hbox_user.addWidget(label, 1)

        # 用户信息
        uvbox = QVBoxLayout()
        usrname = self.cur_user_t[1] if self.cur_user_t is not None else "暂无"
        self.lbl_usrname = QLabel("%s, %s好" % (usrname, "下午"))
        self.lbl_usrname.setFont(QFont("Microsoft YaHei"))
        self.lbl_usrname.setStyleSheet("margin-left:10px")
        uvbox.addWidget(self.lbl_usrname)

        # 消息logo
        msg_logo_num = QWidget()
        msg_logo_num_lay = QHBoxLayout()
        msg_logo_num.setLayout(msg_logo_num_lay)  # 消息条数部分组件
        lbl_msgnum = QLabel()
        msgpixmap = QPixmap("static/msg_sm.png")
        lbl_msgnum.setPixmap(msgpixmap)
        msg_logo_num_lay.addWidget(lbl_msgnum)
        lbl_msg_number = QLabel("(12)")
        lbl_msg_number.setFont(QFont("Microsoft YaHei"))
        msg_logo_num_lay.addWidget(lbl_msg_number, 1)

        uvbox.addWidget(msg_logo_num)

        hbox_user.addLayout(uvbox, 4)

        # 创建消息列表部分
        unread_label = QLabel(self)
        unread_label.setObjectName("unread_label")
        unread_label.setText("未读消息")
        unread_label.setFont(QFont("Microsoft YaHei"))
        unread_label.setStyleSheet(
            "#%s{border:1px solid #e1e2e2;border-left:none;border-right:none;padding-left:20px;}" % "unread_label")
        unread_label.setGeometry(0, 105, 400, 50)
        # 消息列表具体内容
        self.msglist_widget = QWidget(self)
        self.msglist_widget.setGeometry(0, 155, 400, 580)
        self.msglist_widget.setObjectName("msglist")
        self.msglist_widget.setStyleSheet("#msglist{border:1px solid red}")

        # 在此动态添加内容
        self.tree = QTreeWidget(self.msglist_widget)  # 创建tree组件
        # 设置列数
        self.tree.setColumnCount(3)  # 设置列数
        # 设置树形控件的头部标题
        self.tree.setHeaderLabels(["消息描述", "推送时间", "url"])  # 给treeview设置标题
        # 设置隐藏
        self.tree.setColumnHidden(2, True)
        # 设置属性控件列的宽度
        self.tree.setColumnWidth(0, 280)
        self.tree.setColumnWidth(1, 80)

    def create_menu(self):
        """
        创建菜单
        :return:
        """

        menubar = self.menuBar()  # 创建菜单栏
        # 新建菜单项
        fileMenu = menubar.addMenu("&文件(F)")
        # 添加菜单子项
        selfAct = QAction(QIcon('exit.png'), '&个人设置(P)', self)
        selfAct.setShortcut('Ctrl+P')
        selfAct.setStatusTip("个人设置")
        selfAct.triggered.connect(self.go_self_setting)  # 查看个人信息页面
        fileMenu.addAction(selfAct)

        # 系统设置
        syssetAct = QAction("&系统设置(S)", self)
        syssetAct.setShortcut("Ctrl+S")
        syssetAct.setStatusTip("系统设置")
        syssetAct.triggered.connect(self.go_sys_setting)  # 去系统设置页面
        fileMenu.addAction(syssetAct)

        # 退出
        exitAct = QAction("&退出(X)", self)
        exitAct.setShortcut("Ctrl+X")
        exitAct.setStatusTip("退出系统")
        exitAct.triggered.connect(qApp.quit)  # 退出系统
        fileMenu.addAction(exitAct)

        # 新建帮助菜单项
        helpMenu = menubar.addMenu("&帮助(H)")
        # 添加帮助菜单项
        seeAct = QAction("&查看消息记录(M)", self)
        seeAct.setShortcut("Ctrl+M")
        seeAct.setStatusTip("查看消息记录")
        seeAct.triggered.connect(self.go_see_history)  # 查看历史消息
        helpMenu.addAction(seeAct)

        # 刷新系统组织
        refreshSys = QAction("&刷新系统组织(U)", self)
        refreshSys.setShortcut("Ctrl+U")
        refreshSys.setStatusTip("刷新系统组织")
        refreshSys.triggered.connect(self.go_fresh_sys)  # 刷新系统组织
        helpMenu.addAction(refreshSys)

        # 关于
        aboutAct = QAction("&关于(A)", self)
        aboutAct.setShortcut("Ctrl+A")
        aboutAct.setStatusTip("关于系统")
        aboutAct.triggered.connect(self.go_about)  # 关于系统
        helpMenu.addAction(aboutAct)

    def go_self_setting(self):
        """
        个人设置页面
        :return:
        """
        print("查看个人设置 页面")

    def go_sys_setting(self):
        """
        系统设置页面
        :return:
        """
        print("系统设置 页面")

    def go_see_history(self):
        """
        查看历史消息
        :return:
        """
        print("历史消息 页面")

    def go_fresh_sys(self):
        """
        刷新系统组织
        :return:
        """
        print("系统组织")

    def go_about(self):
        """
        查看关于系统
        :return:
        """
        print("关于系统")

    def do_fetch_data(self):
        """
        加载用户数据
        :return:
        """
        self.cur_user_t = getUsrTuples()
        print(self.cur_user_t)

    def onClicked(self, index):
        """
        点击单个选项事件
        :param index:
        :return:
        """
        item = self.tree.currentItem()  # 获取当前选中的节点
        if item and item.text(2) != "":
            param = item.text(2).split("|")
            if param is not None and param[2] != "WAITTING_READ":
                QtGui.QDesktopServices.openUrl(QtCore.QUrl(param[1]))
                return
            button = QMessageBox.warning(self, "提示", "是否前去查看?", QMessageBox.Ok | QMessageBox.Cancel, QMessageBox.Ok)
            if button == QMessageBox.Ok:  # 如果确定，就打开网页
                QtGui.QDesktopServices.openUrl(QtCore.QUrl(param[1]))
                # 发起一个Http请求告知后端该消息已被查看
                if param is not None and param[2] == "WAITTING_READ":
                    try:
                        result = update_msg_read(param[0])
                        print(result)
                    except:
                        pass

    def showEvent(self, *args, **kwargs):
        """
        显示
        1.建立socket连接
        2.加载数据
        3.绑定数据
        :param args:
        :param kwargs:
        :return:
        """
        if self.init == 0:  # 初次加载
            print("show...")
            self.do_fetch_data()
            self.lbl_usrname.setText("%s, %s好" % (self.cur_user_t[1], MyDateInfoHelper.getTimeRange()))
            self.init += 1  # 累加
            # 建立socket连接,开启新线程自动刷新列表
            ChatNamespace.ContainerWidget = self.msglist_widget
            ChatNamespace.Parent = self
            refresh_thread = TreeRenderThread(self.cur_user_t[0])  # 传递工号
            refresh_thread.breakSignal.connect(self.createmsg_list)
            refresh_thread.start()  # 开启新线程

    def createmsg_list(self, msg_info_data):
        """
        添加信息列表
        :param msg_info_data:  消息列表
        :return:
        """
        # 先清空root根下面的所有的历史消息
        self.tree.clear()
        # 设置根节点
        self.root = QTreeWidgetItem(self.tree)  # 设置根节点
        self.root.setText(0, "cssrc消息盒子(未读消息)")  # 设置根节点的名字
        self.root.setIcon(0, QIcon("static/loc.png"))  # 设置 根节点的图片

        try:
            msg_list = msg_info_data.get('data').get('msgs')
            sys_list = msg_info_data.get('data').get('sys')
            for sys in sys_list:
                child = QTreeWidgetItem()
                child.setText(0, sys.get("sysname"))
                child.setIcon(0, QIcon("static/app.png"))
                child.setText(1, "")
                child.setText(2, "")
                # 添加到根节点上
                self.root.addChild(child)
                # 添加二级节点
                for msg in msg_list:
                    # 将该系统下的所有的消息加载到节点上
                    if msg.get("from_sys") == sys.get("id"):
                        status = msg.get("msg_status")
                        sec_child = QTreeWidgetItem(child)
                        # sec_child.setToolTip("")
                        sec_child.setText(0, msg.get("msg_title"))
                        sec_child.setText(1, msg.get("msg_push_time"))
                        sec_child.setText(2, str(msg.get("id")) + "|" + str(msg.get("msg_url")) + "|" + status)
                        if status == "WAITTING_READ":
                            sec_child.setIcon(0, QIcon("static/msg_alert.png"))
                        else:
                            sec_child.setIcon(0, QIcon("static/xx.png"))
        except Exception as e:
            print("解析异常")

        # 加载根节点的所有属性 与子控件
        self.tree.addTopLevelItem(self.root)

        # 给节点点击添加响应事件
        try:
            self.tree.clicked.disconnect(self.onClicked)  # 先取消绑定
        except:
            pass
        self.tree.clicked.connect(self.onClicked)

        # 节点全部展开看
        self.tree.expandAll()

        # 添加到父容器中设置位置
        self.tree.setGeometry(0, 0, 400, 580)

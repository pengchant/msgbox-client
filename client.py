import time

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5.QtWidgets import QWidget, QApplication, QAction, qApp, QMainWindow, QVBoxLayout, QLabel, QHBoxLayout, \
    QScrollArea, QTreeWidget, QTreeWidgetItem, QMessageBox

from service.loginservice import getUsrTuples


class ClientForm(QMainWindow):
    """主页面"""

    def __init__(self):
        super().__init__()
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
        msglist_widget = QWidget(self)
        msglist_widget.setGeometry(0, 155, 400, 580)
        msglist_widget.setObjectName("msglist")
        msglist_widget.setStyleSheet("#msglist{border:1px solid red}")

        # 在此动态添加内容
        self.createmsg_list(msglist_widget)

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

    def createmsg_list(self, parent):
        """
        添加信息列表
        :return:
        """
        self.tree = QTreeWidget(parent)  # 创建tree组件
        # 设置列数
        self.tree.setColumnCount(2)  # 设置列数
        # 设置树形控件的头部标题
        self.tree.setHeaderLabels(["消息描述", "推送时间"])  # 给treeview设置标题

        # 设置根节点
        root = QTreeWidgetItem(self.tree)  # 设置根节点
        root.setText(0, "cssrc消息盒子(未读消息)")  # 设置根节点的名字
        root.setIcon(0, QIcon("static/msg.png"))  # 设置 根节点的图片

        # 设置属性控件列的宽度
        self.tree.setColumnWidth(0, 280)
        self.tree.setColumnWidth(1, 80)

        # 设置子节点
        for i in range(10):
            child = QTreeWidgetItem()
            child.setText(0, "数值船海系统" + str(i + 1))
            child.setText(1, "")
            child.setIcon(0, QIcon("static/msg.png"))
            # 添加子节点
            root.addChild(child)
            # 添加二级节点
            for j in range(2):
                sec_child = QTreeWidgetItem(child)
                sec_child.setText(0, "人力资源管理系统" + str(i + 1))
                curr = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                sec_child.setText(1, curr)
                sec_child.setIcon(0, QIcon("static/msg.png"))

        # todo设置节点的状态
        child2 = QTreeWidgetItem(root)
        child2.setText(0, "人力资源管理系统")
        child2.setText(1, "")
        child2.setIcon(0, QIcon("static/msg.png"))

        # 设置cihld2的子节点
        child3 = QTreeWidgetItem(child2)
        child3.setText(0, "你的app上线了..")
        child3.setText(1, "昨天")
        child3.setIcon(0, QIcon("static/msg.png"))

        child4 = QTreeWidgetItem(child2)
        child4.setText(0, "修改密码成功..")
        child4.setText(1, "昨天")
        child4.setIcon(0, QIcon("static/msg.png"))

        # 加载根节点的所有属性 与子控件
        self.tree.addTopLevelItem(root)

        # 给节点点击添加响应事件
        self.tree.clicked.connect(self.onClicked)

        # 节点全部展开看
        self.tree.expandAll()

        # 添加到父容器中设置位置
        self.tree.setGeometry(0, 0, 400, 580)

    def onClicked(self, index):
        """
        点击单个选项事件
        :param index:
        :return:
        """
        button = QMessageBox.warning(self, "提示", "是否前去查看?", QMessageBox.Ok | QMessageBox.Cancel, QMessageBox.Ok)
        if button == QMessageBox.Ok:
            item = self.tree.currentItem()  # 获取当前选中的节点
            print("key= %s, vlaue= %s" % (item.text(0), item.text(1)))

    def do_fetch_data(self):
        """
        加载后台数据
        :return:
        """
        self.cur_user_t = getUsrTuples()
        print(self.cur_user_t)

    def showEvent(self, *args, **kwargs):
        """
        显示
        :param args:
        :param kwargs:
        :return:
        """
        print("show...")
        self.do_fetch_data()
        self.lbl_usrname.setText("%s, %s好" % (self.cur_user_t[1], "下午"))

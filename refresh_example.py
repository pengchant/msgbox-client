import sys
import time

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QPushButton


class MyThread(QThread):
    breakSignal = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)

    def run(self):
        for i in range(1, 1000):
            print(i)
            time.sleep(1)
            self.breakSignal.emit(i)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    dlg = QDialog()
    dlg.resize(400, 300)
    dlg.setWindowTitle("自定义按钮测试")
    dlgLayout = QVBoxLayout()
    dlgLayout.setContentsMargins(40, 40, 40, 40)
    btn = QPushButton("测试按钮")
    dlgLayout.addWidget(btn)
    dlgLayout.addStretch(40)
    dlg.setLayout(dlgLayout)
    dlg.show()


    def chuli(a):
        btn.setText(str(a))


    thread = MyThread()
    thread.breakSignal.connect(chuli)
    # 启动线程
    thread.start()
    sys.exit(app.exec_())

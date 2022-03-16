import sys
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QPushButton,QWidget,QMainWindow,QLabel, QLineEdit,QWidget,QVBoxLayout
from mainwindow import Ui_MainWindow
class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.setAcceptDrops(True)

app = QApplication()
window = MainWindow()
window.show()
app.exec_()

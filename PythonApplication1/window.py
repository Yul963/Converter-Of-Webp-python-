import sys
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QPushButton,QWidget,QMainWindow,QLabel, QLineEdit,QWidget,QVBoxLayout
from PySide6.QtCore import Qt
from mainwindow import Ui_MainWindow
import main

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.setAcceptDrops(True)
    def dragEnterEvent(self, e): 
        if e.mimeData().hasUrls: 
            e.accept() 
        else: e.ignore() 
    def dragMoveEvent(self, e): 
        if e.mimeData().hasUrls: 
            e.accept() 
        else: 
            e.ignore() 
    def dropEvent(self, e): 
        if e.mimeData().hasUrls: 
            e.setDropAction(Qt.CopyAction) 
            e.accept()
            for url in e.mimeData().urls(): 
                main.dir(url.toLocalFile())
        else: 
            e.ignore()


app = QApplication()
window = MainWindow()
window.show()
app.exec_()
# -*- coding: utf-8 -*-
import os
import webp
import zip
import sys
import ui2py
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QPushButton,QWidget,QMainWindow,QLabel, QLineEdit,QWidget,QVBoxLayout
from PySide6.QtCore import Qt,QThread, SIGNAL
from mainwindow import Ui_MainWindow
import timeit

def dir(path):
    i = 0
    c=webp.convert
    z=zip.zip
    u=zip.unzip
    o=os.path
    if o.isfile(path):
        name, ext = o.splitext(path)
        file=o.basename(path)
        if ext=='.jpg' or ext=='.png' or ext=='.gif':
            print(file)
            c(path)
        elif ext==".zip":
            if 1==u(path):
                print(file)
                dir(name)
                z(name)
        else:
            print("NOT CONVERTABLE")
    elif o.isdir(path):
        for (path_file, directory, files) in os.walk(path):
                for file in files:
                    path_name, ext = o.splitext(file)
                    if ext=='.jpg' or ext=='.png' or ext=='.gif':
                        print(file)
                        c(path_file+'/'+file)
                        i = i + 1
                    elif ext==".zip":
                        if 1==u(path_file+'/'+file):
                            print(file)
                            dir(path_file+'/'+path_name)
                            z(path_file+'/'+path_name)
                            i = i + 1
                if i==0:
                    print("NO CONVERTABLE FILES IN "+path)

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.setAcceptDrops(True)

    def proc(self, count): 
        print("%f초 걸렸습니다." % (count))

    def button_clicked(self):
        self.textBrowser.append()
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
                self.worker = Worker(self.proc,url.toLocalFile())
                self.worker.start()
        else: 
            e.ignore()

class Worker(QThread): 
    def __init__(self, proc, path): 
        super().__init__()
        self.path=path
        self.proc = proc 
    def run(self): 
        start_time = timeit.default_timer() # 시작 시간 체크
        dir(self.path)
        terminate_time = timeit.default_timer() # 종료 시간 체크
        count=terminate_time - start_time
        self.emit(SIGNAL(self.proc(count)))

app = QApplication()
win = MainWindow()
win.show()
app.exec()
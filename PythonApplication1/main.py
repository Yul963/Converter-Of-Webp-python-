# -*- coding: utf-8 -*-
import os
import webp
import sys
import zip
import ui2py
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QPushButton,QWidget,QMainWindow,QLabel, QLineEdit,QWidget,QVBoxLayout
from PySide6.QtCore import Qt,QThread, SIGNAL
from mainwindow import Ui_MainWindow
import timeit
from queue import Queue

class fileQue():
    def __init__(self):
        self.que = Queue()
    def AddQue(self,path):
        i = 0
        if os.path.isfile(path):
            name, ext = os.path.splitext(path)
            file=os.path.basename(path)
            if ext=='.jpg' or ext=='.png' or ext=='.gif':
                self.que.put(path)
            elif ext==".zip":
                if 1==zip.checkzip(path):
                    self.que.put(path)
            else:
                print("NOT CONVERTABLE")
        elif os.path.isdir(path):
            for (path_file, directory, files) in os.walk(path):
                    for file in files:
                        path_name, ext = os.path.splitext(file)
                        if ext=='.jpg' or ext=='.png' or ext=='.gif':
                            self.que.put(path_file+'/'+file)
                            i = i + 1
                        elif ext==".zip":
                            if 1==zip.checkzip(path_file+'/'+file):
                                self.que.put(path_file+'/'+file)
                                i = i + 1
                    if i==0:
                        print("NO CONVERTABLE FILES IN "+path)

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.setAcceptDrops(True)
        self.fileque = fileQue()
        self.worker = Worker(self.proc,self.fileque.que)
        self.worker.start()
    def proc(self, count): 
        print("%fseconds." % (count))

    def closeEvent(self, e):
        self.hide()
        self.worker.stop()

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
                self.fileque.AddQue(url.toLocalFile())
        else: 
            e.ignore()

class Worker(QThread): 
    def __init__(self, proc, que): 
        super().__init__()
        self.proc = proc
        self.que = que 
    def run(self): 
        i=0
        while(True):
            if (self.que.qsize!=0):
                if (i==0):
                    start_time = timeit.default_timer() # 시작 시간 체크
                    i+=1
                webp.convert(self.que.get())
            if (i==1):
                terminate_time = timeit.default_timer() # 종료 시간 체크
                count=terminate_time - start_time
                self.emit(SIGNAL(self.proc(count)))
                i-=1
    def stop(self):
        self.working = False
        self.quit()
        self.wait(1000)

app = QApplication()
win = MainWindow()
win.show()
app.exec()
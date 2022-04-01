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


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.setWindowIcon(QIcon('ic_baseline_double_arrow_24.xml'))
        self.setAcceptDrops(True)
        self.que = Queue()
        self.worker = Worker(self.append_log,self.que,self.changeStatus)
        self.worker.start()
        self.statusBar().showMessage('Ready')
    def proc(self, count):
        print("%fseconds." % (count))
    def changeStatus(self, status):
        self.statusBar().showMessage(status)
    def append_filetext(self,text):
        self.textBrowser_2.append(text)
    def append_log(self,text):
        self.textBrowser.append(text)
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
                self.AddQue(url.toLocalFile())
        else: 
            e.ignore()
    def AddQue(self,path):
        i = 0
        if os.path.isfile(path):
            name, ext = os.path.splitext(path)
            filename=os.path.basename(path)
            if ext=='.jpg' or ext=='.png' or ext=='.gif':
                self.que.put(path)
                self.textBrowser_2.append(filename)
            elif ext==".zip":
                if 1==zip.checkzip(path):
                    self.que.put(path)
                    self.textBrowser_2.append(filename)
            else:
                self.textBrowser.append("NOT CONVERTABLE")
        elif os.path.isdir(path):
            for (path_file, directory, files) in os.walk(path):
                    for file in files:
                        path_name, ext = os.path.splitext(file)
                        if ext=='.jpg' or ext=='.png' or ext=='.gif':
                            self.que.put(path_file+'/'+file)
                            self.textBrowser_2.append(file)
                            i = i + 1
                        elif ext==".zip":
                            if 1==zip.checkzip(path_file+'/'+file):
                                self.que.put(path_file+'/'+file)
                                self.textBrowser_2.append(file)
                                i = i + 1
                    if i==0:
                        self.textBrowser.append("NO CONVERTABLE FILES IN "+path)

class Worker(QThread): 
    def __init__(self, log, que, status): 
        super().__init__()
        self.log = log
        self.que = que
        self.status = status
    def run(self): 
        i=True
        while(True):
            file=self.que.get()
            if (i):
                start_time = timeit.default_timer() # 시작 시간 체크
                self.emit(SIGNAL(self.status("Working")))
                i=False
            webp.convert(file)
            filename=os.path.basename(file)
            if (self.que.empty()):
                if not (i):
                    terminate_time = timeit.default_timer() # 종료 시간 체크
                    count = terminate_time - start_time
                    self.emit(SIGNAL(self.log(str(count)+'seconds.')))
                    self.emit(SIGNAL(self.status("Ready")))
                    i=True

    def stop(self):
        self.working = False
        self.quit()
        self.wait(1000)

ui2py.py()
app = QApplication()
win = MainWindow()
win.show()
app.exec()
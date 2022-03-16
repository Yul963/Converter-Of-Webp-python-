# -*- coding: utf-8 -*-
import os
import webp
import zip
import sys
import window
import ui2py
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QLabel

def dir(path):
    i = 0
    c=webp.convert
    z=zip.zip
    u=zip.unzip
    o=os.path
    if o.isfile(path):
        name, ext = o.splitext(path)
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

ui2py.py()
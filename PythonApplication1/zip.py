import zipfile
import os
import shutil

def zip(path):#압축할 파일경로 받음
    shutil.make_archive(path,"zip",path)
    shutil.rmtree(path)

def unzip(path):#압축풀 파일 받음
    name, ext = os.path.splitext(path)
    shutil.unpack_archive(path,name)
    os.remove(path)

def checkzip(path):
    my_zip = zipfile.ZipFile(path)
    name, ext = os.path.splitext(path)
    list = my_zip.namelist()
    num=0
    for i in list:
        if not (i.find('.jpg')==-1 and i.find('.png')==-1 and i.find('.gif')==-1):
            num=num+1
    if num==0:
        my_zip.close()
        return 0;
    my_zip.close()
    return 1;
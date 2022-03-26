import os
from PIL import Image
import zip

def convert(path):#변환할 파일 받음
    name, ext = os.path.splitext(path)
    if ext=='.jpg' or ext=='.png':
        im = Image.open(path)
        im.save(name+'.webp','webp',subsampling=0,quality=100)
        im.close()
        os.remove(path)
    elif ext=='.gif':
        im = Image.open(path)
        im.save(name+'.webp','webp',duration=im.info["duration"], save_all=True,subsampling=0,quality=100)
        im.close()
        os.remove(path)
    elif ext==".zip":
        zip.unzip(path)
        for (path_file, directory, files) in os.walk(name):
            for file in files:
                path_name, ext = os.path.splitext(file)
                if ext=='.jpg' or ext=='.png' or ext=='.gif':
                    convert(path_file+'/'+file)
                elif ext==".zip":
                    if 1==zip.checkzip(path_file+'/'+file):
                        convert(path_file+'/'+file)
        zip.zip(name)
        
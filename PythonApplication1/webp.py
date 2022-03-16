import os
from PIL import Image

def convert(path):#변환할 파일 받음
    name, ext = os.path.splitext(path)
    quali = {'quality': 90}
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
    else :
        print("NO CONVERTABLE FILES IN "+path)
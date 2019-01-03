import numpy as np
from jfs.api import Path
import os
from numpy import unicode

def is_file_normal(path):
    # path = unicode(path,'utf8')
    fsize = os.path.getsize(path)
    if fsize/float(1024)>10:
        return True
    else:
        print(path+'is not a normal file!')
        return False

def load_data(path):
    f = open(path,'rb')
    pack = []
    try:
        while True:
            chunk = f.read(1)
            if not chunk:
                break
            pack.append(ord(chunk))
    finally:
        f.close()
    return pack
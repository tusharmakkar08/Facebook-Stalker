

import os
import sys

def getpath(name=None):
    if getattr(sys, '_MEIPASS', None):
        basedir = sys._MEIPASS
    else:
        #basedir = os.path.dirname(__file__)
        basedir = os.getcwd()
        
    if name is None:
        return basedir

    return os.path.join(basedir, name)

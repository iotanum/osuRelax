from ctypes import *
from ctype_structures import POINT


handle = windll.user32.FindWindowW(0, 'osu!')
pos = POINT()


def convert_cords():
    if windll.user32.GetCursorPos(byref(pos)):
        if windll.user32.ScreenToClient(handle, byref(pos)):
            return pos.x, pos.y

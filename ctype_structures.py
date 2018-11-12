from ctypes import *


class RECT(Structure):
    _fields_ = [('left', c_long),
                ('top', c_long),
                ('right', c_long),
                ('bottom', c_long)]


class POINT(Structure):
    _fields_ = [('x', c_long),
                ('y', c_long)]

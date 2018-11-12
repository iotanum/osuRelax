from ctypes import *
from ctypes.wintypes import *


class Win:
    def __init__(self):
        self.PROCESS_VM_READ = 0x0010
        self.PROCESS_ALL_ACCESS = 0x1f0fff
        self.k32 = WinDLL('kernel32')
        self.u32 = WinDLL('user32')
        self.k32.OpenProcess.argtypes = DWORD, BOOL, DWORD
        self.k32.OpenProcess.restype = HANDLE
        self.k32.ReadProcessMemory.argtypes = HANDLE, LPVOID, LPVOID, c_size_t, POINTER(c_size_t)
        self.k32.ReadProcessMemory.restype = BOOL
        self.process_handle = None

    def handles(self, pid):
        self.process_handle = self.k32.OpenProcess(self.PROCESS_ALL_ACCESS, 0, pid)

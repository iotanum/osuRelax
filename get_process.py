import psutil
import sys
import time
from ctypes import *
from ctype_structures import RECT


class FindProcess:
    def __init__(self):
        self.process_name = ""
        self.process_pid = 0
        self.retries = 10  # wait 10s for osu process
        self.window_handle = None
        self.top_window_offset = 29  # if windowed remove bars
        self.bottom_window_offset = 6  # if windowed remove bars
        self.osu_window_width = 0
        self.osu_window_height = 0

    # for future
    def reset(self):
        self.__init__()

    def run(self, process_name):
        self.process_name = process_name
        self.get_pid()

    def get_pid(self):
        while self.retries:
            process_pid = self.find_pid()
            try:
                if process_pid:
                    print(f'Found {self.process_name} process, PID={process_pid}')
                    self.process_pid = process_pid
                    self.retries = None
                else:
                    self.retries -= 1
                    self.wait_for_program()
            finally:
                if self.retries == 0:
                    sys.exit(f"Couldn't find {self.process_name}")

    def find_pid(self):
        for process in psutil.process_iter():
            if process.name() == self.process_name:
                return int(process.pid)

    def wait_for_program(self):
        print(f'waiting for {self.process_name}...')
        time.sleep(1.5)
        self.get_pid()

    def get_window_handle(self):
        self.window_handle = windll.user32.FindWindowW(0, "osu!")
        self.get_window_size()

    def get_window_size(self):
        windll.user32.GetWindowRect(self.window_handle, byref(rect))
        self.osu_window_width = rect.right - rect.left - self.bottom_window_offset
        self.osu_window_height = rect.bottom - rect.top - self.top_window_offset
        print(f'osu! window size: {self.osu_window_width}x{self.osu_window_height}')


rect = RECT()

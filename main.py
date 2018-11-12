from ctypes import *
from get_beatmap_name import GetWindowName
from find_beatmap import BmapHitObject
from key_presses import PressKey, ReleaseKey
from get_process import FindProcess
from find_pattern import Signature
from win32_calls import Win
from convert_mouse_pos import convert_cords
import random

Win32 = Win()
HitObjects = BmapHitObject()
Process = FindProcess()


class Main:
    def __init__(self):
        self.title = ""
        self.proc_name = 'osu!.exe'
        self.PROCESS_ID = None
        self.proc_address = None
        self.beatmap_timer_address = None
        self.lock()
        self.window = dict()
        self.window['title'] = ""
        self.key_to_press = 0x1F
        self.hit_object_counter = 0
        self.bytes_to_read = 4
        self.buf = create_string_buffer(self.bytes_to_read)
        self.s = c_size_t()
        self.sig = 0x1555ba0
        self.standard_width = 576
        self.standard_height = 432

    def lock(self):
        Process.run(self.proc_name)
        self.PROCESS_ID = Process.process_pid
        Win32.handles(self.PROCESS_ID)
        self.beatmap_timer_address = Signature.find_address(Win32)
        Process.get_window_handle()

    def stuff(self):
        while True:
            if self.check_map():
                try:
                    if self.window['title'] == self.title:
                        if Win32.k32.ReadProcessMemory(Win32.process_handle, self.beatmap_timer_address, self.buf,
                                                       self.bytes_to_read, byref(self.s)):
                            mem_offset = int.from_bytes(self.buf.raw, byteorder='little')
#                            print(' '.join('%02X' % x for x in self.buf.raw), f"@ {self.beatmap_timer_address}")
                            bmap_offset = int(HitObjects.hit_objects[0 + self.hit_object_counter].split(",")[2])
                            next_note = int(HitObjects.hit_objects[0 + self.hit_object_counter + 1].split(",")[2])
#                            x, y = self.conv_hitobject_x_y(self.get_hitobject_x_y(
#                                HitObjects.hit_objects[0 + self.hit_object_counter]))
#                            mouse_x, mouse_y = convert_cords()
                            if mem_offset - random.randint(5, 30) <= bmap_offset <= mem_offset + random.randint(5, 30):
#                                Win32.u32.SetCursorPos(x, y)
                                PressKey(self.key_to_press)
                            elif mem_offset - random.randint(5, 25) <= next_note <= mem_offset + random.randint(5, 25):
                                ReleaseKey(self.key_to_press)
                                print(f"note @ {self.buf.raw.hex()}")
                                self.hit_object_counter += 1
                        else:
                            print(Win32.process_handle, self.beatmap_timer_address, self.buf, self.bytes_to_read,
                                  byref(self.s))
                            print(Win32.k32.GetLastError())
                except IndexError:
                    continue

    def check_map(self):
        title = GetWindowName().song_name()
        if self.window['title'] != title:
            self.window['title'] = title
            if title != "Main Menu":
                self.title = title
                self.hit_object_counter = 0
                self.parse_hitobjects()
                print(f"Loaded map: '{self.window['title']}', hit objects: {len(HitObjects.hit_objects)}")
                return True
            else:
                self.title = "get off"
                print("Main Menu")
        else:
            return True

    def parse_hitobjects(self):
        HitObjects.beatmap_file(self.title)

    def conv_hitobject_x_y(self, xy):
        x, y = xy
        object_x_offset = Process.osu_window_width - self.standard_width
        object_y_offset = Process.osu_window_height - self.standard_height
        return x + object_x_offset, y + object_y_offset

    def get_hitobject_x_y(self, line):
        x = int(line.split(",")[0])
        y = int(line.split(",")[1])
        return x, y


a = Main()
a.stuff()

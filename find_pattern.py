from ctypes import *
import time


class Pattern:
    def __init__(self):
        self.pattern = [0x44, 0x2C, 0x47, 0x00, 0x44, 0x2C, 0x47]
        self.pattern_address = None
        self.address_offset_offset = -33  # relative to the pattern
        self.bytes_to_read = 50  # 'chunk' to read before incrementing
        self.buf = create_string_buffer(self.bytes_to_read)  # C magic
        self.s = c_size_t()  # C magic
        self.initial_address = 0x00A10000  # random for the time being
        self.scanning = True
        self.offset_inc = 10  # offset to add when searching for pattern bytes

    def find_address(self, Win32):
        print("Searching for the signature..")
        while self.scanning:
            if Win32.k32.ReadProcessMemory(Win32.process_handle, self.initial_address, self.buf,
                                           self.bytes_to_read, byref(self.s)):
                mem_bytes = " ".join(str(x) for x in list(self.buf.raw))
                pattern_bytes = " ".join(str(x) for x in self.pattern)
                if pattern_bytes in mem_bytes:
                    for idx, byte in enumerate(list(self.buf.raw)):
                        if self.pattern[0] == byte:
                            offset_to_pattern = idx
                            self.pattern_address = self.initial_address + offset_to_pattern + self.address_offset_offset
                            print('Found! Address in memory:', hex(self.pattern_address))
                            self.scanning = False
                            time.sleep(2)
                            return self.pattern_address
                else:
                    self.initial_address = self.initial_address + self.offset_inc
            else:
                self.initial_address = self.initial_address + self.offset_inc
#                sys.exit(f"Couldn't scan osu!'s memory, try again. Error {Win32.k32.GetLastError()}")


Signature = Pattern()

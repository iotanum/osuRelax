import os


class BmapHitObject:
    def __init__(self):
        self.section = ""
        self.hit_objects = []
        self.slider_multiplier = None

    def reset(self):
        self.__init__()

    def beatmap_file(self, diff_name):
        dire = self.find_beatmap_dir(diff_name)
        self.find_hitobject(dire)

    def find_beatmap_dir(self, diff_name):
        diff_name = self.strip_name(diff_name)
        for directory in os.walk(r"C:\Users\Evaldas\AppData\Local\osu!\Songs"):
            if diff_name[0] in str(directory):
                for file in directory[2]:
                    if all(str(_) in str(file) for _ in diff_name):
                        folder, _, file_list = directory
                        return folder + "\\" + file

    def strip_name(self, diff_name):
        strip_chars = ['*', '/', ">", "<", "=", "^", "?"]
        for char in strip_chars:
            diff_name = diff_name.replace(char, "")
        return diff_name.split(" ")

    def find_hitobject(self, beatmap_file_dir):
        self.hit_objects = []
        with open(beatmap_file_dir, 'r', encoding='utf8') as f:
            for idx, line in enumerate(f.readlines()):
                line = line.strip()

                if line.startswith("["):
                    section = line[1:-1]
                    continue

                if line == 'HitObjects':
                    section = 'HitObjects'
                    continue

                if line.startswith("SliderMultiplier:"):
                    self.slider_multiplier = float(line[17:])

                try:
                    if section == 'HitObjects':
                        self.hit_objects.append(line[:-1])
                except (ValueError, UnboundLocalError):
                    continue

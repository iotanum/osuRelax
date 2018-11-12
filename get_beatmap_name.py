import win32gui


class GetWindowName:
    def enum_window_titles(self):
        def callback(handle, data):
            titles.append(win32gui.GetWindowText(handle))

        titles = []
        win32gui.EnumWindows(callback, None)
        return titles

    def find_osu_window_name(self, titles):
        for title in titles:
            if title.startswith('osu!  - '):
                return title

    def parse_window_title(self):
        titles = self.enum_window_titles()
        title = self.find_osu_window_name(titles)
        return title

    def song_name(self):
        title = self.parse_window_title()
        try:
            return title[8:]
        except TypeError:
            return "Main Menu"

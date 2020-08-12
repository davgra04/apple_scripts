from curses import wrapper
import curses
import os
import subprocess
import time


class display:

    DEFAULT_WIDTH = 63
    HEADER_ELEMENTS = ["==", "--", "==", "~~"]
    TITLE = "Wallpaper Changer"
    CONTROLS = ["SPACE / RIGHT ARROW - Next wallpaper", "Q - Quit"]

    def __init__(self, screen):
        self.update_width(screen)
        self.prep_display()
        self.height = len(self.lines)
        self.count = -1
        self.color = curses.has_colors()

    def generate_title_bar(self):
        halfbar = ""
        for i in range(self.width // 4):
            halfbar += self.HEADER_ELEMENTS[i % 4]

        gap = ""
        if self.width % 2 == 1:
            gap = " "

        return "{:s}{:s}{:s}".format(halfbar, gap, halfbar[::-1])

    def prep_display(self):
        self.lines = list()
        self.lines.append(self.generate_title_bar())
        self.lines.append(
            "{}{}".format((self.width // 2 - len(self.TITLE) // 2) * " ", self.TITLE)
        )
        self.lines.append(self.generate_title_bar())
        self.lines.append("")
        self.lines.append("COUNT_BAR")
        self.lines.append("")
        for c in self.CONTROLS:
            hypen_loc = c.find("-")
            self.lines.append("{}{}".format((self.width // 2 - hypen_loc - 1) * " ", c))

    def update_width(self, screen):
        _, w = screen.getmaxyx()
        self.width = min(self.DEFAULT_WIDTH, w)
        self.prep_display()

    def print_count_bar(self, screen, y, x):

        box_count = (self.width - 6) // 2
        # end_gap_width = (self.width - 6) % 2
        end_gap_width = 0

        screen.addstr(y, x, " [ ")
        for b in range(box_count):
            if b < self.count % (box_count) + 1 and self.count > -1:
                if self.color:
                    screen.addstr("+", curses.color_pair(b % 6 + 1))
                else:
                    screen.addstr("+")
                screen.addstr(" ")
            else:
                screen.addstr("  ")

        screen.addstr("{}]".format(" " * end_gap_width))

    def print_to_screen(self, screen):
        try:
            h, w = screen.getmaxyx()

            for i, l in enumerate(self.lines):
                y = h // 2 - self.height // 2 + i
                x = w // 2 - self.width // 2
                y = min(max(y, 0), h - 1)
                x = max(x, 0)
                if l == "COUNT_BAR":
                    self.print_count_bar(screen, y, x)
                else:
                    screen.addnstr(y, x, l, w)

        except curses.error:
            pass


def change_all_wallpapers(basepath):
    scriptpath = os.path.join(basepath, "change_all_wallpapers.scpt")
    subprocess.call(
        ["osascript", scriptpath,]
    )


def curses_loop(screen):
    k = None
    d = display(screen)
    basepath = os.path.dirname(os.path.realpath(__file__))

    last_wp_change_time = 0
    change_threshold = (
        0.5  # minimum number of seconds to wait between wallpaper changes
    )

    if curses.has_colors() and curses.can_change_color():
        curses.use_default_colors()

        color_cycle = [
            curses.COLOR_CYAN,
            curses.COLOR_MAGENTA,
            curses.COLOR_BLUE,
            curses.COLOR_YELLOW,
            curses.COLOR_GREEN,
            curses.COLOR_RED,
        ]

        for i, c in enumerate(color_cycle):
            curses.init_pair(i + 1, curses.COLOR_WHITE, c)

    while True:

        screen.clear()
        d.print_to_screen(screen)

        # screen.addstr(0, 0, "last key pressed: {}".format(k))

        if k == "q":
            # quit
            break
        elif k == " " or k == "KEY_RIGHT":
            # change wallpapers if past threshold
            if time.time() > last_wp_change_time + change_threshold:
                # screen.addstr(1, 0, "changing wallpapers".format(k))
                d.count += 1
                d.print_to_screen(screen)
                # DO IT
                change_all_wallpapers(basepath)
                last_wp_change_time = time.time()
        elif k == "KEY_RESIZE":
            # resize screen
            d.update_width(screen)
            d.print_to_screen(screen)

        screen.refresh()

        try:
            k = screen.getkey()
        except curses.error:
            pass


def main():
    try:
        wrapper(curses_loop)
    except KeyboardInterrupt as e:  # don't dump stack trace on Ctrl+C
        pass


if __name__ == "__main__":
    main()

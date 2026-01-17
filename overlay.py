import pygame
import win32api
import win32gui
import win32con
import sys
from constants import INDEX_TIP_IDX, SCREEN_WIDTH, SCREEN_HEIGHT

FUCHSIA = (255, 0, 128)


class Overlay():
    def __init__(self):
        pygame.init()
        width = win32api.GetSystemMetrics(0)
        height = win32api.GetSystemMetrics(1)
        self.screen = pygame.display.set_mode((width, height), pygame.NOFRAME)
        window = pygame.display.get_wm_info()["window"]
        ex_style = win32gui.GetWindowLong(window, win32con.GWL_EXSTYLE)
        ex_style |= win32con.WS_EX_LAYERED | win32con.WS_EX_TOPMOST
        win32gui.SetWindowLong(window, win32con.GWL_EXSTYLE, ex_style)
        win32gui.SetLayeredWindowAttributes(
            window, win32api.RGB(*FUCHSIA), 0, win32con.LWA_COLORKEY)
        win32gui.SetWindowPos(window, win32con.HWND_TOPMOST, 0, 0, 0, 0,
                              win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_SHOWWINDOW)

        pygame.display.set_caption("Pinch OS overlay")

        self.clock = pygame.time.Clock()
        self.running = True

    def getwindows(self):
        list = []

        def callback(hwnd, ctx):
            if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd) != "":
                title = win32gui.GetWindowText(hwnd)
                left, top, right, bottom = win32gui.GetWindowRect(hwnd)
                width = right - left
                height = bottom - top

                if (width, height) == (SCREEN_WIDTH, SCREEN_HEIGHT):
                    return
                list.append({
                    'window': hwnd,
                    'title': title,
                    'position': (left, top),
                    'dimensions': (width, height)
                })
            return True
        win32gui.EnumWindows(callback, None)
        return list

    def draw_windows(self):
        windows = self.getwindows()
        foreground = win32gui.GetForegroundWindow()
        for window in windows:
            hwnd = window['window']
            if hwnd == foreground:
                x, y = window['position']
                w, h = window['dimensions']
                pygame.draw.rect(self.screen, (0, 255, 0), (x, y, w, h), 3)

    def draw_pointer(self, points, w, h):
        ix, iy = points[INDEX_TIP_IDX]
        monitor_coordinates = (ix/w*SCREEN_WIDTH, iy/h*SCREEN_HEIGHT)
        pygame.draw.circle(self.screen, (0, 255, 0), monitor_coordinates, 8, 2)

    def mainloop(self, pointer_points=None, w=None, h=None):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                self.running = False
        self.screen.fill(FUCHSIA)
        self.draw_windows()
        if len(pointer_points) is not 0 and w is not None and h is not None:
            self.draw_pointer(pointer_points, w, h)
        pygame.display.update()
        self.clock.tick(60)

    def quit():
        pygame.quit()
        sys.exit()

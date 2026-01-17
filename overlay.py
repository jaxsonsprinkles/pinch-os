import pygame
import win32api
import win32gui
import win32con
import sys
from screeninfo import get_monitors

SCREEN_WIDTH, SCREEN_HEIGHT = get_monitors()[0].width, get_monitors()[0].height


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
        self.window_list = []

        def callback(window, ctx):
            if win32gui.IsWindowVisible(window) and win32gui.GetWindowText(window) != "":
                title = win32gui.GetWindowText(window)
                left, top, right, bottom = win32gui.GetWindowRect(window)
                width = right - left
                height = bottom - top

                if (width, height) == (SCREEN_WIDTH, SCREEN_HEIGHT):
                    return
                self.window_list.append({
                    'window': window,
                    'title': title,
                    'position': (left, top),
                    'dimensions': (width, height)
                })
            return True
        win32gui.EnumWindows(callback, None)
        return self.window_list

    def mainloop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                self.running = False
        self.screen.fill(FUCHSIA)
        surf = pygame.Surface((200, 200), pygame.SRCALPHA)
        pygame.draw.circle(surf, (0, 255, 0, 150), (100, 100), 80)
        self.screen.blit(surf, (100, 100))

        pygame.display.update()
        self.clock.tick(60)

    def quit():
        pygame.quit()
        sys.exit()

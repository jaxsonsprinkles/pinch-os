import pygame
import win32api
import win32gui
import win32con
import sys
from constants import INDEX_TIP_IDX, SCREEN_WIDTH, SCREEN_HEIGHT
import time

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
        self.smoothed_pos = None
        self.smoothed_alpha = 0.35
        self.windows = self.getwindows()
        self.current_window = None
        self.window_rect_list = []
        self.pointer_rect = None
        self.last_pointer_pos = None

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
                    'hwnd': hwnd,
                    'title': title,
                    'position': (left, top),
                    'dimensions': (width, height)
                })
            return True
        win32gui.EnumWindows(callback, None)

        # Sort
        win_map = {w['hwnd']: w for w in list}
        ordered = []
        hw = win32gui.GetTopWindow(None)
        while hw:
            if hw in win_map:
                ordered.append(win_map[hw])
            hw = win32gui.GetWindow(hw, win32con.GW_HWNDNEXT)

        return ordered

    def draw_windows(self):
        self.window_rect_list = []
        for i, window in enumerate(self.windows[:3]):
            x, y = window['position']
            w, h = window['dimensions']
            self.window_rect_list.append(pygame.Rect(x, y, w, h))
            pygame.draw.rect(self.screen, (0, 255, 0), (x, y, w, h), 3)

    def draw_pointer(self, points, w, h):
        ix, iy = points[INDEX_TIP_IDX]
        monitor_coords = (int(ix/w*SCREEN_WIDTH), int(iy/h*SCREEN_HEIGHT))
        if self.smoothed_pos is None:
            self.smoothed_pos = monitor_coords
        else:
            # Exponential smoothing
            self.smoothed_pos = (int(self.smoothed_alpha*monitor_coords[0]+(1-self.smoothed_alpha)*self.smoothed_pos[0]), int(
                self.smoothed_alpha*monitor_coords[1]+(1-self.smoothed_alpha)*self.smoothed_pos[1]))
        pygame.draw.circle(self.screen, (0, 255, 0), self.smoothed_pos, 8, 2)
        self.pointer_rect = pygame.Rect(self.smoothed_pos, (16, 16))

    def move_window(self, hwnd):

        window = next(
            (item for item in self.windows if item["hwnd"] == hwnd), None)
        w, h = window['dimensions']
        px, py = self.pointer_rect.x, self.pointer_rect.y
        dx, dy = self.pointer_delta

        if "drag_pos" not in window:
            window["drag_pos"] = list(window["position"])

        window["drag_pos"][0] += dx
        window["drag_pos"][1] += dy

        win32gui.SetWindowPos(
            hwnd, None,
            window["drag_pos"][0], window["drag_pos"][1],
            w, h,
            win32con.SWP_NOZORDER | win32con.SWP_NOACTIVATE
        )

    def mainloop(self, pointer_points=None, w=None, h=None):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                self.running = False

        self.windows = self.getwindows()
        self.screen.fill(FUCHSIA)
        self.draw_windows()
        if len(pointer_points) != 0 and w is not None and h is not None:
            self.draw_pointer(pointer_points, w, h)
            # in mainloop, after draw_pointer
            if self.last_pointer_pos:
                self.pointer_delta = (
                    self.pointer_rect.x - self.last_pointer_pos[0],
                    self.pointer_rect.y - self.last_pointer_pos[1]
                )
            else:
                self.pointer_delta = (0, 0)

            self.last_pointer_pos = (self.pointer_rect.x, self.pointer_rect.y)

            idx = self.pointer_rect.collidelist(self.window_rect_list)
            if idx != -1:
                self.current_window = self.windows[idx]
            else:
                self.current_window = None

        pygame.display.update()
        self.clock.tick(60)

    def quit():
        pygame.quit()
        sys.exit()

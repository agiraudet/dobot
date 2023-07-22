import time
import pyautogui


class Region:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def show(self, delay=0):
        pyautogui.moveTo(self.x, self.y)
        time.sleep(delay)
        pyautogui.moveTo(self.x + self.w, self.y)
        time.sleep(delay)
        pyautogui.moveTo(self.x + self.w, self.y + self.h)
        time.sleep(delay)
        pyautogui.moveTo(self.x, self.y + self.h)

    def set(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def print(self):
        print("x:{} y:{} w:{} h:{}".format(self.x, self.y, self.w, self.h))

    def screenshot(self, save=''):
        if len(save) > 0:
            print("f[RG]Saved {save}")
            return pyautogui.screenshot(save, region=(
                self.x,
                self.y,
                self.w,
                self.h
            ))
        else:
            return pyautogui.screenshot(region=(
                self.x,
                self.y,
                self.w,
                self.h
            ))

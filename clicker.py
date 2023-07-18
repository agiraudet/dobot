#!/usr/bin/python3

import pyautogui
import time


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


class Game:
    def __init__(self):
        discoLoc = pyautogui.locateOnScreen('beacons/disco_btn.png')
        chatLoc = pyautogui.locateOnScreen('beacons/chat_btn.png')
        if discoLoc is None or chatLoc is None:
            discoLoc = pyautogui.locateOnScreen('beacons/disco_btn_big.png')
            chatLoc = pyautogui.locateOnScreen('beacons/chat_btn_big.png')
        if discoLoc is None or chatLoc is None:
            raise Exception("Could not locate game window")
        self.region = Region(
            x=(chatLoc.left),
            y=(discoLoc.top),
            w=((discoLoc.left + discoLoc.width) - chatLoc.left),
            h=(chatLoc.top - discoLoc.top)
        )


try:
    game = Game()
except Exception as e:
    print(e)
    exit(1)

game.region.show(1)

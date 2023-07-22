import cv2
import numpy
import pyautogui
import random

from Region import Region


class Landmark:

    def __init__(
        self,
        region,
        imagePath,
        hideSprite=False,
        threshold=0.5,
        log=False,
        name='landmark',
        offsetX=0,
        offsetY=0,
        delayMouse=(0.2, 1.)  # Set to None for no delay
    ):
        self.region = region
        self.beacon = cv2.imread(imagePath, 0)
        self.threshold = threshold
        self.hideSprite = hideSprite
        self.log = log
        self.name = name
        self.offsetX = offsetX
        self.offsetY = offsetY
        self.delayMouse = delayMouse
        self.pos = None
        self.fullPos = Region(0, 0, 0, 0)

    def find(self):
        if self.hideSprite:
            pyautogui.keyDown('e')
        sc = self.region.screenshot()
        if self.hideSprite:
            pyautogui.keyUp('e')
        scGray = cv2.cvtColor(numpy.array(sc), cv2.COLOR_RGB2GRAY)
        result = cv2.matchTemplate(scGray, self.beacon, cv2.TM_CCOEFF_NORMED)
        minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(result)
        if maxVal < self.threshold:
            if self.log:
                print(f"{self.name} {maxVal} KO")
            self.pos = None
            return False
        if self.log:
            print(f"{self.name} {maxVal} OK")
        self.fullPos.set(
            maxLoc[0],
            maxLoc[1],
            self.beacon.shape[0],
            self.beacon.shape[1])
        centerX = (maxLoc[0] + self.beacon.shape[1] // 2) + \
            self.region.x + self.offsetX
        centerY = (maxLoc[1] + self.beacon.shape[0] // 2) + \
            self.region.y + self.offsetY
        self.pos = (centerX, centerY)
        return True

    def clickOn(self, forgetAfterClick=True):
        if self.pos is None:
            self.find()
        if self.pos is not None:
            if self.delayMouse is not None:
                pyautogui.moveTo(self.pos[0], self.pos[1], random.uniform(
                    self.delayMouse[0], self.delayMouse[1]), pyautogui.easeOutQuad)
            pyautogui.click(self.pos[0], self.pos[1])
            if forgetAfterClick:
                self.pos = None
            return True
        return False

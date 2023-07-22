import cv2
import numpy
import pyautogui
import random

from Region import Region
import colorTerm as ct


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
        delayMouse=(0.2, 1.),  # Set to None for no delay
        randomize=False
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
        self.randomize = randomize

    def logConfidence(self, maxVal):
        color = ct.GREEN
        if maxVal < self.threshold:
            color = ct.RED
        confidence = f"{ct.BOLD}{color}{maxVal*100: .2f}%{ct.RESET}"
        ct.announce(f"{self.name} {confidence}", ct.GREEN, "Farmer")

    def setPos(self):
        if self.randomize:
            posX = (self.fullPos.x
                    + random.randint(1, self.beacon.shape[1] - 1)
                    + self.region.x + self.offsetX)
            posY = (self.fullPos.y
                    + random.randint(1, self.beacon.shape[0] - 1)
                    + self.region.y + self.offsetY)
            self.pos = (posX, posY)
        else:
            # Switched shape[0] and shape[1], in case of trouble, switch back.
            centerX = (self.fullPos.x + self.beacon.shape[1] // 2) + \
                self.region.x + self.offsetX
            centerY = (self.fullPos.y + self.beacon.shape[0] // 2) + \
                self.region.y + self.offsetY
            self.pos = (centerX, centerY)

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
                self.logConfidence(maxVal)
            self.pos = None
            return False
        if self.log:
            self.logConfidence(maxVal)
        self.fullPos.set(
            maxLoc[0],
            maxLoc[1],
            self.beacon.shape[0],
            self.beacon.shape[1])
        self.setPos()
        return True

    def clickOn(self, forgetAfterClick=True):
        if self.pos is None:
            self.find()
        if self.pos is not None:
            x, y = self.pos
            if self.randomize:
                x += random.randint(-3, 3)
                y += random.randint(-3, 3)
            if self.delayMouse is not None:
                pyautogui.moveTo(x,
                                 y,
                                 random.uniform(
                                     self.delayMouse[0], self.delayMouse[1]),
                                 pyautogui.easeOutQuad)
            pyautogui.click(x, y)
            if forgetAfterClick:
                self.pos = None
            return True
        return False

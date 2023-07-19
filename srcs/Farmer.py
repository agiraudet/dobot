import cv2
import numpy
import pyautogui
import random
import time


class Farmer:
    def __init__(self, game, resFile, collectFile, delay, delayAddMax=1.):
        print("[Farmer]Init...")
        self.game = game
        self.readyBeac = cv2.imread('beacons/btn/ready.png', 0)
        self.collectBeac = cv2.imread(collectFile, 0)
        self.resBeac = cv2.imread(resFile, 0)
        self.delayMin = delay
        self.delayMax = delay + delayAddMax
        self.threshold = 0.5

    def lookFor(self, beacon):
        sc = self.game.region.screenshot()
        scGray = cv2.cvtColor(numpy.array(sc), cv2.COLOR_RGB2GRAY)
        result = cv2.matchTemplate(scGray, beacon, cv2.TM_CCOEFF_NORMED)
        minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(result)
        print(maxVal)
        if maxVal < self.threshold:
            return False
        centerX = (maxLoc[0] + beacon.shape[1] // 2) + self.game.region.x
        centerY = (maxLoc[1] + beacon.shape[0] // 2) + self.game.region.y
        pyautogui.moveTo(centerX, centerY,
                         random.uniform(0.2, 1.), pyautogui.easeOutQuad)
        pyautogui.click(centerX, centerY)
        return True

    def collect(self):
        print('res')
        self.lookFor(self.resBeac)
        print('action')
        self.lookFor(self.collectBeac)

    def checkFight(self):
        print('fight')
        if self.lookFor(self.readyBeac):
            print('[Farmer]Fight detected')
            return False
        return True

    def farm(self):
        try:
            while self.checkFight():
                if self.collect():
                    time.sleep(random.uniform(self.delayMin, self.delayMax))
        except KeyboardInterrupt:
            return

import cv2
import numpy
import pyautogui
import random
import time
import eye


class Farmer:
    def __init__(self, game, fighter, resFile, collectFile, delay, delayAddMax=1.):
        print("[Farmer]Init...")
        self.game = game
        self.fighter = fighter
        self.readyBeac = cv2.imread('beacons/btn/ready.png', 0)
        self.collectBeac = cv2.imread(collectFile, 0)
        self.resBeac = cv2.imread(resFile, 0)
        self.delayMin = delay
        self.delayMax = delay + delayAddMax
        self.threshold = 0.5

    # def lookFor(self, beacon, hideSprite=False, threshold=0.5, log=False, logName=''):
    #     if hideSprite:
    #         pyautogui.keyDown('e')
    #     sc = self.game.region.screenshot()
    #     if hideSprite:
    #         pyautogui.keyUp('e')
    #     scGray = cv2.cvtColor(numpy.array(sc), cv2.COLOR_RGB2GRAY)
    #     result = cv2.matchTemplate(scGray, beacon, cv2.TM_CCOEFF_NORMED)
    #     minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(result)
    #     if maxVal < threshold:
    #         if log:
    #             print(f"{logName} {maxVal} KO")
    #         return False
    #     if log:
    #         print(f"{logName} {maxVal} OK")
    #     centerX = (maxLoc[0] + beacon.shape[1] // 2) + self.game.region.x
    #     centerY = (maxLoc[1] + beacon.shape[0] // [b]2) + self.game.region.y
    #     pyautogui.moveTo(centerX, centerY,
    #                      random.uniform(0.2, 1.), pyautogui.easeOutQuad)
    #     pyautogui.click(centerX, centerY)
    #     return True

    def collect(self):
        # self.lookFor(self.resBeac, log=True, logName='res:', threshold=0.4)
        # return self.lookFor(self.collectBeac, threshold=0.9)
        eye.lookFor(self.resBeac, self.game.region, threshold=0.4)
        return eye.lookFor(self.collectBeac, self.game.region, threshold=0.9)

    def checkFight(self):
        # if self.lookFor(self.readyBeac):
        if eye.lookFor(self.resBeac, self.game.region):
            print('[Farmer]Fight detected')
            if self.fighter is not None:
                self.fighter.fight()
                print('[Farmer]Resuming farming')
            return True
        return False

    def farm(self):
        print("[Farmer]Starting farming...")
        try:
            while True:
                self.checkFight()
                if self.collect():
                    time.sleep(random.uniform(self.delayMin, self.delayMax))
        except KeyboardInterrupt:
            print("[Farmer]Ctrl+C interrupt")
            return


import cv2
import numpy
import pyautogui
import random
import time


class Fighter:
    def __init__(self, game, spellSlot):
        print("[Fighter]Init...")
        self.game = game
        # self.readyBeac = cv2.imread('beacons/btn/ready.png', 0)
        self.mobBeac = cv2.imread('beacons/fight/mob.png', cv2.IMREAD_COLOR)
        self.threshold = 0.2
        self.spell = spellSlot

    def lookFor(self, beacon):
        sc = self.game.region.screenshot()
        sc = numpy.array(sc)
        sc[:, :, 0] = 0
        sc[0, :, :] = 0
        result = cv2.matchTemplate(sc, beacon, cv2.TM_CCORR_NORMED)
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

    def fight(self):
        try:
            while True:
                self.lookFor(self.mobBeac)
                time.sleep(1)
        except KeyboardInterrupt:
            return

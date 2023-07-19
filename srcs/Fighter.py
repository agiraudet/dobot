
import cv2
import numpy
import pyautogui
import random
import time

import utils


class Fighter:
    def __init__(self, game, spellSlot, spellTries):
        print("[Fighter]Init...")
        self.game = game
        self.threshold = 0.88
        self.eyeBeac = cv2.imread('beacons/fight/eye.png', 0)
        self.finishedBeac = cv2.imread('beacons/fight/end.png', 0)
        self.tlBeac = cv2.imread('beacons/fight/tl.png', 0)
        self.challBeac = cv2.imread('beacons/fight/chall.png', 0)
        self.spell = spellSlot
        self.spellTries = spellTries
        self.mobLowHSV = (50, 200, 200)
        self.mobHighHSV = (150, 255, 255)
        self.plrLowHSV = (0, 200, 200)
        self.plrHighHSV = (3, 255, 255)
        self.maxMoveTries = 5
        self.timerPos = self.findTimerPos()

    def findTimerPos(self):
        timerBeac = cv2.imread('beacons/fight/timer.png', 0)
        sc = self.game.guiRegion.screenshot()
        scGray = cv2.cvtColor(numpy.array(sc), cv2.COLOR_RGB2GRAY)
        result = cv2.matchTemplate(scGray, timerBeac, cv2.TM_CCOEFF_NORMED)
        minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(result)
        centerX = (maxLoc[0] + timerBeac.shape[0] // 2)
        centerY = (maxLoc[1] + timerBeac.shape[1] // 2)
        return (centerX, centerY)

    def findCharPos(self, lowHSV, highHSV):
        pyautogui.moveTo(self.game.guiRegion.x + self.timerPos[0],
                         self.game.guiRegion.y + self.timerPos[1],
                         random.uniform(0.02, 0.05), pyautogui.easeOutQuad)
        sc = self.game.region.screenshot()
        hsv = cv2.cvtColor(numpy.array(sc), cv2.COLOR_RGB2HSV)
        mask = cv2.inRange(hsv, lowHSV, highHSV)
        contours, _ = cv2.findContours(
            mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # cv2.imshow("Mask", mask)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        cMax = -1
        c = None
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > cMax:
                cMax = area
                c = contour
        if c is None:
            return None
        M = cv2.moments(c)
        if M["m00"] != 0:
            centerX = int(M["m10"] / M["m00"])
            centerY = int(M["m01"] / M["m00"])
            centerX += self.game.region.x
            centerY += self.game.region.y
            # pyautogui.moveTo(centerX, centerY, random.uniform(
            #     0.2, 0.5), pyautogui.easeOutQuad)
            return (centerX, centerY)
        return None

    def movePossible(self, pos):
        pyautogui.moveTo(pos[0], pos[1])
        sc = self.game.region.screenshot()
        pix = sc.getpixel((pos[0] - self.game.region.x,
                          pos[1] - self.game.region.y))
        if pix[0] > 245:
            return True
        return False

    def moveIncPos(self, pos, plrPos, mobPos):
        posX = pos[0]
        posY = pos[1]
        if mobPos[0] - plrPos[0] < 0:
            posX -= self.game.cellW / 2
        else:
            posX += self.game.cellW / 2
        if mobPos[1] - plrPos[1] < 0:
            posY -= self.game.cellH / 2
        else:
            posY += self.game.cellH / 2
        return (posX, posY)

    def move(self):
        plrPos = self.findCharPos(self.plrLowHSV, self.plrHighHSV)
        mobPos = self.findCharPos(self.mobLowHSV, self.mobHighHSV)
        if plrPos is None or mobPos is None:
            return
        okMoves = plrPos
        pyautogui.moveTo(plrPos[0], plrPos[1])
        cursPos = self.moveIncPos(plrPos, plrPos, mobPos)
        for i in range(self.maxMoveTries):
            cursPos = self.moveIncPos(cursPos, plrPos, mobPos)
            if self.movePossible(cursPos):
                okMoves = cursPos
        pyautogui.click(okMoves[0], okMoves[1])
        time.sleep(random.uniform(1., 1.5))

    def moveAround(self):
        plrPos = self.findCharPos(self.plrLowHSV, self.plrHighHSV)
        mobPos = self.findCharPos(self.mobLowHSV, self.mobHighHSV)
        if plrPos is None or mobPos is None:
            return
        pyautogui.moveTo(plrPos[0], plrPos[1])
        mobRelPos = (mobPos[0] - self.game.region.x,
                     mobPos[1] - self.game.region.y)
        bestPos = self.findBestMove(mobRelPos)
        if bestPos is not None:
            pyautogui.click(
                bestPos[0] + self.game.region.x,
                bestPos[1] + self.game.region.y
            )

    def findBestMove(self, mobRelPos, min_contour_area=50):
        lowHSV = (62, 85, 35)
        highHSV = (68, 100, 140)
        sc = self.game.region.screenshot()
        hsv = cv2.cvtColor(numpy.array(sc), cv2.COLOR_RGB2HSV)
        mask = cv2.inRange(hsv, lowHSV, highHSV)
        contours, _ = cv2.findContours(
            mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        mob_center_x, mob_center_y = mobRelPos
        closest_contour = None
        closest_distance = float('inf')
        for contour in contours:
            area = cv2.contourArea(contour)
            if area < min_contour_area:
                continue
            M = cv2.moments(contour)
            contour_center_x = int(M["m10"] / M["m00"])
            contour_center_y = int(M["m01"] / M["m00"])
            distance = numpy.sqrt((mob_center_x - contour_center_x)
                                  ** 2 + (mob_center_y - contour_center_y)**2)
            if distance < closest_distance:
                closest_contour = contour
                closest_distance = distance
        if closest_contour is not None:
            M = cv2.moments(closest_contour)
            closest_center_x = int(M["m10"] / M["m00"])
            closest_center_y = int(M["m01"] / M["m00"])
            return closest_center_x, closest_center_y
        else:
            return None

    def lookFor(self, beacon, offsetX=0, offsetY=0):
        sc = self.game.region.screenshot()
        scGray = cv2.cvtColor(numpy.array(sc), cv2.COLOR_RGB2GRAY)
        result = cv2.matchTemplate(scGray, beacon, cv2.TM_CCOEFF_NORMED)
        minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(result)
        if maxVal < self.threshold:
            return False
        centerX = (maxLoc[0] + beacon.shape[1] // 2) + \
            self.game.region.x + offsetX
        centerY = (maxLoc[1] + beacon.shape[0] // 2) + \
            self.game.region.y + offsetY
        pyautogui.moveTo(centerX, centerY,
                         random.uniform(0.2, 1.), pyautogui.easeOutQuad)
        pyautogui.click(centerX, centerY)
        return True

    def clickMob(self):
        pos = self.findCharPos(self.mobLowHSV, self.mobHighHSV)
        if pos is None:
            return
        pyautogui.moveTo(pos[0], pos[1], random.uniform(
            0.2, 0.5), pyautogui.easeOutQuad)
        pyautogui.click(pos[0], pos[1])

    def launchSpell(self):
        pyautogui.keyDown(self.spell)
        time.sleep(random.uniform(0.01, 0.03))
        pyautogui.keyUp(self.spell)
        self.clickMob()
        time.sleep(random.uniform(0.8, 1.2))

    def waitForNextTurn(self):
        while True:
            if self.lookFor(self.finishedBeac):
                return False
            sc = self.game.guiRegion.screenshot()
            pix = sc.getpixel(self.timerPos)
            if pix[0] > 245:
                return True
            time.sleep(0.05)

    def minimizeGui(self):
        self.lookFor(self.eyeBeac, self.eyeBeac.shape[0] * -2)
        time.sleep(random.uniform(0.01, 0.03))
        self.lookFor(self.tlBeac)
        time.sleep(random.uniform(0.01, 0.03))
        self.lookFor(self.challBeac)
        time.sleep(random.uniform(0.01, 0.03))

    def fight(self):
        print("[Fighter]Started fight")
        self.moveAround()
        exit()
        self.minimizeGui()
        pyautogui.moveTo(self.game.region.x + self.game.region.w / 2,
                         self.game.region.y + self.game.region.h / 2)
        try:
            while self.waitForNextTurn():
                print('[Fighter]New turn')
                self.move()
                for n in range(self.spellTries):
                    self.launchSpell()
                    time.sleep(random.uniform(0.2, 0.5))
                pyautogui.keyDown('f1')
                time.sleep(random.uniform(0.01, 0.03))
                pyautogui.keyUp('f1')
            print("[Fighter]Finished fight")
            return
        except KeyboardInterrupt:
            print("[Fighter]Ctrl+C interrupt")
            return

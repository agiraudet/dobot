import time
import random
import pyautogui

from Landmark import Landmark
from ColorMask import ColorMask
import colorTerm as ct


class Fighter:
    def __init__(self, game, spellSlot, spellTries):
        ct.announce("Init..", ct.RED, "Fighter")
        self.game = game
        self.spriteBtn = Landmark(
            game.regionMap['game'],
            'beacons/fight/eye.png',
            threshold=0.7,
            name="eyeBtn")
        self.spriteBtn.offsetX = self.spriteBtn.beacon.shape[0] * -2
        self.finishBtn = Landmark(
            game.regionMap['game'],
            'beacons/fight/end.png',
            threshold=0.8,
            name="endBtn")
        self.tlBtn = Landmark(
            game.regionMap['game'],
            'beacons/fight/tl.png',
            threshold=0.8,
            name="tlBtn")
        self.challBtn = Landmark(
            game.regionMap['game'],
            'beacons/fight/chall.png',
            threshold=0.8,
            name="challBtn")
        self.timer = Landmark(
            game.regionMap['gui'],
            'beacons/fight/timer.png',
            threshold=0.4,
            name="timer")
        self.spell = spellSlot
        self.spellTries = spellTries
        self.moveMask = ColorMask(
            game.regionMap['game'], (62, 85, 35), (68, 100, 140))
        self.plrMask = ColorMask(
            game.regionMap['game'], (0, 200, 200), (3, 255, 255))
        self.mobMask = ColorMask(
            game.regionMap['game'], (50, 200, 200), (150, 255, 255))

    def fight(self):
        ct.announce("Started fight", ct.RED, "Fighter")
        self.setupGui()
        try:
            while self.waitForNextTurn():
                ct.announce("New turn", ct.RED, "Fighter")
                self.move()
                time.sleep(random.uniform(1., 1.3))
                for n in range(self.spellTries):
                    ct.printc(f"Spell {self.spell} {n+1}/{self.spellTries}",
                              ct.RED,
                              "Fighter")
                    self.lauchSpell()
                    time.sleep(random.uniform(1.7, 2.))
                pyautogui.press('f1')
            ct.announce("Ended fight", ct.RED, "Fighter")
            return
        except KeyboardInterrupt:
            ct.announce("Interrupted", ct.RED, "Fighter")
            return

    def setupGui(self):
        ct.announce("Setting up GUI", ct.RED, "Fighter")
        self.timer.find()
        self.timerPos = (
            self.timer.pos[0] - self.game.regionMap['gui'].x,
            self.timer.pos[1] - self.game.regionMap['gui'].y
        )
        self.spriteBtn.clickOn()
        time.sleep(random.uniform(0.01, 0.1))
        self.tlBtn.clickOn()
        time.sleep(random.uniform(0.01, 0.1))
        self.challBtn.clickOn()
        time.sleep(random.uniform(0.01, 0.1))

    def waitForNextTurn(self):
        while True:
            if self.finishBtn.clickOn():
                return False
            sc = self.game.regionMap['gui'].screenshot()
            pix = sc.getpixel(self.timerPos)
            if pix[0] > 245:
                return True
            time.sleep(random.uniform(0.01, 0.1))

    def move(self):
        plrPos = self.plrMask.findMainColorPos()
        mobPos = self.mobMask.findMainColorPos()
        if plrPos is None or mobPos is None:
            return
        pyautogui.moveTo(plrPos[0], plrPos[1])
        bestMoves = self.moveMask.findClosestToPoint(
            mobPos, minArea=50)
        if bestMoves is not None:
            ct.announce("Moving", ct.RED, "Fighter")
            for m in bestMoves:
                pyautogui.moveTo(m[0], m[1])
                mousePos = pyautogui.position()
                sc = pyautogui.screenshot(
                    region=(mousePos[0] - 2,
                            mousePos[1] - 2,
                            1,
                            1))
                pix = sc.getpixel((0, 0))
                if pix[0] > 245:
                    pyautogui.click(m[0], m[1])
                    return

    def clickMob(self):
        mobPos = self.mobMask.findMainColorPos()
        if mobPos is not None:
            pyautogui.moveTo(mobPos[0], mobPos[1], random.uniform(
                0.1, 0.3), pyautogui.easeOutQuad)
            time.sleep(random.uniform(0.04, 0.09))
            pyautogui.click(mobPos[0], mobPos[1])

    def lauchSpell(self):
        pyautogui.keyDown(self.spell)
        time.sleep(random.uniform(0.1, 0.4))
        pyautogui.keyUp(self.spell)
        self.clickMob()
        pyautogui.moveTo(self.timerPos[0] - 10,
                         self.timerPos[1] - 10,
                         random.uniform(0.1, 0.3),
                         pyautogui.easeOutQuad)

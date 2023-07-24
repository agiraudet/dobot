import random
import time
import pyautogui

from Landmark import Landmark
import colorTerm as ct


class Farmer:
    def __init__(self, game, job, resFile, actFile, routine=None):
        ct.announce("Init...", ct.GREEN, "Farmer")
        self.game = game
        self.job = job
        self.routine = routine
        if routine is not None:
            self.routine.delayMouse = (0.8, 1.2)
        try:
            self.rdyBtn = Landmark(
                game.regionMap['game'],
                'beacons/btn/ready.png',
                threshold=0.8,
                name='ready')
            self.action = Landmark(
                game.regionMap['game'],
                actFile,
                threshold=game.getConf('jobs', job, 'action', 'threshold'),
                log=game.getConf('jobs', job, 'action', 'log'),
                name='collect')
            self.ressource = Landmark(
                game.regionMap['game'],
                resFile,
                threshold=game.getConf('jobs', job, 'ressource', 'threshold'),
                log=game.getConf('jobs', job, 'ressource', 'log'),
                randomize=True,
                checkMirror=game.getConf(
                    'jobs', job, 'ressource', 'checkMirror'),
                name='ressource')
            self.delay = (game.getConf('jobs', job, 'delay', 'min'),
                          game.getConf('jobs', job, 'delay', 'max'))
        except KeyError as e:
            ct.announce(f"{ct.RED}{e}{ct.RESET}", ct.RED, "Error")
            exit(1)
        self.count = 0
        self.fail = 0
        self.routineStepThreshold = 5

    def collect(self):
        self.ressource.clickOn()
        collected = self.action.clickOn()
        if collected:
            self.count += 1
            return True
        else:
            if self.fail == 3:
                self.game.focusRegion('game')
                pyautogui.press('enter')
            if self.fail >= self.routineStepThreshold \
                    and self.routine is not None:
                self.fail = 0
                self.routine.nextStep(replay=True)
                time.sleep(3)
            else:
                self.fail += 1
            return False

    def checkFight(self):
        if self.rdyBtn.clickOn():
            ct.announce("Fight detected", ct.GREEN, "Farmer")
            return True
        return False

    def printCount(self):
        ct.announce(f"collected {self.count} times.", ct.GREEN, "Farmer")

    def farm(self):
        ct.announce("Started farming", ct.GREEN, "Farmer")
        while True:
            if self.checkFight():
                return True
            if self.collect():
                time.sleep(random.uniform(self.delay[0], self.delay[1]))
        return False

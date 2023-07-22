import random
import time

from Landmark import Landmark
import colorTerm as ct


class Farmer:
    def __init__(self, game, resFile, actFile, delayFarm=(2.5, 3.)):
        ct.announce("Init...", ct.GREEN, "Farmer")
        self.game = game
        self.rdyBtn = Landmark(
            game.regionMap['game'],
            'beacons/btn/ready.png',
            threshold=0.8,
            name='readyBtn')
        self.action = Landmark(
            game.regionMap['game'],
            actFile,
            threshold=0.8,
            log=True,
            name='collectBtn')
        self.ressource = Landmark(
            game.regionMap['game'],
            resFile,
            threshold=0.4,
            log=True,
            name='ressource')
        self.delay = delayFarm
        self.count = 0

    def collect(self):
        self.ressource.clickOn()
        collected = self.action.clickOn()
        if collected:
            self.count += 1
            return True
        else:
            return False

    def checkFight(self):
        if self.rdyBtn.clickOn():
            ct.announce("Fight detected", ct.GREEN, "Farmer")
            return True
        return False

    def printCount(self):
        ct.announce(f"collected {self.count} times.", ct.GREEN, "Farmer")

    def farm(self):
        print("[Farmer]Starting farming...")
        ct.announce("Started farming", ct.GREEN, "Farmer")
        while True:
            if self.checkFight():
                return True
            if self.collect():
                time.sleep(random.uniform(self.delay[0], self.delay[1]))
        return False

import random
import time

from Landmark import Landmark
import colorTerm as ct


class Farmer:
    def __init__(self, game, job, resFile, actFile):
        ct.announce("Init...", ct.GREEN, "Farmer")
        self.game = game
        self.job = job
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
                name='ressource')
            self.delay = (game.getConf('jobs', job, 'delay', 'min'),
                          game.getConf('jobs', job, 'delay', 'max'))
        except KeyError as e:
            ct.announce(f"{ct.RED}{e}{ct.RESET}", ct.RED, "Error")
            exit(1)
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

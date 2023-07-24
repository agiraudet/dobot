import pyautogui
import json

from Region import Region
from Landmark import Landmark


class Game:
    def __init__(self):
        self.regionMap = {}
        self.regionMap['global'] = self.createGlobalRegion()
        self.regionMap['game'] = self.createGameRegion()
        self.regionMap['coord'] = self.createCoordRegion()
        self.regionMap['gui'] = self.createGuiRegion()
        self.cellW = self.regionMap['game'].w / 28
        self.cellH = self.regionMap['game'].h / 34
        self.loadConf()

    def loadConf(self):
        with open('conf.json', 'r') as confFile:
            self.conf = json.load(confFile)

    def getConf(self, *args):
        return self.recConf(self.conf, *args)

    def recConf(self, confData, *args):
        if len(args) == 0:
            return confData
        elif len(args) == 1:
            return confData[args[0]]
        else:
            if args[0] not in confData:
                raise KeyError(f"{args[0]} not in conf.json")
            else:
                return self.recConf(confData[args[0]], *args[1:])

    def createGlobalRegion(self):
        size = pyautogui.size()
        return Region(
            x=0,
            y=0,
            w=size[0],
            h=size[1],
        )

    def createGameRegion(self):
        discoBtn = Landmark(
            self.regionMap['global'],
            'beacons/btn/disco_btn.png',
            threshold=0.8,
            name='discoBtn',
        )
        chatBtn = Landmark(
            self.regionMap['global'],
            'beacons/btn/chat_btn.png',
            threshold=0.8,
            name='chatBtn',
        )
        discoBtn.find()
        chatBtn.find()
        if discoBtn.pos is None or chatBtn.pos is None:
            raise RuntimeError(
                "Could not locate game window.\nCheck that the game is open, visible, and that your are logged in.")
        return Region(
            x=chatBtn.fullPos.x,
            y=discoBtn.fullPos.y,
            w=discoBtn.fullPos.x + discoBtn.fullPos.w - chatBtn.fullPos.x,
            h=chatBtn.fullPos.y - discoBtn.fullPos.y
        )

    def createCoordRegion(self):
        return Region(
            x=self.regionMap['game'].w / 80 + self.regionMap['game'].x,
            y=self.regionMap['game'].h / 13 + self.regionMap['game'].y,
            w=self.regionMap['game'].w / 5,
            h=self.regionMap['game'].h / 20
        )

    def createGuiRegion(self):
        return Region(
            x=self.regionMap['game'].x,
            y=self.regionMap['game'].y + self.regionMap['game'].h,
            w=self.regionMap['game'].w,
            h=self.regionMap['game'].h / 2
        )

    def focusRegion(self, regionName):
        region = self.regionMap[regionName]
        if region is not None:
            pyautogui.moveTo(region.x + region.w / 2,
                             region.y + region.h / 2)

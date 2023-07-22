import pyautogui

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
            raise Exception("Could not locate game window")
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

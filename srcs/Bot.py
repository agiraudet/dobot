import os
import glob

from Game import Game
from Pilot import Pilot
from Fighter import Fighter
from Farmer import Farmer
import colorTerm as ct


class Bot:
    def __init__(self):
        try:
            self.game = Game()
        except Exception as e:
            ct.printc(e, ct.RED)
            exit(1)

    def initModes(self):
        self.pilot = Pilot(self.game)
        self.fighter = Fighter(self.game, '1', 2)

    def banner(self):
        clr = ct.YELLOW
        ct.printc("██████╗  ██████╗ ██████╗  ██████╗ ████████╗", clr)
        ct.printc("██╔══██╗██╔═══██╗██╔══██╗██╔═══██╗╚══██╔══╝", clr)
        ct.printc("██║  ██║██║   ██║██████╔╝██║   ██║   ██║", clr)
        ct.printc("██║  ██║██║   ██║██╔══██╗██║   ██║   ██║", clr)
        ct.printc("██████╔╝╚██████╔╝██████╔╝╚██████╔╝   ██║", clr)
        ct.printc("╚═════╝  ╚═════╝ ╚═════╝  ╚═════╝    ╚═╝", clr)

    def displayMenu(self, menuTitle, optionList, color):
        nOpt = "├"
        lastOpt = "└"
        dash = "─"
        i = 1
        ct.printc(menuTitle, ct.BOLD + color)
        for opt in optionList:
            if i < len(optionList):
                bullet = nOpt
            else:
                bullet = lastOpt
            ct.printc(f"{bullet}{dash}{i}{dash} {opt}", color)
            i += 1
        while True:
            x = input("> ")
            try:
                xi = int(x) - 1
                if xi >= len(optionList) or xi < 0:
                    raise ValueError("out of range")
                return xi
            except ValueError:
                ct.printc("Not a valid input", ct.RED)

    def getPngFiles(self, path):
        pngFiles = []
        for filePath in glob.glob(os.path.join(path, '*.png')):
            fileNameFull = os.path.basename(filePath)
            fileName, _ = os.path.splitext(fileNameFull)
            if fileName != 'act':
                pngFiles.append(fileName)
        return pngFiles

    def getDirList(self, path):
        subdirectories = [subdir for subdir in os.listdir(
            path) if os.path.isdir(os.path.join(path, subdir))]
        return subdirectories

    def farmingMenu(self):
        basePath = "beacons/job/"
        jobList = self.getDirList(basePath)
        x = self.displayMenu("Pick a job", jobList)
        job = jobList[x]
        action = basePath + job + "/act.png"
        resList = self.getPngFiles(basePath + job)
        x = self.displayMenu("Pick a ressource", resList)
        res = basePath + job + '/' + resList[x] + '.png'
        return Farmer(self.game, res, action)

    def start(self):
        self.banner()
        self.initModes()
        self.menu()

    def menu(self):
        while True:
            x = self.displayMenu("What do you want to do ?",
                                 ["Farm",
                                  "GoTo",
                                  "Fight",
                                  "Exit"],
                                 ct.YELLOW)
            if x == 0:
                farmer = self.farmingMenu()
                try:
                    while True:
                        if farmer.farm():
                            self.fighter.fight()
                except KeyboardInterrupt:
                    ct.announce("Stopped Farming", ct.GREEN, "Farmer")
                    farmer.printCount()

            elif x == 1:
                self.pilot.menu()
            elif x == 2:
                self.fighter.fight()
            elif x == 3:
                exit(0)

import os
import glob

from Game import Game
from Pilot import Pilot
from Fighter import Fighter
from Farmer import Farmer
import colorTerm as ct


class Bot:
    def __init__(self):
        self.conf = None
        try:
            self.game = Game()
        except Exception as e:
            ct.announce(f"{ct.RED}{e}{ct.RESET}", ct.RED, "Error")
            exit(1)

    def initModes(self):
        self.pilot = Pilot(self.game)
        self.fighter = Fighter(self.game, '1', 2)

    def banner(self):
        clr = ct.YELLOW
        ct.printc("\n██████╗  ██████╗ ██████╗  ██████╗ ████████╗", clr)
        ct.printc("██╔══██╗██╔═══██╗██╔══██╗██╔═══██╗╚══██╔══╝", clr)
        ct.printc("██║  ██║██║   ██║██████╔╝██║   ██║   ██║", clr)
        ct.printc("██║  ██║██║   ██║██╔══██╗██║   ██║   ██║", clr)
        ct.printc("██████╔╝╚██████╔╝██████╔╝╚██████╔╝   ██║", clr)
        ct.printc("╚═════╝  ╚═════╝ ╚═════╝  ╚═════╝    ╚═╝", clr)

    def displayMenu(self, menuTitle, optionList, color, tabs=0):
        nOpt = "├"
        lastOpt = "└"
        dash = "─"
        i = 1
        tabsLine = ''
        tabsSpace = ''
        if tabs > 0:
            tabsLine = tabs * ' ' + lastOpt + dash
            tabsSpace = (tabs + 2) * ' '
        ct.printc(f"{tabsLine}{menuTitle}", ct.BOLD + color)
        for opt in optionList:
            if i < len(optionList):
                bullet = nOpt
            else:
                bullet = lastOpt
            ct.printc(f"{tabsSpace}{bullet}{dash}{i}{dash} {opt}", color)
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
        x = self.displayMenu("Pick a job", jobList, ct.GREEN, tabs=2)
        job = jobList[x]
        action = basePath + job + "/act.png"
        resList = self.getPngFiles(basePath + job)
        x = self.displayMenu("Pick a ressource", resList, ct.GREEN, tabs=4)
        res = basePath + job + '/' + resList[x] + '.png'
        return Farmer(self.game, job, res, action)

    def addWaypoint(self, tabs=0):
        tabSpace = ' ' * tabs
        x = input(ct.BLUE + tabSpace + '└─X: ' + ct.RESET)
        y = input(ct.BLUE + tabSpace + '└─Y: ' + ct.RESET)
        return int(x), int(y)

    def pilotMenu(self):
        waypoints = []
        i = 0
        x = 0
        while x != 1:
            print(x)
            i += 1
            ct.printc(f"Point {i}:", ct.BLUE)
            waypoints.append(self.addWaypoint(tabs=4))
            x = self.displayMenu(
                "What's next ?", ["Add waypoint", "Start running"], ct.BLUE, tabs=4)
        self.pilot.start(waypoints)

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
                self.pilotMenu()
                # self.pilot.menu()
            elif x == 2:
                self.fighter.fight()
            elif x == 3:
                exit(0)

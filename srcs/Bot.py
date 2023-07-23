import os
import glob

from Game import Game
from Pilot import Pilot
from Fighter import Fighter
from Farmer import Farmer
from Routine import RoutineMaster
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
        self.rtMaster = RoutineMaster(self.game.regionMap['game'])

    def banner(self):
        clr = ct.YELLOW
        ct.printc("\n██████╗  ██████╗ ██████╗  ██████╗ ████████╗", clr)
        ct.printc("██╔══██╗██╔═══██╗██╔══██╗██╔═══██╗╚══██╔══╝", clr)
        ct.printc("██║  ██║██║   ██║██████╔╝██║   ██║   ██║", clr)
        ct.printc("██║  ██║██║   ██║██╔══██╗██║   ██║   ██║", clr)
        ct.printc("██████╔╝╚██████╔╝██████╔╝╚██████╔╝   ██║", clr)
        ct.printc("╚═════╝  ╚═════╝ ╚═════╝  ╚═════╝    ╚═╝", clr)

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
        x = ct.displayMenu("Pick a job", jobList, ct.GREEN, tabs=2)
        job = jobList[x]
        action = basePath + job + "/act.png"
        resList = self.getPngFiles(basePath + job)
        x = ct.displayMenu("Pick a ressource", resList, ct.GREEN, tabs=4)
        res = basePath + job + '/' + resList[x] + '.png'
        x = ct.displayMenu("Add a routine ?", ["y", "n"], ct.GREEN, tabs=6)
        rt = None
        if x == 0:
            rt = self.rtMaster.selectRoutine(tabs=8)
        return Farmer(self.game, job, res, action, rt)

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
            x = ct.displayMenu(
                "What's next ?", ["add waypoint", "start running"], ct.BLUE, tabs=4)
        self.pilot.start(waypoints)

    def routineMenu(self):
        x = ct.displayMenu("What about routines ?",
                           ["new",
                            "run",
                            "delete"],
                           ct.MAGENTA,
                           tabs=2)
        if x == 0:
            self.rtMaster.newRoutine()
        elif x == 1:
            rt = self.rtMaster.selectRoutine(tabs=4)
            if rt is not None:
                rt.doAllSteps(delay=5)
        else:
            rt = self.rtMaster.selectRoutine(tabs=4)
            if rt is not None:
                self.rtMaster.deleteRoutineByName(rt.name)

    def start(self):
        self.banner()
        self.initModes()
        self.menu()

    def menu(self):
        while True:
            x = ct.displayMenu("What do you want to do ?",
                               ["farm",
                                "goTo",
                                "fight",
                                "routine",
                                "exit"],
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
                self.routineMenu()
            else:
                exit(0)

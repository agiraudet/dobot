import pyautogui
import cv2
import numpy
import time

from Coord import Coord
import colorTerm as ct


class Pilot:
    def __init__(self, game):
        ct.announce("Init...", ct.BLUE, "Pilot")
        self.game = game
        self.coord = Coord(game.regionMap['coord'])
        self.histo = []
        self.realCoord = []
        self.waypoints = []
        self.curX = 0
        self.curY = 0

    def init(self):
        oldX, oldY = pyautogui.position()
        pyautogui.moveTo(self.game.regionMap['game'].x
                         + self.game.regionMap['game'].w / 2,
                         self.game.regionMap['game'].y
                         + self.game.regionMap['game'].h / 2)
        if self.coord.readCoord() is None:
            ct.announce("Cant read start coords", ct.BLUE, "Pilot")
        else:
            self.curX, self.curY = self.coord.coord
            ct.announce(f"Init at {self.coord.coord}", ct.BLUE, "Pilot")
            self.histo = []
            self.realCoord = []
        pyautogui.moveTo(oldX, oldY)

    def group_pixels(self, points, radius):
        grouped_points = []
        while len(points) > 0:
            p1 = points.pop(0)
            group = [p1]
            i = 0
            while i < len(group):
                p = group[i]
                j = 0
                while j < len(points):
                    q = points[j]
                    dist = numpy.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)
                    if dist <= radius:
                        group.append(points.pop(j))
                    else:
                        j += 1
                i += 1
            if len(group) > 0:
                group_x, group_y = zip(*group)
                avg_x = int(sum(group_x) / len(group))
                avg_y = int(sum(group_y) / len(group))
                grouped_points.append((avg_x, avg_y))
        return grouped_points

    def locateCompasses(self):
        pyautogui.keyDown('e')
        scr1 = self.game.regionMap['game'].screenshot()
        pyautogui.keyUp('e')
        pyautogui.press('a')
        time.sleep(1)
        pyautogui.keyDown('e')
        scr2 = self.game.regionMap['game'].screenshot()
        pyautogui.keyUp('e')
        sc1 = numpy.array(scr1)
        sc2 = numpy.array(scr2)
        gray1 = cv2.cvtColor(sc1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(sc2, cv2.COLOR_BGR2GRAY)
        diff = cv2.absdiff(gray1, gray2)
        threshold = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)[1]
        whitish_mask = cv2.inRange(sc2, (200, 200, 200), (255, 255, 255))
        threshold[whitish_mask == 0] = 0
        contours, _ = cv2.findContours(
            threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        middle_points = []
        for contour in contours:
            M = cv2.moments(contour)
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                middle_points.append((cX, cY))
        radius = max(self.game.cellW + 10, self.game.cellH + 10)
        return self.group_pixels(middle_points, radius)

    def findCompassDir(self, compass):
        if compass[1] < self.game.cellH * 2.1:
            return 'N'
        if compass[1] > self.game.regionMap['game'].h - self.game.cellH * 2.1:
            return 'S'
        if compass[0] < self.game.cellW * 2.1:
            return 'W'
        if compass[0] > self.game.regionMap['game'].w - self.game.cellW * 2.1:
            return 'E'
        return '?'

    def checkCurCoord(self):
        if self.coord.coord is None:
            if self.coord.readCoord() is None:
                return False
        if self.coord.coord[0] != self.curX or self.coord.coord[1] != self.curY:
            ct.announce(
                f"Read {self.coord.coord}, exepected {self.curX, self.curY}",
                ct.BLUE,
                "Pilot")
            self.realCoord.append(self.coord.coord)
            if len(self.realCoord) >= 3:
                self.correctCoord()
        else:
            ct.announce(
                f"Believes to be at ({self.curX}, {self.curY})", ct.BLUE, "Pilot")
            self.realCoord = []
        return True

    def correctCoord(self):
        for i in range(1, len(self.realCoord)):
            diffX = abs(self.realCoord[i-1][0] - self.realCoord[i][0])
            diffY = abs(self.realCoord[i-1][1] - self.realCoord[i][1])
            if diffX > 1 or diffY > 1 or (diffX >= 1 and diffY >= 1):
                print("[AP]Removing odd values from RC")
                del self.realCoord[0]
                print(self.realCoord)
                return
        ct.announce(
            f"Correcting coord from ({self.curX}, {self.curY}) to {self.realCoord[-1]}",
            ct.BLUE,
            "Pilot")
        self.curX = self.realCoord[-1][0]
        self.curY = self.realCoord[-1][1]
        self.realCoord = []

    def getDirPrio(self, dir):
        dirPrios = {
            'N': ['N', 'E', 'W', 'S'],
            'E': ['E', 'S', 'N', 'W'],
            'S': ['S', 'W', 'E', 'N'],
            'W': ['W', 'N', 'S', 'E']
        }
        return (dirPrios[dir])

    def getOppDir(self, dir):
        oppDir = {
            'N': 'S',
            'S': 'N',
            'E': 'W',
            'W': 'E'
        }
        return oppDir[dir]

    def updateState(self, dir):
        self.histo.append(dir)
        if dir == 'N':
            self.curY -= 1
        elif dir == 'S':
            self.curY += 1
        elif dir == 'W':
            self.curX -= 1
        elif dir == 'E':
            self.curX += 1

    def gotoDir(self, compass, dir):
        self.updateState(dir)
        pyautogui.keyDown('e')
        pyautogui.click(self.game.regionMap['game'].x +
                        compass[0], self.game.regionMap['game'].y + compass[1])
        pyautogui.keyUp('e')
        self.coord.waitForChange()
        self.checkCurCoord()

    def goto(self, dir):
        comp = self.locateCompasses()
        compMap = {}
        for c in comp:
            compMap[self.findCompassDir(c)] = c
        dirPrio = self.getDirPrio(dir)
        for d in dirPrio:
            if len(self.histo) > 1 and d == self.getOppDir(self.histo[-1]):
                continue
            if d in compMap:
                self.gotoDir(compMap[d], d)
                return True
        ct.announce("Seems stuck", ct.BLUE, "Pilot")
        return False

    def chooseDir(self, toX, toY):
        diffX = abs(toX - self.curX)
        diffY = abs(toY - self.curY)
        if diffX > diffY:
            if (toX > self.curX):
                return 'E'
            else:
                return 'W'
        else:
            if (toY > self.curY):
                return 'S'
            else:
                return 'N'

    def navigateTo(self, toX, toY):
        ct.announce(f"Set to ({toX}, {toY})", ct.BLUE, "Pilot")
        while self.curY != toY or self.curX != toX:
            dir = self.chooseDir(toX, toY)
            if self.goto(dir) is False:
                return False
        ct.announce('>>>> Arrived to waypoint', ct.BLUE, "Pilot")
        ct.announce(f"{self.histo}", ct.BLUE, "Pilot")
        return True

    def menu(self):
        self.init()
        print('##### AutoPilot targeting #####')
        i = 0
        while True:
            print(f'| Point {i}:')
            i += 1
            x = input('| x> ')
            y = input('| y> ')
            self.waypoints.append((int(x), int(y)))

            m = ' '
            while m != 'A' and m != 'a' and m != 'G' and m != 'g':
                m = input("| (A)dd waypoint/(G)o> ")
            if m == 'g' or m == 'G':
                break
        print(f"| {i} Waypoints.")
        print('###############################')
        pyautogui.moveTo(self.game.regionMap['game'].x
                         + self.game.regionMap['game'].w / 2,
                         self.game.regionMap['game'].y
                         + self.game.regionMap['game'].h / 2)
        for wp in self.waypoints:
            if self.navigateTo(wp[0], wp[1]) is False:
                return False
        return True

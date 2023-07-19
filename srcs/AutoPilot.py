import pyautogui


class AutoPilot:
    def __init__(self, game):
        print("[AP]Init...")
        self.game = game
        self.setCurCoord()
        self.histo = []
        self.realCoord = []
        self.waypoints = []

    def setCurCoord(self):
        coord = self.game.lookatCoord()
        if coord is None:
            raise Exception("Could not find current coordinates")
        self.curX = coord[0]
        self.curY = coord[1]
        print(f"[AP]Started at ({coord[0]}, {coord[1]})")

    def checkCurCoord(self):
        coord = self.game.lookatCoord()
        if coord is None:
            return 0
        if coord[0] != self.curX or coord[1] != self.curY:
            print(
                f"[AP]Real Coords seems to be {coord}, expected {self.curX, self.curY}")
            self.realCoord.append(coord)
            if len(self.realCoord) >= 3:
                self.correctCoord()
        else:
            self.realCoord = []

        return 1

    def correctCoord(self):
        for i in range(1, len(self.realCoord)):
            diffX = abs(self.realCoord[i-1][0] - self.realCoord[i][0])
            diffY = abs(self.realCoord[i-1][1] - self.realCoord[i][1])
            if diffX > 1 or diffY > 1 or (diffX >= 1 and diffY >= 1):
                print("[AP]Removing odd values from RC")
                del self.realCoord[0]
                print(self.realCoord)
                return
        print(
            f"[AP]Correcting coord from ({self.curX}, {self.curY}) to {self.realCoord[-1]}")
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
        pyautogui.click(self.game.region.x +
                        compass[0], self.game.region.y + compass[1])
        pyautogui.keyUp('e')
        self.game.waitForMapChange()
        print(f"[AP]believes to be at ({self.curX}, {self.curY})")
        self.checkCurCoord()

    def goto(self, dir):
        comp = self.game.locateCompasses()
        compMap = {}
        for c in comp:
            compMap[self.game.findCompassDir(c)] = c
        dirPrio = self.getDirPrio(dir)
        for d in dirPrio:
            if len(self.histo) > 1 and d == self.getOppDir(self.histo[-1]):
                continue
            if d in compMap:
                self.gotoDir(compMap[d], d)
                return True
        print("[AP]Seems stucked:")
        print(self.histo)
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
        print(f"[AP] Set to ({toX}, {toY})")
        while self.curY != toY or self.curX != toX:
            dir = self.chooseDir(toX, toY)
            if self.goto(dir) is False:
                return False
        print('[AP]>>>> Arrived to waypoint')
        print(self.histo)
        return True

    def menu(self):
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
        for wp in self.waypoints:
            if self.navigateTo(wp[0], wp[1]) is False:
                exit(1)
        exit(0)

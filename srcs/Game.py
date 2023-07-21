import pyautogui
import numpy
import time
import cv2
import pytesseract
import re

from Region import Region


class Game:
    def __init__(self):
        print("[Game]Init...")
        discoLoc = pyautogui.locateOnScreen('beacons/btn/disco_btn.png')
        chatLoc = pyautogui.locateOnScreen('beacons/btn/chat_btn.png')
        if discoLoc is None or chatLoc is None:
            discoLoc = pyautogui.locateOnScreen(
                'beacons/btn/disco_btn_big.png')
            chatLoc = pyautogui.locateOnScreen(
                'beacons/btn/chat_btn_big.png')
        if discoLoc is None or chatLoc is None:
            raise Exception("Could not locate game window")
        self.region = Region(
            x=(chatLoc.left),
            y=(discoLoc.top),
            w=((discoLoc.left + discoLoc.width) - chatLoc.left),
            h=(chatLoc.top - discoLoc.top)
        )
        self.coordRegion = self.initCoordRegion()
        self.guiRegion = self.findGUI()
        self.cellW = self.region.w / 28
        self.cellH = self.region.h / 34

    def initCoordRegion(self):
        return Region(
            x=self.region.w / 80 + self.region.x,
            y=self.region.h / 13 + self.region.y,
            w=self.region.w / 5,
            h=self.region.h / 20
        )

    def findGUI(self):
        return Region(
            x=self.region.x,
            y=self.region.y + self.region.h,
            w=self.region.w,
            h=self.region.h / 2
        )

    def translateCoord(self, text):
        # pattern = r"(-?\d+,\s*\d+)"
        pattern = r"(-?\d+,\s*-?\d+)"
        matches = re.findall(pattern, text)
        if len(matches) != 1:
            return None
        coord = matches[0].split(',')
        return (int(coord[0]), int(coord[1]))

    def readCoord(self):
        lowHSV = (0, 0, 125)
        highHSV = (50, 35, 255)
        sc = self.coordRegion.screenshot()
        hsv = cv2.cvtColor(numpy.array(sc), cv2.COLOR_RGB2HSV)
        mask = cv2.inRange(hsv, lowHSV, highHSV)
        # cv2.imshow("Mask", mask)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        text = pytesseract.image_to_string(mask, config='--psm 6')
        print(text)
        return self.translateCoord(text)

    def lookatCoord(self):
        coord_capt = self.coordRegion.screenshot()
        coord_array = numpy.array(coord_capt)
        grayscale_image = cv2.cvtColor(coord_array, cv2.COLOR_RGB2GRAY)
        threshold_value = 220
        _, thresholded_image = cv2.threshold(
            grayscale_image, threshold_value, 255, cv2.THRESH_BINARY)
        black_bg = numpy.zeros_like(coord_array)
        black_bg[thresholded_image >
                 0] = coord_array[thresholded_image > 0]
        coord_pic = cv2.cvtColor(black_bg, cv2.COLOR_BGR2GRAY)
        text = pytesseract.image_to_string(coord_pic, config='--psm 6')
        return self.translateCoord(text)

    def pointToCell(self, cellX, cellY):
        coordY = self.cellH * cellY + self.cellH / 2
        coordX = self.cellW * cellX + self.cellW / 2
        pyautogui.moveTo(self.region.x + coordX, self.region.y + coordY)

    def gotoCell(self, cellX, cellY):
        coordY = self.cellH * cellY + self.cellH / 2
        coordX = self.cellW * cellX + self.cellW / 2
        pyautogui.keyDown('e')
        pyautogui.click(self.region.x + coordX, self.region.y + coordY)
        pyautogui.keyUp('e')

    def printCell(self):
        pos = pyautogui.position()
        x = pos[0] - self.region.x
        y = pos[1] - self.region.y
        cellX = round(x / self.cellW + y / self.cellH)
        cellY = round(y / self.cellH - x / self.cellW)
        print(f"Cell {cellX, cellY}")

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
        pyautogui.moveTo(self.region.x + self.region.w / 2,
                         self.region.y + self.region.h / 2)
        pyautogui.keyDown('e')
        scr1 = self.region.screenshot()
        pyautogui.keyUp('e')
        pyautogui.press('a')
        time.sleep(1)
        pyautogui.keyDown('e')
        scr2 = self.region.screenshot()
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

        radius = max(self.cellW + 10, self.cellH + 10)
        return self.group_pixels(middle_points, radius)
        # cv2.imwrite('highlighted_elements.png', threshold)

    def findCompassDir(self, compass):
        if compass[1] < self.cellH * 2.1:
            return 'N'
        if compass[1] > self.region.h - self.cellH * 2.1:
            return 'S'
        if compass[0] < self.cellW * 2.1:
            return 'W'
        if compass[0] > self.region.w - self.cellW * 2.1:
            return 'E'
        return '?'

    def updateCoordFromDir(self, curX, curY, dir):
        if dir == 'N':
            curY -= 1
        elif dir == 'S':
            curY += 1
        elif dir == 'W':
            curX -= 1
        elif dir == 'E':
            curX += 1
        return (curX, curY)

    def navigate(self):
        coord = self.lookatCoord()
        if coord is None:
            print('Coord: ?, ?')
        else:
            print('Coord: {}, {}'.format(coord[0], coord[1]))
        comp = self.locateCompasses()
        i = 0
        for c in comp:
            cellId = (int(c[0] / self.cellW), int(c[1] / self.cellH))
            print("{}: {}\t{}".format(i, self.findCompassDir(c), cellId))
            i += 1
        while True:
            inp = input('> ')
            if inp == 'q':
                exit()
            navTo = int(inp)
            if navTo >= 0 and navTo < i:
                break
        pyautogui.keyDown('e')
        pyautogui.click(
            self.region.x + comp[navTo][0], self.region.y + comp[navTo][1])
        pyautogui.keyUp('e')

    def waitForMapChange(self, timeout=5):
        startTime = int(time.time())
        pixel = pyautogui.pixel(
            self.region.x + self.region.w / 2,
            self.region.y + self.region.h / 3)
        while True:
            newPixel = pyautogui.pixel(
                self.region.x + self.region.w / 2,
                self.region.y + self.region.h / 3)
            if newPixel != pixel:
                time.sleep(1)
                return
            if int(time.time()) - startTime > timeout:
                print("[Game]Map change timeout")
                return
            # time.sleep(0.005)

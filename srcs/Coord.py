import pytesseract
import re
import pyautogui
import time

from ColorMask import ColorMask
import colorTerm as ct


class Coord:
    def __init__(self, region):
        self.region = region
        self.colorMask = ColorMask(region, (0, 0, 125), (50, 35, 255))
        self.coord = None

    def readCoord(self):
        self.colorMask.makeMask()
        text = pytesseract.image_to_string(
            self.colorMask.mask, config='--psm 6')
        pattern = r"(-?\d+,\s*-?\d+)"
        matches = re.findall(pattern, text)
        if len(matches) != 1:
            self.coord = None
        else:
            coord = matches[0].split(',')
            self.coord = (int(coord[0]), int(coord[1]))
        return self.coord

    def waitForChange(self, timeout=5):
        startTime = int(time.time())
        pixel = pyautogui.pixel(self.region.x + 1, self.region.y + 1)
        while int(time.time()) - startTime < timeout:
            newPixel = pyautogui.pixel(self.region.x + 1, self.region.y + 1)
            if newPixel != pixel:
                time.sleep(0.1)
                self.readCoord()
                return

        self.readCoord()
        ct.announce(f"Wait: timeout. Reading {self.coord}", ct.CYAN, "Coord")

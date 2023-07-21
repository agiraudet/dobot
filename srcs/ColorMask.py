import cv2
import numpy


class ColorMask:
    def __init__(self, region, lowHSV, highHSV, debugMask=False):
        self.lowHSV = lowHSV
        self.highHSV = highHSV
        self.region = region
        self.debugMask = debugMask
        self.mask = None

    def showMask(self):
        if self.mask is not None:
            cv2.imshow("Mask", self.mask)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

    def makeMask(self):
        sc = self.region.screenshot()
        hsv = cv2.cvtColor(numpy.array(sc), cv2.COLOR_RGB2HSV)
        self.mask = cv2.inRange(hsv, self.lowHSV, self.highHSV)
        if self.debugMask:
            self.showMask()

    def findMainColorPos(self, forceMakeMask=True):
        if forceMakeMask or self.mask is None:
            self.makeMask()
        contours, _ = cv2.findContours(
            self.mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cMax = -1
        c = None
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > cMax:
                cMax = area
                c = contour
        if c is None:
            return None
        M = cv2.moments(c)
        if M["m00"] != 0:
            centerX = int(M["m10"] / M["m00"])
            centerY = int(M["m01"] / M["m00"])
            centerX += self.game.region.x
            centerY += self.game.region.y
            return (centerX, centerY)
        return None

    def findClosestToPoint(self, pos, minArea=1, forceMakeMask=True):
        if forceMakeMask or self.mask is None:
            self.makeMask()
        posX, posY = pos
        contours, _ = cv2.findContours(
            self.mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        closestContour = None
        closestDist = float('inf')
        for contour in contours:
            area = cv2.contourArea(contour)
            if area < minArea:
                continue
            M = cv2.moments(contour)
            contourCenterX = int(M["m10"] / M["m00"])
            contourCenterY = int(M["m01"] / M["m00"])
            distance = numpy.sqrt((posX - contourCenterX)
                                  ** 2 + (posY - contourCenterY)**2)
            if distance < closestDist:
                closestContour = contour
                closestDist = distance
        if closestContour is not None:
            M = cv2.moments(closestContour)
            closestCenterX = int(M["m10"] / M["m00"])
            closestCenterY = int(M["m01"] / M["m00"])
            return closestCenterX, closestCenterY
        else:
            return None

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
            centerX += self.region.x
            centerY += self.region.y
            return (centerX, centerY)
        return None

    def findClosestToPoint(self, pos, ref=None, minArea=1, forceMakeMask=True):
        pointList = self.findGroupsPos(
            minArea=minArea, forceMakeMask=forceMakeMask)
        posX, posY = pos
        distances_and_points = [(numpy.sqrt(
            (posX - point[0])**2 + (posY - point[1])**2), point) for point in pointList]
        if ref is not None:
            refX, refY = ref
            distances_and_points = [(distance, point) for distance, point in distances_and_points if
                                    numpy.sqrt((posX - point[0])**2 + (posY - point[1])**2) < np.sqrt((refX - point[0])**2 + (refY - point[1])**2)]
        sorted_distances_and_points = sorted(
            distances_and_points, key=lambda x: x[0])
        sorted_points = [point for _, point in sorted_distances_and_points]
        return sorted_points

    def findGroupsPos(self, minArea=1, forceMakeMask=True):
        if forceMakeMask or self.mask is None:
            self.makeMask()
        contours, _ = cv2.findContours(
            self.mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        pointList = []
        for contour in contours:
            area = cv2.contourArea(contour)
            if area < minArea:
                continue
            M = cv2.moments(contour)
            contourCenterX = int(M["m10"] / M["m00"])
            contourCenterY = int(M["m01"] / M["m00"])
            pointList.append((contourCenterX + self.region.x,
                             contourCenterY + self.region.y))
        return pointList

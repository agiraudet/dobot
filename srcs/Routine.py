import pynput
import json
import pyautogui
import random
import time
import datetime

import colorTerm as ct


class Routine:
    def __init__(self, reference, delayMouse=None):
        self.steps = []
        self.delayMouse = delayMouse
        self.name = ''
        self.reference = reference
        self.iterator = 0

    def setName(self, name):
        if len(name) < 1:
            self.name = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        else:
            self.name = name

    def addStep(self, pos):
        self.steps.append(pos)

    def convertRefToPos(self, x, y):
        posX = x * self.reference.w + self.reference.x
        posY = y * self.reference.h + self.reference.y
        return (posX, posY)

    def nextStep(self, replay=False):
        if replay and self.iterator >= len(self.steps):
            self.iterator = 0
        x, y = self.steps[self.iterator]
        x, y = self.convertRefToPos(x, y)
        ct.announce(f"Click: ({x},{y})", ct.MAGENTA, "Routine")
        if self.delayMouse is not None:
            pyautogui.moveTo(x,
                             y,
                             random.uniform(
                                 self.delayMouse[0], self.delayMouse[1]),
                             pyautogui.easeOutQuad)
        pyautogui.click(x, y)
        self.iterator += 1

    def doAllSteps(self, delay=None):
        while self.iterator < len(self.steps):
            self.nextStep()
            if delay and self.iterator < len(self.steps):
                time.sleep(delay)

    def setToBeginining(self):
        self.iterator = 0


class RoutineMaster:
    def __init__(self, reference):
        self.routinesMap = {}
        self.reference = reference
        self.wipRoutine = None
        self.saveFile = 'routines.json'
        self.loadRoutinesFromFile()

    def convertPosToRef(self, x, y):
        refX = x - self.reference.x
        refX /= self.reference.w
        refY = y - self.reference.y
        refY /= self.reference.h
        return (refX, refY)

    def onLeftClick(self, x, y, button, pressed):
        if button == pynput.mouse.Button.left and pressed \
                and self.wipRoutine is not None:
            self.wipRoutine.addStep(self.convertPosToRef(x, y))
            ct.announce(f"Clicked ({x},{y})", ct.MAGENTA, "Routine")
        elif button == pynput.mouse.Button.right and pressed:
            return False

    def chooseName(self):
        ct.announce("Pick a name for the new routine:", ct.MAGENTA, "Routine")
        while True:
            name = input("> ")
            if name in self.routinesMap:
                x = ct.displayMenu(
                    f"{name} already exist. Do you want to replace it ?",
                    ["y", "n"],
                    ct.MAGENTA)
                if x == 1:
                    continue
            self.wipRoutine.setName(name)
            self.routinesMap[name] = self.wipRoutine
            self.wipRoutine = None
            self.saveRoutinesToFile()
            return

    def newRoutine(self):
        self.wipRoutine = Routine(self.reference)
        with pynput.mouse.Listener(on_click=self.onLeftClick) as listener:
            ct.announce(
                "Started Recording. Right-click to end.",
                ct.MAGENTA,
                "Routine")
            listener.join()
            ct.announce("Stopped recording", ct.MAGENTA, "Routine")
        self.chooseName()

    def getRoutineList(self):
        return [*self.routinesMap]

    def getRoutineFromName(self, name):
        return self.routinesMap[name]

    def selectRoutine(self, tabs=0):
        routineList = [*self.routinesMap]
        if len(routineList) <= 0:
            ct.announce("No routine saved!", ct.MAGENTA, "Routine")
            return None
        x = ct.displayMenu("Pick a routine:",
                           routineList,
                           ct.MAGENTA,
                           tabs=tabs)
        return self.routinesMap[routineList[x]]

    def createRoutineFromSteps(self, steps, name):
        newRoutine = Routine(self.reference)
        newRoutine.name = name
        newRoutine.steps = steps
        return newRoutine

    def saveRoutinesToFile(self):
        data = {}
        for name, rt in self.routinesMap.items():
            data[name] = rt.steps
        with open(self.saveFile, 'w') as file:
            json.dump(data, file)

    def loadRoutinesFromFile(self):
        with open(self.saveFile, 'r') as file:
            data = json.load(file)
        for name, steps in data.items():
            rt = self.createRoutineFromSteps(steps, name)
            self.routinesMap[name] = rt

    def deleteRoutineByName(self, name):
        del self.routinesMap[name]
        self.saveRoutinesToFile()
        ct.announce(f"deleted {name}", ct.MAGENTA, "Routine")

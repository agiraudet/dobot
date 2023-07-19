import time
import pyautogui

from Game import Game

game = Game()

y = game.region.y
for cy in range(34):
    x = game.region.x
    maxCX = 15
    if cy % 2 > 0:
        x += game.cellW
        maxCX -= 1
    for cx in range(maxCX):
        pyautogui.moveTo(x, y)
        print(cx, cy)
        time.sleep(0.5)
        x += game.cellW * 2
    y += game.cellH

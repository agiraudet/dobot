#!/usr/bin/python3

from Game import Game
from AutoPilot import AutoPilot
from Farmer import Farmer
from Fighter import Fighter

try:
    game = Game()
    pilot = AutoPilot(game)
    fighter = Fighter(game, '1', 2)
    farmer = Farmer(game,
                    fighter,
                    'beacons/job/res/houblon.png',
                    'beacons/job/act/faucher.png',
                    2.)
except Exception as e:
    print(e)
    # exit(1)

print("#### Dobototototot ###")
print("| 1: farm")
print("| 2: goto")
print("| 3: fight")
x = input('| > ')
print("######################")
x = int(x)
if x == 1:
    farmer.farm()
elif x == 2:
    pilot.menu()
elif x == 3:
    fighter.fight()

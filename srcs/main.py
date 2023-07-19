#!/usr/bin/python3

from Game import Game
from AutoPilot import AutoPilot
from Farmer import Farmer
from Fighter import Fighter

try:
    game = Game()
    pilot = AutoPilot(game)
    farmer = Farmer(game,
                    'beacons/job/res/houblon.png',
                    'beacons/job/act/faucher.png',
                    2.)
    fighter = Fighter(game, '1')
except Exception as e:
    print(e)
    exit(1)

farmer.farm()
# pilot.menu()
# fighter.fight()

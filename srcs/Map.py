class Cell:
    def __init(self, cX, cY):
        self.cX = cX
        self.cY = cY


class Sun(Cell):
    def __init__(self, cX, cY, toX, toY):
        super().__init__(cX, cY)
        self.toX = toX
        self.toY = toY


class Res(Cell):
    def __init__(self, cX, cY, type):
        super().__init__(cX, cY)
        self.type = type


class Map:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        cells = []

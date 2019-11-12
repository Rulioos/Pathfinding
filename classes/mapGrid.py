from mapGen.map import *


class MapGrid:
    """
    Define the grid on which the player will move.
    By default the grid is composed of squares 16x16 on a map 2048x2048.
    """

    def __init__(self, map_size=2048, square_size=16):
        self.map = Map(map_size)
        self.square = square_size
        self.square_dict = {}
        self.view_range = 48
        x, y = 0, 0
        mean = 0
        while x < map_size:
            y = 0
            while y < map_size:
                for i in range(x, 15):
                    for j in range(y, 15):
                        mean += self.map.heightMap[i][j]
                mean /= 16
                self.square_dict[(x, y)] = {"height": mean,
                                            "land": self.map.landThreshold <= mean < self.map.mountain_treshold,
                                            "prairies": self.map.landThreshold <= mean < self.map.forest_treshold,
                                            "forest": self.map.forest_treshold <= mean < self.map.mountain_treshold,
                                            "sea": mean < self.map.landThreshold,
                                            "mountain": mean >= self.map.mountain_treshold}
                y += 16
            x += 16

        self.start = self.get_start()

    def get_start(self):
        x, y = start = 0, 0
        return start


b = MapGrid(map_size=1024)

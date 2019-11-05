from noise import snoise2
from mapGen.color import *
from math import sqrt, pow
import random
import tqdm
from PIL import Image


def distance(a, b):
    """
    Calculate euclidian distance between two 2D points
    :param a: 2D Tuple corresponding to a point in 2D dimension
    :param b: 2D Tuple corresponding to a point in 2D dimension
    :return: Euclidian distance between two points
    """
    ax, ay = a
    bx, by = b
    x, y = ax - bx, ay - by
    return sqrt(x ** 2 + y ** 2)


def distance_normalized(a, b, size=256):
    """
    Gives the normalized distance between two points
    :param a: 2D Tuple corresponding to a point in 2D dimension
    :param b: 2D Tuple corresponding to a point in 2D dimension
    :param size: int
    :return: Normalized distance
    """
    dist = distance(a, b)
    dist /= size
    return dist


# Defining land and water color
# paperColor = Color(212, 161, 104)
grassColor = Color(50, 205, 50)
mountainColor = Color(44, 45, 60)
# paperColor = grassColor
waterColor = Color(0, 20, 28)
waterLakeColor = Color(171, 217, 227)


class Map:
    """
    Map object possesses a height mapGen and a color mapGen.
    It's composed of only water and land.
    All the hyper parameters can be modified when the object is initialized.
    The generate method create the height and color mapGen which are grids.
    """

    def __init__(self, size=2048, color_perlin_scale=0.025, perlin_scale=0.0025, random_color_range=10,
                 land_treshold=0.1, water_noise_perlin_scale=0.01):
        # define hyper parameters for mapGen generation
        self.perlin_offset = random.random() * 2048
        self.perlin_scale = perlin_scale
        self.colorPerlinScale = color_perlin_scale
        self.randomColorRange = random_color_range
        self.landThreshold = land_treshold
        self.mountain_treshold = 0.2
        self.lake_treshold = 0.12
        self.water_noise_perlin_scale = water_noise_perlin_scale
        # define the mapGen size and mapGen center
        self.mapSize = size
        self.mapCenter = (self.mapSize / 2, self.mapSize / 2)
        self.mapLeft_bot = (self.mapSize / 4, self.mapSize / 4)
        self.mapLeft_top = (self.mapSize / 4, 3 * self.mapSize / 4)
        self.mapRight_top = (3 * self.mapSize / 4, 3 * self.mapSize / 4)
        self.mapRight_bot = (3 * self.mapSize / 4, self.mapSize / 4)

        # define the height mapGen and the color mapGen
        self.heightMap = [[0] * self.mapSize for x in range(self.mapSize)]
        self.colorMap = [[Color() for j in range(self.mapSize)] for i in range(self.mapSize)]

        # generate the map
        self.generate()

    def generate(self):
        print("Generating the map...")
        for x in tqdm.tqdm(range(self.mapSize)):
            for y in range(self.mapSize):
                # generate base perlin noise value
                base_noise = snoise2(x * self.perlin_scale, y * self.perlin_scale,
                                     octaves=8,
                                     lacunarity=2.0,
                                     persistence=0.5,
                                     base=self.perlin_offset,
                                     repeatx=self.mapSize,
                                     repeaty=self.mapSize) + 1
                base_noise /= 2

                # pixel height

                dist_pos_center = distance_normalized((x, y), self.mapCenter, self.mapSize)
                dist_pos_lb = distance_normalized((x, y), self.mapLeft_bot, self.mapSize)
                dist_pos_lt = distance_normalized((x, y), self.mapLeft_top, self.mapSize)
                dist_pos_rb = distance_normalized((x, y), self.mapRight_bot, self.mapSize)
                dist_pos_rt = distance_normalized((x, y), self.mapRight_top, self.mapSize)
                dist_pos = min(dist_pos_center, dist_pos_lb, dist_pos_lt, dist_pos_rb, dist_pos_rt)

                base_noise -= pow(dist_pos, 0.5)
                # if base_noise <= 0:
                #     base_noise = 0

                self.heightMap[x][y] = base_noise * (base_noise > 0) + 0

                # land case
                if base_noise > self.landThreshold:
                    detail_perlin_value = snoise2(x * self.perlin_scale, y * self.perlin_scale,
                                                  octaves=12,
                                                  lacunarity=2.0,
                                                  persistence=0.8,
                                                  base=self.perlin_offset,
                                                  repeatx=self.mapSize,
                                                  repeaty=self.mapSize) + 1
                    detail_perlin_value /= 2
                    normalized_height = pow(detail_perlin_value - self.landThreshold, 3)

                    noise_value = snoise2(x * self.colorPerlinScale, y * self.colorPerlinScale,
                                          octaves=2,
                                          lacunarity=2.0,
                                          persistence=0.5,
                                          base=self.perlin_offset,
                                          repeatx=self.mapSize,
                                          repeaty=self.mapSize) + 1
                    noise_value /= 2
                    rd_color_offset = (random.random() - 0.5) * 8 + 24.0 * noise_value + normalized_height * 96.0

                    r = grassColor.r * (0.5 + base_noise) + rd_color_offset
                    g = grassColor.g * (0.5 + base_noise) + rd_color_offset
                    b = grassColor.b * (0.5 + base_noise) + rd_color_offset

                    if base_noise / (1 + dist_pos / 50) - self.landThreshold < self.landThreshold * 7 / 100:
                        r = 194 - rd_color_offset
                        g = 178 - rd_color_offset
                        b = 128 - rd_color_offset

                    self.colorMap[x][y].set_color(r, g, b)

                # water case
                else:
                    normalized_height = self.heightMap[x][y]
                    noise_value = snoise2(x * self.water_noise_perlin_scale, y * self.water_noise_perlin_scale,
                                          octaves=2,
                                          lacunarity=2.0,
                                          persistence=0.5,
                                          base=self.perlin_offset,
                                          repeatx=self.mapSize,
                                          repeaty=self.mapSize) + 1
                    noise_value /= 2
                    rd_color_offset = (random.random() - 0.5) * 4 + 12.0 * noise_value + normalized_height * 96.0
                    r = waterColor.r + rd_color_offset
                    g = waterColor.g + rd_color_offset
                    b = waterColor.b + rd_color_offset

                    if base_noise > -0.003:
                        r = 0 + rd_color_offset
                        g = 100 / abs(base_noise * 50) + rd_color_offset
                        b = 140 / abs(base_noise * 50) + rd_color_offset

                    r, g, b = r * (r >= 0), g * (g >= 0), b * (b >= 0)
                    self.colorMap[x][y].set_color(r, g, b)

        print("Done")


m = Map(size=4096)
image = Image.new("RGB", (m.mapSize, m.mapSize))
for x in range(0, m.mapSize):
    for y in range(0, m.mapSize):
        image.putpixel((x, y), m.colorMap[x][y].get_color())
print("Saving the image")
image.save("mapBase.png")
image.show()

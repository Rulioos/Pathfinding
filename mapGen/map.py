from noise import snoise2
from mapGen.color import *
from math import sqrt, pow
import random
import tqdm
from PIL import Image, ImageDraw


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
paperColor = grassColor = Color(212, 161, 104)
# grassColor = Color(50, 205, 50)
mountainColor = Color(44, 45, 60)
# paperColor = grassColor
waterColor = Color(0, 40, 56)
waterLakeColor = Color(171, 217, 227)


class Map:
    """
    Map object possesses a height mapGen and a color mapGen.
    It's composed of only water and land.
    All the hyper parameters can be modified when the object is initialized.
    The generate method create the height and color mapGen which are grids.
    """

    def __init__(self, size=2048, color_perlin_scale=0.025, perlin_scale=0.0025, random_color_range=10,
                 land_treshold=0.001, water_noise_perlin_scale=0.01):
        # define hyper parameters for mapGen generation
        self.perlin_offset = random.random() * size
        self.perlin_scale = perlin_scale
        self.colorPerlinScale = color_perlin_scale
        self.randomColorRange = random_color_range
        self.landThreshold = land_treshold
        self.mountain_treshold = 0.22
        self.forest_treshold = 0.12
        self.water_noise_perlin_scale = water_noise_perlin_scale
        # define the mapGen size and mapGen center
        self.mapSize = size
        self.mapCenter = (self.mapSize / 2, self.mapSize / 2)
        self.mapPos = []
        self.mapPos.append((self.mapSize / 2, self.mapSize / 2))
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
                                     octaves=9,
                                     lacunarity=5.0,
                                     persistence=0.25,
                                     base=self.perlin_offset,
                                     repeatx=self.mapSize,
                                     repeaty=self.mapSize) + 1
                base_noise /= 2

                # pixel height
                dist_pos = distance_normalized((x, y), self.mapPos[0], self.mapSize)
                for item in self.mapPos:
                    d = distance_normalized((x, y), item, self.mapSize)
                    if d < dist_pos:
                        dist_pos = d

                base_noise -= pow(dist_pos, 1.5)
                self.heightMap[x][y] = base_noise

                # land case
                if base_noise > self.landThreshold:
                    detail_perlin_value = snoise2(x * self.perlin_scale, y * self.perlin_scale,
                                                  octaves=12,
                                                  lacunarity=16.0,
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
                    rd_color_offset = (random.random() - 0.5) * 8 + 24.0 * noise_value + normalized_height * 256.0

                    r = grassColor.r + rd_color_offset
                    g = grassColor.g + rd_color_offset
                    b = grassColor.b + rd_color_offset

                    if base_noise / (1 + dist_pos / 10) - self.landThreshold < self.landThreshold * 10 / 100:
                        r = 194 - rd_color_offset
                        g = 178 - rd_color_offset
                        b = 128 - rd_color_offset

                    elif base_noise > self.mountain_treshold:
                        r = mountainColor.r * 5 * base_noise + rd_color_offset
                        g = mountainColor.g * 5 * base_noise + rd_color_offset
                        b = mountainColor.b * 5 * base_noise + rd_color_offset

                    elif self.forest_treshold < base_noise <= self.mountain_treshold:
                        r = 34 + rd_color_offset
                        g = 139 + rd_color_offset
                        b = 34 + rd_color_offset

                    self.colorMap[x][y].set_color(r, g, b)

                # water case
                else:
                    normalized_height = base_noise * (base_noise > 0) + 0
                    noise_value = snoise2(x * self.water_noise_perlin_scale, y * self.water_noise_perlin_scale,
                                          octaves=2,
                                          lacunarity=14.0,
                                          persistence=0.5,
                                          base=self.perlin_offset,
                                          repeatx=self.mapSize,
                                          repeaty=self.mapSize) + 1
                    noise_value /= 2
                    rd_color_offset = (random.random() - 0.5) * 4 + 12.0 * noise_value + normalized_height * 96.0
                    r = waterColor.r * (0.5 + abs(base_noise)) + rd_color_offset
                    g = waterColor.g * (0.5 + abs(base_noise)) + rd_color_offset
                    b = waterColor.b * (0.5 + abs(base_noise)) + rd_color_offset

                    if base_noise > -0.004:
                        r = 0 + rd_color_offset
                        g = 100 / abs(base_noise * 200) + rd_color_offset
                        b = 140 / abs(base_noise * 200) + rd_color_offset

                    r, g, b = r * (r >= 0), g * (g >= 0), b * (b >= 0)
                    self.colorMap[x][y].set_color(r, g, b)

        print("Done")

    def draw_map(self):
        for row in self.colorMap:
            for color in row:
                yield color.get_color()


m = Map(size=256)
image = Image.new("RGB", (m.mapSize, m.mapSize))
draw = ImageDraw.Draw(image)
for x in range(0, m.mapSize):
    for y in range(0, m.mapSize):
        image.putpixel((x, y), m.colorMap[x][y].get_color())
        if y % 16 == 0:
            pass  # draw.line(((0, y), (m.mapSize, y)))

    if x % 16 == 0:
        pass  # draw.line(((x, 0), (x, m.mapSize)))

print("Saving the image")
image.save("mapBase.png", dpi=(300, 300))
image.show()

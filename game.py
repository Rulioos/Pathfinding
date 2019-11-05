import pygame as pg
from board import *
import time

FPS = 60
score = 0
pg.init()
clock = pg.time.Clock()
screen = pg.display.set_mode((800, 600))


def resize(image, w, h):
    return pg.transform.scale(image, (w, h))


human = pg.image.load("assets/Kickpixel's - RPG Icons/human.png")
desert_tile = pg.image.load("assets/DesertTileset/png/Objects/StoneBlock.png")
occupied_tile = pg.image.load("assets/DesertTileset/png/Objects/Grass (2).png")
coin = pg.image.load("assets/Kickpixel's - RPG Icons/coin_bronze.png")

square_size = 50
board = Board(800, 600, square_size)

# drawing the grid
grid = board.state.grid
for key, value in grid.items():
    if value["occupied"]:
        screen.blit(resize(occupied_tile, square_size, square_size), key)
    else:
        screen.blit(resize(desert_tile, square_size, square_size), key)

screen.blit(resize(human, square_size, square_size), board.state.get_coin_looker_pos())

# pick a font you have and set its size
myfont = pg.font.SysFont("Comic Sans MS", 30)
# apply it to text on a label
counter = 0

# put the label object on the screen at point x=100, y=100

screen.blit(resize(coin, square_size, square_size), board.goal)
pg.display.update()

start_time = time.perf_counter()
Node, n = a_star_search(board)
# Node, n = bfs_tree_search(board)
end_time = time.perf_counter()
counter += end_time - start_time

path = Node.path()
actions = [item.state.get_coin_looker_pos() for item in path]
label = myfont.render("Time: " + str(counter), 1, (255, 255, 255))
score_label = myfont.render("Score: " + str(score), 1, (255, 255, 255))

score = 1
while score < 1000:
    clock.tick(FPS)

    for key, value in grid.items():
        if value["occupied"]:
            screen.blit(resize(occupied_tile, square_size, square_size), key)
        else:
            screen.blit(resize(desert_tile, square_size, square_size), key)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            quit()
    if len(actions) == 0:
        screen.blit(resize(desert_tile, square_size, square_size), board.goal)
        screen.blit(resize(human, square_size, square_size), board.goal)
        board.new_goal()
        screen.blit(resize(coin, square_size, square_size), board.goal)
        screen.blit(label, (0, 0))
        screen.blit(score_label, (600, 0))
        pg.display.update()
        start_time = time.perf_counter()
        Node, n = a_star_search(board)
        # Node, n = bfs_tree_search(board)
        end_time = time.perf_counter()
        score += 1
        counter += end_time - start_time
        path = Node.path()
        actions = [item.state.get_coin_looker_pos() for item in path]
        label = myfont.render("Time: " + str(counter), 1, (255, 255, 255))
        score_label = myfont.render("Score: " + str(score), 1, (255, 255, 255))
    else:
        act = actions.pop()
        key = board.state.move_coin_looker(act)
        screen.blit(resize(desert_tile, square_size, square_size), key)

    screen.blit(label, (0, 0))
    screen.blit(score_label, (600, 0))
    screen.blit(resize(human, square_size, square_size), board.state.get_coin_looker_pos())
    screen.blit(resize(coin, square_size, square_size), board.goal)
    time.sleep(0.025)

    pg.display.update()

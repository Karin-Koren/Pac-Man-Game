# This is a sample Python script.
import copy
from board import boards
import pygame
import math

pygame.init()

WIDTH = 700
HEIGHT = 750
screen = pygame.display.set_mode([WIDTH, HEIGHT])
timer = pygame.time.Clock()
fps = 60
font = pygame.font.Font('freesansbold.ttf', 20)
level = copy.deepcopy(boards)
color = 'blue'
PI = math.pi
player_images = []
img_size = 35


for i in range(1, 5):
    player_images.append(
        pygame.transform.scale(pygame.image.load(f'assets/player_images/{i}.png'), (img_size, img_size)))

blinky_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/red.png'), (img_size, img_size))
pinky_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/pink.png'), (img_size, img_size))
inky_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/blue.png'), (img_size, img_size))
clyde_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/orange.png'), (img_size, img_size))
spooked_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/powerup.png'), (img_size, img_size))
dead_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/dead.png'), (img_size, img_size))

height_piece = ((HEIGHT - 50) // 32)
width_piece = (WIDTH // 30)

player_x = 330
player_y = 495
direction = 0

blinky_x = 42
blinky_y = 38
blinky_direction = 0

inky_x = 340
inky_y = 288
inky_direction = 2

pinky_x = 330
pinky_y = 328
pinky_direction = 2

clyde_x = 320
clyde_y = 328
clyde_direction = 2

counter = 0
flicker = False
# R, L, U, D
turns_allowed = [False, False, False, False]
direction_command = 0
player_speed = 2
score = 0
power = False
power_count = 0
eaten_ghosts = [False, False, False, False]
ghosts_targets = [(player_x, player_y), (player_x, player_y), (player_x, player_y), (player_x, player_y)]

blinky_dead = False
pinky_dead = False
inky_dead = False
clyde_dead = False
blinky_box = False
pinky_box = False
inky_box = False
clyde_box = False

ghost_speeds = [2, 2, 2, 2]

moving = False
startup_counter = 0
lives = 1
game_over = False
game_won = False


class Ghost:
    def __init__(self, x_coord, y_coord, target, speed, img, direct, deed, box, id):
        self.x_pos = x_coord
        self.y_pos = y_coord
        self.center_x = self.x_pos + img_size // 2
        self.center_y = self.y_pos + img_size // 2 + 1
        self.target = target
        self.speed = speed
        self.img = img
        self.direct = direct
        self.deed = deed
        self.in_box = box
        self.id = id
        self.turns, self.in_box = self.check_collisions()
        self.rect = self.draw()

    def draw(self):
        if (not power and not self.deed) or (eaten_ghosts[self.id] and power and not self.deed):
            screen.blit(self.img, (self.x_pos, self.y_pos))
        elif power and not self.deed and not eaten_ghosts[self.id]:
            screen.blit(spooked_img, (self.x_pos, self.y_pos))
        else:
            screen.blit(dead_img, (self.x_pos, self.y_pos))
        ghost_rect = pygame.rect.Rect((self.center_x - 18, self.center_y - 18), (36, 36))
        return ghost_rect

    def check_collisions(self):
        self.turns = [False, False, False, False]
        num = 15

        if 0 < self.center_x // 30 < 29:
            if level[(self.center_y - num) // height_piece][self.center_x // width_piece] == 9:
                self.turns[2] = True
            if level[self.center_y // height_piece][(self.center_x - num) // width_piece] < 3 \
                    or (level[self.center_y // height_piece][(self.center_x - num) // width_piece] == 9 and (
                    self.in_box or self.deed)):
                self.turns[1] = True
            if level[self.center_y // height_piece][(self.center_x + num) // width_piece] < 3 \
                    or (level[self.center_y // height_piece][(self.center_x + num) // width_piece] == 9 and (
                    self.in_box or self.deed)):
                self.turns[0] = True
            if level[(self.center_y + num) // height_piece][self.center_x // width_piece] < 3 \
                    or (level[(self.center_y + num) // height_piece][self.center_x // width_piece] == 9 and (
                    self.in_box or self.deed)):
                self.turns[3] = True
            if level[(self.center_y - num) // height_piece][self.center_x // width_piece] < 3 \
                    or (level[(self.center_y - num) // height_piece][self.center_x // width_piece] == 9 and (
                    self.in_box or self.deed)):
                self.turns[2] = True

            if self.direct == 2 or self.direct == 3:
                if 6 <= self.center_x % width_piece <= 14:
                    if level[(self.center_y + num) // height_piece][self.center_x // width_piece] < 3 \
                            or (level[(self.center_y + num) // height_piece][self.center_x // width_piece] == 9 and (
                            self.in_box or self.deed)):
                        self.turns[3] = True
                    if level[(self.center_y - num) // height_piece][self.center_x // width_piece] < 3 \
                            or (level[(self.center_y - num) // height_piece][self.center_x // width_piece] == 9 and (
                            self.in_box or self.deed)):
                        self.turns[2] = True
                if 6 <= self.center_y % height_piece <= 14:
                    if level[self.center_y // height_piece][(self.center_x - width_piece) // width_piece] < 3 \
                            or (level[self.center_y // height_piece][
                                    (self.center_x - width_piece) // width_piece] == 9 and (
                                        self.in_box or self.deed)):
                        self.turns[1] = True
                    if level[self.center_y // height_piece][(self.center_x + width_piece) // width_piece] < 3 \
                            or (level[self.center_y // height_piece][
                                    (self.center_x + width_piece) // width_piece] == 9 and (
                                        self.in_box or self.deed)):
                        self.turns[0] = True

            if self.direct == 0 or self.direct == 1:
                if 6 <= self.center_x % width_piece <= 14:
                    if level[(self.center_y + height_piece) // height_piece][self.center_x // width_piece] < 3 \
                            or (level[(self.center_y + height_piece) // height_piece][
                                    self.center_x // width_piece] == 9 and (
                                        self.in_box or self.deed)):
                        self.turns[3] = True
                    if level[(self.center_y - height_piece) // height_piece][self.center_x // width_piece] < 3 \
                            or (level[(self.center_y - height_piece) // height_piece][
                                    self.center_x // width_piece] == 9 and (
                                        self.in_box or self.deed)):
                        self.turns[2] = True
                if 6 <= self.center_y % height_piece <= 14:
                    if level[self.center_y // height_piece][(self.center_x - num) // width_piece] < 3 \
                            or (level[self.center_y // height_piece][(self.center_x - num) // width_piece] == 9 and (
                            self.in_box or self.deed)):
                        self.turns[1] = True
                    if level[self.center_y // height_piece][(self.center_x + num) // width_piece] < 3 \
                            or (level[self.center_y // height_piece][(self.center_x + num) // width_piece] == 9 and (
                            self.in_box or self.deed)):
                        self.turns[0] = True
        else:
            self.turns[0] = True
            self.turns[1] = True

        if 270 < self.x_pos < 385 and 258 < self.y_pos < 348:
            self.in_box = True
        else:
            self.in_box = False

        return self.turns, self.in_box

    def move_clyde(self):
        # r, l, u, d
        # clyde is going to turn whenever advantageous for pursuit
        if self.direct == 0:
            if self.target[0] > self.x_pos and self.turns[0]:
                self.x_pos += self.speed
            elif not self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direct = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direct = 2
                    self.y_pos -= self.speed
                elif self.target[0] < self.y_pos and self.turns[1]:
                    self.direct = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direct = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direct = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direct = 1
                    self.x_pos -= self.speed
            elif self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direct = 3
                    self.y_pos += self.speed
                if self.target[1] < self.y_pos and self.turns[2]:
                    self.direct = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos += self.speed
        elif self.direct == 1:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.direct = 3
                self.y_pos += self.speed
            elif self.target[0] < self.x_pos and self.turns[1]:
                self.x_pos -= self.speed
            elif not self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direct = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direct = 2
                    self.y_pos -= self.speed
                elif self.target[0] > self.x_pos and self.turns[0]:
                    self.direct = 0
                    self.x_pos += self.speed
                elif self.turns[3]:
                    self.direct = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direct = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direct = 0
                    self.x_pos += self.speed
            elif self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direct = 3
                    self.y_pos += self.speed
                if self.target[1] < self.y_pos and self.turns[2]:
                    self.direct = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos -= self.speed
        elif self.direct == 2:
            if self.target[0] < self.x_pos and self.turns[1]:
                self.direct = 1
                self.x_pos -= self.speed
            elif self.target[1] < self.y_pos and self.turns[2]:
                self.y_pos -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direct = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.y_pos and self.turns[1]:
                    self.direct = 1
                    self.x_pos -= self.speed
                elif self.target[1] > self.y_pos and self.turns[3]:
                    self.direct = 3
                    self.y_pos += self.speed
                elif self.turns[1]:
                    self.direct = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direct = 3
                    self.y_pos += self.speed
                elif self.turns[0]:
                    self.direct = 0
                    self.x_pos += self.speed
            elif self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direct = 0
                    self.x_pos += self.speed
                if self.target[0] < self.x_pos and self.turns[1]:
                    self.direct = 1
                    self.x_pos -= self.speed
                else:
                    self.y_pos -= self.speed
        elif self.direct == 3:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.y_pos += self.speed
            elif not self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direct = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direct = 1
                    self.x_pos -= self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direct = 2
                    self.y_pos -= self.speed
                elif self.turns[2]:
                    self.direct = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direct = 1
                    self.x_pos -= self.speed
                elif self.turns[0]:
                    self.direct = 0
                    self.x_pos += self.speed
            elif self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direct = 0
                    self.x_pos += self.speed
                if self.target[0] < self.x_pos and self.turns[1]:
                    self.direct = 1
                    self.x_pos -= self.speed
                else:
                    self.y_pos += self.speed

        if self.x_pos > 655:
            self.x_pos = 0
        elif self.x_pos < -40:
            self.x_pos = 650

        return self.x_pos, self.y_pos, self.direct

    def move_blinky(self):
        # r, l, u, d
        # blinky is going to turn whenever colliding with walls, otherwise continue straight
        if self.direct == 0:
            if self.target[0] > self.x_pos and self.turns[0]:
                self.x_pos += self.speed
            elif not self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direct = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direct = 2
                    self.y_pos -= self.speed
                elif self.target[0] < self.y_pos and self.turns[1]:
                    self.direct = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direct = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direct = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direct = 1
                    self.x_pos -= self.speed
            elif self.turns[0]:
                self.x_pos += self.speed
        elif self.direct == 1:
            if self.target[0] < self.x_pos and self.turns[1]:
                self.x_pos -= self.speed
            elif not self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direct = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direct = 2
                    self.y_pos -= self.speed
                elif self.target[0] > self.x_pos and self.turns[0]:
                    self.direct = 0
                    self.x_pos += self.speed
                elif self.turns[3]:
                    self.direct = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direct = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direct = 0
                    self.x_pos += self.speed
            elif self.turns[1]:
                self.x_pos -= self.speed
        elif self.direct == 2:
            if self.target[1] < self.y_pos and self.turns[2]:
                self.y_pos -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direct = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.y_pos and self.turns[1]:
                    self.direct = 1
                    self.x_pos -= self.speed
                elif self.target[1] > self.y_pos and self.turns[3]:
                    self.direct = 3
                    self.y_pos += self.speed
                elif self.turns[3]:
                    self.direct = 3
                    self.y_pos += self.speed
                elif self.turns[0]:
                    self.direct = 0
                    self.x_pos += self.speed
                elif self.turns[1]:
                    self.direct = 1
                    self.x_pos -= self.speed
            elif self.turns[2]:
                self.y_pos -= self.speed
        elif self.direct == 3:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.y_pos += self.speed
            elif not self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direct = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direct = 1
                    self.x_pos -= self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direct = 2
                    self.y_pos -= self.speed
                elif self.turns[2]:
                    self.direct = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direct = 0
                    self.x_pos += self.speed
                elif self.turns[1]:
                    self.direct = 1
                    self.x_pos -= self.speed
            elif self.turns[3]:
                self.y_pos += self.speed

        if self.x_pos > 655:
            self.x_pos = 0
        elif self.x_pos < -40:
            self.x_pos = 650

        return self.x_pos, self.y_pos, self.direct

    def move_inky(self):
        # r, l, u, d
        # inky turn up or down at any point to pursuit, but left and right only on collision
        if self.direct == 0:
            if self.target[0] > self.x_pos and self.turns[0]:
                self.x_pos += self.speed
            elif not self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direct = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direct = 2
                    self.y_pos -= self.speed
                elif self.target[0] < self.y_pos and self.turns[1]:
                    self.direct = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direct = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direct = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direct = 1
                    self.x_pos -= self.speed
            elif self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direct = 3
                    self.y_pos += self.speed
                if self.target[1] < self.y_pos and self.turns[2]:
                    self.direct = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos += self.speed
        elif self.direct == 1:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.direct = 3
                self.y_pos += self.speed
            elif self.target[0] < self.x_pos and self.turns[1]:
                self.x_pos -= self.speed
            elif not self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direct = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direct = 2
                    self.y_pos -= self.speed
                elif self.target[0] > self.x_pos and self.turns[0]:
                    self.direct = 0
                    self.x_pos += self.speed
                elif self.turns[3]:
                    self.direct = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direct = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direct = 0
                    self.x_pos += self.speed
            elif self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direct = 3
                    self.y_pos += self.speed
                if self.target[1] < self.y_pos and self.turns[2]:
                    self.direct = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos -= self.speed
        elif self.direct == 2:
            if self.target[1] < self.y_pos and self.turns[2]:
                self.y_pos -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direct = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.y_pos and self.turns[1]:
                    self.direct = 1
                    self.x_pos -= self.speed
                elif self.target[1] > self.y_pos and self.turns[3]:
                    self.direct = 3
                    self.y_pos += self.speed
                elif self.turns[1]:
                    self.direct = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direct = 3
                    self.y_pos += self.speed
                elif self.turns[0]:
                    self.direct = 0
                    self.x_pos += self.speed
            elif self.turns[2]:
                self.y_pos -= self.speed
        elif self.direct == 3:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.y_pos += self.speed
            elif not self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direct = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direct = 1
                    self.x_pos -= self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direct = 2
                    self.y_pos -= self.speed
                elif self.turns[2]:
                    self.direct = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direct = 1
                    self.x_pos -= self.speed
                elif self.turns[0]:
                    self.direct = 0
                    self.x_pos += self.speed
            elif self.turns[3]:
                self.y_pos += self.speed

        if self.x_pos > 655:
            self.x_pos = 0
        elif self.x_pos < -40:
            self.x_pos = 650

        return self.x_pos, self.y_pos, self.direct

    def move_pinky(self):
        # r, l, u, d
        # pinky turn left or right at any point to pursuit, but up or down only on collision
        if self.direct == 0:
            if self.target[0] > self.x_pos and self.turns[0]:
                self.x_pos += self.speed
            elif not self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direct = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direct = 2
                    self.y_pos -= self.speed
                elif self.target[0] < self.y_pos and self.turns[1]:
                    self.direct = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direct = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direct = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direct = 1
                    self.x_pos -= self.speed
            elif self.turns[0]:
                self.x_pos += self.speed
        elif self.direct == 1:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.direct = 3
                self.y_pos += self.speed
            elif self.target[0] < self.x_pos and self.turns[1]:
                self.x_pos -= self.speed
            elif not self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direct = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direct = 2
                    self.y_pos -= self.speed
                elif self.target[0] > self.x_pos and self.turns[0]:
                    self.direct = 0
                    self.x_pos += self.speed
                elif self.turns[3]:
                    self.direct = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direct = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direct = 0
                    self.x_pos += self.speed
            elif self.turns[1]:
                self.x_pos -= self.speed
        elif self.direct == 2:
            if self.target[0] < self.x_pos and self.turns[1]:
                self.direct = 1
                self.x_pos -= self.speed
            elif self.target[1] < self.y_pos and self.turns[2]:
                self.y_pos -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direct = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.y_pos and self.turns[1]:
                    self.direct = 1
                    self.x_pos -= self.speed
                elif self.target[1] > self.y_pos and self.turns[3]:
                    self.direct = 3
                    self.y_pos += self.speed
                elif self.turns[1]:
                    self.direct = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direct = 3
                    self.y_pos += self.speed
                elif self.turns[0]:
                    self.direct = 0
                    self.x_pos += self.speed
            elif self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direct = 0
                    self.x_pos += self.speed
                if self.target[0] < self.x_pos and self.turns[1]:
                    self.direct = 1
                    self.x_pos -= self.speed
                else:
                    self.y_pos -= self.speed
        elif self.direct == 3:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.y_pos += self.speed
            elif not self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direct = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direct = 1
                    self.x_pos -= self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direct = 2
                    self.y_pos -= self.speed
                elif self.turns[2]:
                    self.direct = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direct = 1
                    self.x_pos -= self.speed
                elif self.turns[0]:
                    self.direct = 0
                    self.x_pos += self.speed
            elif self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direct = 0
                    self.x_pos += self.speed
                if self.target[0] < self.x_pos and self.turns[1]:
                    self.direct = 1
                    self.x_pos -= self.speed
                else:
                    self.y_pos += self.speed

        if self.x_pos > 655:
            self.x_pos = 0
        elif self.x_pos < -40:
            self.x_pos = 650

        return self.x_pos, self.y_pos, self.direct


def draw_board():
    # height_piece = ((HEIGHT - 50) // 32)
    # width_piece = (WIDTH // 30)

    for i in range(len(level)):
        for j in range(len(level[i])):
            if level[i][j] == 1:
                pygame.draw.circle(screen, 'white',
                                   (j * width_piece + (0.5 * width_piece), i * height_piece + (0.5 * height_piece)), 4)
            elif level[i][j] == 2 and not flicker:
                pygame.draw.circle(screen, 'white',
                                   (j * width_piece + (0.5 * width_piece), i * height_piece + (0.5 * height_piece)), 10)
            elif level[i][j] == 3:
                pygame.draw.line(screen, color, (j * width_piece + (0.5 * width_piece), i * height_piece),
                                 (j * width_piece + (0.5 * width_piece), i * height_piece + height_piece), 3)
            elif level[i][j] == 4:
                pygame.draw.line(screen, color, (j * width_piece, i * height_piece + (0.5 * height_piece)),
                                 (j * width_piece + width_piece, i * height_piece + (0.5 * height_piece)), 3)
            elif level[i][j] == 5:
                pygame.draw.arc(screen, color,
                                [(j * width_piece - (width_piece * 0.4) - 2), (i * height_piece + (0.5 * height_piece)),
                                 width_piece, height_piece], 0, PI / 2, 3)
            elif level[i][j] == 6:
                pygame.draw.arc(screen, color,
                                [(j * width_piece + (width_piece * 0.5)), (i * height_piece + (0.5 * height_piece)),
                                 width_piece, height_piece], PI / 2, PI, 3)
            elif level[i][j] == 7:
                pygame.draw.arc(screen, color,
                                [(j * width_piece + (width_piece * 0.5)), (i * height_piece - (0.4 * height_piece)),
                                 width_piece, height_piece], PI, 3 * PI / 2, 3)
            elif level[i][j] == 8:
                pygame.draw.arc(screen, color,
                                [(j * width_piece - (width_piece * 0.4)) - 2, (i * height_piece - (0.4 * height_piece)),
                                 width_piece, height_piece], 3 * PI / 2, 2 * PI, 3)
            elif level[i][j] == 9:
                pygame.draw.line(screen, 'white', (j * width_piece, i * height_piece + (0.5 * height_piece)),
                                 (j * width_piece + width_piece, i * height_piece + (0.5 * height_piece)), 3)


def draw_player():
    # 0-RIGHT, 1-LEFT, 2-UP, 3-DOWN
    if direction == 0:
        screen.blit(player_images[counter // 5], (player_x, player_y))
    if direction == 1:
        screen.blit(pygame.transform.flip(player_images[counter // 5], True, False), (player_x, player_y))
    if direction == 2:
        screen.blit(pygame.transform.rotate(player_images[counter // 5], 90), (player_x, player_y))
    if direction == 3:
        screen.blit(pygame.transform.rotate(player_images[counter // 5], 270), (player_x, player_y))


def draw_misc():
    score_text = font.render(f'Score: {score}', True, 'white')
    screen.blit(score_text, (10, HEIGHT - 30))
    if power:
        pygame.draw.circle(screen, 'blue', (140, 730), 15)
    for i in range(lives):
        screen.blit(pygame.transform.scale(player_images[0], (35, 35)), (550 + i * 40, HEIGHT - 50))
    if game_over:
        pygame.draw.rect(screen, "white", [50, 200,800,300], 0, 10)
        pygame.draw.rect(screen, "dark gray", [70, 220,760,260], 0, 10)
        gameover_text = font.render("Game Over! Space bar to restart!", True, "red")
        screen.blit(gameover_text, (100,300))
    if game_won:
        pygame.draw.rect(screen, "white", [50, 200,800,300], 0, 10)
        pygame.draw.rect(screen, "dark gray", [70, 220,760,260], 0, 10)
        gamewin_text = font.render("You Won! Space bar to restart!", True, "green")
        screen.blit(gamewin_text, (100,300))

def check_position(center_x, center_y):
    turns = [False, False, False, False]
    # y = center_y % height_piece
    # x = center_x % width_piece
    num = 15
    # print(center_x)
    # print(center_y // height_piece, (center_x + num) // width_piece)

    # check collision based on center x and center y of player +/- fudge number
    if center_x // 30 < 29:
        if direction == 0:
            if level[center_y // height_piece][(center_x - num) // width_piece] < 3:
                turns[1] = True
        if direction == 1:
            if level[center_y // height_piece][(center_x + num) // width_piece] < 3:
                turns[0] = True
        if direction == 2:
            if level[(center_y + num) // height_piece][center_x // width_piece] < 3:
                turns[3] = True
        if direction == 3:
            if level[(center_y - num) // height_piece][center_x // width_piece] < 3:
                turns[2] = True

        if direction == 2 or direction == 3:
            if 6 <= center_x % width_piece <= 14:
                if level[(center_y + num) // height_piece][center_x // width_piece] < 3:
                    turns[3] = True
                if level[(center_y - num) // height_piece][center_x // width_piece] < 3:
                    turns[2] = True
            if 6 <= center_y % height_piece <= 14:
                if level[center_y // height_piece][(center_x - width_piece) // width_piece] < 3:
                    turns[1] = True
                if level[center_y // height_piece][(center_x + width_piece) // width_piece] < 3:
                    turns[0] = True

        if direction == 0 or direction == 1:
            if 6 <= center_x % width_piece <= 14:
                if level[(center_y + height_piece) // height_piece][center_x // width_piece] < 3:
                    turns[3] = True
                if level[(center_y - height_piece) // height_piece][center_x // width_piece] < 3:
                    turns[2] = True
            if 6 <= center_y % height_piece <= 14:
                if level[center_y // height_piece][(center_x - num) // width_piece] < 3:
                    turns[1] = True
                if level[center_y // height_piece][(center_x + num) // width_piece] < 3:
                    turns[0] = True
    else:
        turns[0] = True
        turns[1] = True
    return turns


def move_player(play_x, play_y):
    # r, l, u, d
    if direction == 0 and turns_allowed[0]:
        play_x += player_speed
    elif direction == 1 and turns_allowed[1]:
        play_x -= player_speed
    elif direction == 2 and turns_allowed[2]:
        play_y -= player_speed
    elif direction == 3 and turns_allowed[3]:
        play_y += player_speed
    return play_x, play_y


def check_collisions(score, power, power_count, eaten_ghosts):
    if 0 < player_x < WIDTH:
        if level[center_y // height_piece][center_x // width_piece] == 1:
            level[center_y // height_piece][center_x // width_piece] = 0
            score += 10
        if level[center_y // height_piece][center_x // width_piece] == 2:
            level[center_y // height_piece][center_x // width_piece] = 0
            score += 50
            power = True
            power_count = 0
            eten_ghosts = [False, False, False, False]

    return score, power, power_count, eaten_ghosts


def get_targets(blink_x, blink_y, ink_x, ink_y, pink_x, pink_y, clyd_x, clyd_y):
    if player_x < 350:
        runaway_x = 700
    else:
        runaway_x = 0
    if player_y < 350:
        runaway_y = 700
    else:
        runaway_y = 0
    return_target = (340, 288)
    if power:
        if not blinky.deed and not eaten_ghosts[0]:
            blink_target = (runaway_x, runaway_y)
        elif not blinky.deed and eaten_ghosts[0]:
            if blinky.in_box:
                blink_target = (400, 100)
            else:
                blink_target = (player_x, player_y)
        else:
            blink_target = return_target
        if not inky.deed and not eaten_ghosts[1]:
            ink_target = (runaway_x, player_y)
        elif not inky.deed and eaten_ghosts[1]:
            if inky.in_box:
                ink_target = (400, 100)
            else:
                ink_target = (player_x, player_y)
        else:
            ink_target = return_target
        if not pinky.deed and not eaten_ghosts[2]:
            pink_target = (player_x, runaway_y)
        elif not pinky.deed and eaten_ghosts[2]:
            if pinky.in_box:
                pink_target = (400, 100)
            else:
                pink_target = (player_x, player_y)
        else:
            pink_target = return_target
        if not clyde.deed and not eaten_ghosts[3]:
            clyde_target = (350, 350)
        elif not clyde.deed and eaten_ghosts[3]:
            if clyde.in_box:
                clyde_target = (400, 100)
            else:
                clyde_target = (player_x, player_y)
        else:
            clyde_target = return_target
    else:
        if not blinky.deed:
            if blinky.in_box:
                blink_target = (400, 100)
            else:
                blink_target = (player_x, player_y)
        else:
            blink_target = return_target
        if not inky.deed:
            if inky.in_box:
                ink_target = (400, 100)
            else:
                ink_target = (player_x, player_y)
        else:
            ink_target = return_target
        if not pinky.deed:
            if pinky.in_box:
                pink_target = (400, 100)
            else:
                pink_target = (player_x, player_y)
        else:
            pink_target = return_target
        if not clyde.deed:
            if clyde.in_box:
                clyde_target = (400, 100)
            else:
                clyde_target = (player_x, player_y)
        else:
            clyde_target = return_target

    return [blink_target, ink_target, pink_target, clyde_target]


run = True
while run:
    timer.tick(fps)
    if counter < 19:
        counter += 1
        if counter > 3:
            flicker = False
    else:
        counter = 0
        flicker = True

    if power and power_count < 600:
        power_count += 1
    elif power and power_count >= 600:
        power_count = 0
        power = False
        eaten_ghosts = [False, False, False, False]

    if startup_counter < 180 and not game_won and not game_over:
        moving = False
        startup_counter += 1
    else:
        moving = True

    center_x = player_x + img_size // 2
    center_y = player_y + img_size // 2 + 1

    if power:
        ghost_speeds = [1, 1, 1, 1]
    else:
        ghost_speeds = [2, 2, 2, 2]
    if eaten_ghosts[0]:
        ghost_speeds[0] = 2
    if eaten_ghosts[1]:
        ghost_speeds[1] = 2
    if eaten_ghosts[2]:
        ghost_speeds[2] = 2
    if eaten_ghosts[3]:
        ghost_speeds[3] = 2
    if blinky_dead:
        ghost_speeds[0] = 4
    if inky_dead:
        ghost_speeds[1] = 4
    if pinky_dead:
        ghost_speeds[2] = 4
    if clyde_dead:
        ghost_speeds[3] = 4

    game_won = True
    for i in range(len(level)):
        if 1 in level[i] or 2 in level[i]:
            game_won = False

    screen.fill('black')
    draw_board()
    player_circle = pygame.draw.circle(screen, 'black', (center_x, center_y), 16, 2)
    draw_player()
    blinky = Ghost(blinky_x, blinky_y, ghosts_targets[0], ghost_speeds[0], blinky_img,
                   blinky_direction, blinky_dead, blinky_box, 0)
    inky = Ghost(inky_x, inky_y, ghosts_targets[1], ghost_speeds[1], inky_img,
                 inky_direction, inky_dead, inky_box, 1)
    pinky = Ghost(pinky_x, pinky_y, ghosts_targets[2], ghost_speeds[2], pinky_img,
                  pinky_direction, pinky_dead, pinky_box, 2)
    clyde = Ghost(clyde_x, clyde_y, ghosts_targets[3], ghost_speeds[3], clyde_img,
                  clyde_direction, clyde_dead, clyde_box, 3)
    draw_misc()
    ghosts_targets = get_targets(blinky_x, blinky_y, inky_x, inky_y, pinky_x, pinky_y, clyde_x, clyde_y)
    # pygame.draw.circle(screen, 'red', (center_x, center_y), 2)
    turns_allowed = check_position(center_x, center_y)
    if moving:
        player_x, player_y = move_player(player_x, player_y)
        if not blinky_dead and not blinky.in_box:
            blinky_x, blinky_y, blinky_direction = blinky.move_blinky()
        else:
            blinky_x, blinky_y, blinky_direction = blinky.move_clyde()
        if not inky_dead and not inky.in_box:
            inky_x, inky_y, inky_direction = inky.move_inky()
        else:
            inky_x, inky_y, inky_direction = inky.move_clyde()
        if not pinky_dead and not pinky.in_box:
            pinky_x, pinky_y, pinky_direction = pinky.move_pinky()
        else:
            pinky_x, pinky_y, pinky_direction = pinky.move_clyde()
        clyde_x, clyde_y, clyde_direction = clyde.move_clyde()
    score, power, power_count, eaten_ghosts = check_collisions(score, power, power_count, eaten_ghosts)

    if not power:
        if (player_circle.colliderect(blinky.rect) and not blinky.deed) or \
                (player_circle.colliderect(inky.rect) and not inky.deed) or \
                (player_circle.colliderect(pinky.rect) and not pinky.deed) or \
                (player_circle.colliderect(clyde.rect) and not clyde.deed):
            if lives > 0:
                lives -= 1
                startup_counter = 0
                direction_command = 0
                power = False
                power_count = 0
                player_x = 330
                player_y = 495
                direction = 0

                blinky_x = 42
                blinky_y = 38
                blinky_direction = 0

                inky_x = 340
                inky_y = 288
                inky_direction = 2

                pinky_x = 330
                pinky_y = 328
                pinky_direction = 2

                clyde_x = 320
                clyde_y = 328
                clyde_direction = 2

                eaten_ghosts = [False, False, False, False]
                blinky_dead = False
                pinky_dead = False
                inky_dead = False
                clyde_dead = False
            else:
                game_over = True
                moving = False
                startup_counter = 0
    if power:
        if (player_circle.colliderect(blinky.rect) and eaten_ghosts[0] and not blinky.deed) or \
                  (player_circle.colliderect(inky.rect) and eaten_ghosts[1] and not inky.deed) or \
                  (player_circle.colliderect(pinky.rect) and eaten_ghosts[2] and not pinky.deed) or \
                  (player_circle.colliderect(clyde.rect) and eaten_ghosts[3] and not clyde.deed):
            if lives > 0:
                lives -= 1
                startup_counter = 0
                direction_command = 0
                power = False
                power_count = 0
                player_x = 330
                player_y = 495
                direction = 0

                blinky_x = 42
                blinky_y = 38
                blinky_direction = 0

                inky_x = 340
                inky_y = 288
                inky_direction = 2

                pinky_x = 330
                pinky_y = 328
                pinky_direction = 2

                clyde_x = 320
                clyde_y = 328
                clyde_direction = 2

                eaten_ghosts = [False, False, False, False]
                blinky_dead = False
                pinky_dead = False
                inky_dead = False
                clyde_dead = False

            else:
                game_over = True
                moving = False
                startup_counter = 0

    if power and player_circle.colliderect(blinky.rect) and not blinky.deed and not eaten_ghosts[0]:
        blinky_dead = True
        eaten_ghosts[0] = True
        score += 200
    if power and player_circle.colliderect(inky.rect) and not inky.deed and not eaten_ghosts[1]:
        inky_dead = True
        eaten_ghosts[1] = True
        score += 200
    if power and player_circle.colliderect(pinky.rect) and not pinky.deed and not eaten_ghosts[2]:
        pinky_dead = True
        eaten_ghosts[2] = True
        score += 200
    if power and player_circle.colliderect(clyde.rect) and not clyde.deed and not eaten_ghosts[3]:
        clyde_dead = True
        eaten_ghosts[3] = True
        score += 200

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                direction_command = 0
            if event.key == pygame.K_LEFT:
                direction_command = 1
            if event.key == pygame.K_UP:
                direction_command = 2
            if event.key == pygame.K_DOWN:
                direction_command = 3
            if event.key == pygame.K_SPACE and (game_won or game_over):
                lives -= 1
                startup_counter = 0
                direction_command = 0
                power = False
                power_count = 0
                player_x = 330
                player_y = 495
                direction = 0

                blinky_x = 42
                blinky_y = 38
                blinky_direction = 0

                inky_x = 340
                inky_y = 288
                inky_direction = 2

                pinky_x = 330
                pinky_y = 328
                pinky_direction = 2

                clyde_x = 320
                clyde_y = 328
                clyde_direction = 2

                eaten_ghosts = [False, False, False, False]
                blinky_dead = False
                pinky_dead = False
                inky_dead = False
                clyde_dead = False
                score = 0
                live = 3
                level = level = copy.deepcopy(boards)
                game_over = False
                game_won = False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT and direction_command == 0:
                direction_command = direction
            if event.key == pygame.K_LEFT and direction_command == 1:
                direction_command = direction
            if event.key == pygame.K_UP and direction_command == 2:
                direction_command = direction
            if event.key == pygame.K_DOWN and direction_command == 3:
                direction_command = direction

    for i in range(4):
        if direction_command == i and turns_allowed[i]:
            direction = i

    if player_x > 655:
        player_x = 0
    elif player_x < -40:
        player_x = 650

    if blinky.in_box and blinky_dead:
        blinky_dead = False
    if inky.in_box and inky_dead:
        inky_dead = False
    if pinky.in_box and pinky_dead:
        pinky_dead = False
    if clyde.in_box and clyde_dead:
        clyde_dead = False

    pygame.display.flip()

pygame.quit()

import pygame
import sys
import random
from pygame.locals import *

# Set up pygame.
pygame.init()
mainClock = pygame.time.Clock()

# Set up the window.
windowSurface = pygame.display.set_mode((700, 500), 0, 32)
vertical_bounds = 500
horizontal_bounds = 700

# Set up the colors.
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (100, 25, 100)

# set graphics, stats, music
pong_boing = pygame.mixer.Sound('pong_boing.wav')
pong_start = pygame.mixer.Sound('pong_start.wav')
pong_player_lost = pygame.mixer.Sound('pong_playerLost.wav')
pong_player_won = pygame.mixer.Sound('pong_playerWon.wav')
set_font = pygame.font.SysFont("Times New Roman", 24, True)
set_bumper_speed = 6
set_puck_speed = 2
bumper_thickness = int(horizontal_bounds / 32)
bumper_length = int(vertical_bounds / 8)
set_puck_diameter = int(bumper_length / 3)
backgroundImage = pygame.image.load('pong_background.png')
backgroundStretchedImage = pygame.transform.scale(backgroundImage, (horizontal_bounds, vertical_bounds))
b2Image = pygame.image.load('pong_b1.jpg')
b2StretchedImage = pygame.transform.scale(b2Image, (bumper_thickness, bumper_length))
b2_aboveStretchedImage = pygame.transform.scale(b2Image, (bumper_length, bumper_thickness))
b2_belowStretchedImage = pygame.transform.scale(b2Image, (bumper_length, bumper_thickness))
b1Image = pygame.image.load('pong_b2.jpg')
b1StretchedImage = pygame.transform.scale(b1Image, (bumper_thickness, bumper_length))
b1_aboveStretchedImage = pygame.transform.scale(b1Image, (bumper_length, bumper_thickness))
b1_belowStretchedImage = pygame.transform.scale(b1Image, (bumper_length, bumper_thickness))


def global_draw(surface, text, font, draw_color, x_pos, y_pos):
    global_text = font.render(text, True, draw_color)
    surface.blit(global_text, (x_pos, y_pos))


class Bumper:
    def __init__(self, surface, x, y, xlen, ylen, moves_horizontal, bumper_speed, bumper_color, bumper_image):
        self.surface = surface
        self.x = x
        self.y = y
        self.xlen = xlen
        self.ylen = ylen
        self.moves_horizontal = moves_horizontal
        self.bumper_speed = bumper_speed
        self.bumper_color = bumper_color
        self.rect = pygame.Rect(x, y, xlen, ylen)
        self.image = bumper_image

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_rect(self):
        return self.rect

    def draw(self):
        pygame.draw.rect(self.surface, self.bumper_color, self.rect)
        self.surface.blit(self.image, self.rect)

    def move(self, dir1, dir2):
        if self.moves_horizontal:
            if dir1 and self.rect.left > horizontal_bounds/2:
                self.rect.left -= self.bumper_speed
                self.x -= self.bumper_speed
            if dir2 and self.rect.right < horizontal_bounds:
                self.rect.left += self.bumper_speed
                self.x += self.bumper_speed
        else:
            if dir1 and self.rect.bottom < vertical_bounds:
                self.rect.top += self.bumper_speed
                self.y += self.bumper_speed
            if dir2 and self.rect.top > 0:
                self.rect.top -= self.bumper_speed
                self.y -= self.bumper_speed

    def follow_puck(self, follow_puck_x, follow_puck_y):
        if self.moves_horizontal:
            if follow_puck_x - self.x > 0 and self.rect.right < horizontal_bounds/2:
                self.rect.left += (self.bumper_speed - 2)
                self.x += (self.bumper_speed - 2)
            if follow_puck_x - self.x < 0 and (self.rect.left > 0):
                self.rect.left -= (self.bumper_speed - 2)
                self.x -= (self.bumper_speed - 2)
        else:
            if follow_puck_y - self.y > 0 and self.rect.bottom < vertical_bounds:
                self.rect.top += (self.bumper_speed - 3)
                self.y += (self.bumper_speed - 3)
            if (follow_puck_y - self.y < 0) and (self.rect.top > 0):
                self.rect.top -= (self.bumper_speed - 3)
                self.y -= (self.bumper_speed - 3)


class Net:
    def __init__(self, surface, x, y, xlen, ylen, net_color):
        self.surface = surface
        self.x = x
        self.y = y
        self.xlen = xlen
        self.ylen = ylen
        self.net_color = net_color
        self.rect = pygame.Rect(x, y, xlen, ylen)

    def draw(self):
        pygame.draw.rect(self.surface, self.net_color, self.rect)


class Puck:
    def __init__(self, puck_diameter, puck_speed, puck_color):
        self.puck_x = int(horizontal_bounds/2)
        self.puck_y = int(vertical_bounds/2)
        self.surface = windowSurface
        self.puck_diameter = puck_diameter
        self.rect = pygame.Rect(self.puck_x, self.puck_y, self.puck_diameter, self.puck_diameter)
        self.puck_speed = puck_speed
        self.puck_color = puck_color
        ip = random.randint(1, 4)
        if ip == 1:
            self.Vx = -self.puck_speed
            self.Vy = self.puck_speed
        if ip == 2:
            self.Vx = -self.puck_speed
            self.Vy = -self.puck_speed
        if ip == 3:
            self.Vx = self.puck_speed
            self.Vy = self.puck_speed
        if ip == 4:
            self.Vx = self.puck_speed
            self.Vy = -self.puck_speed

    def get_x(self):
        return self.puck_x

    def get_y(self):
        return self.puck_y

    def move(self, collidable, puck_score):
        if self.puck_x + int(self.puck_diameter/2) <= 0 or self.puck_x + int(self.puck_diameter/2) >= horizontal_bounds:
            if self.puck_x + int(self.puck_diameter/2) < int(horizontal_bounds/2):
                puck_score.set_score(0, 1)
            else:
                puck_score.set_score(1, 0)
            self.reset_puck()
        if self.puck_y + int(self.puck_diameter/2) <= 0 or self.puck_y + int(self.puck_diameter/2) >= vertical_bounds:
            if self.puck_x + int(self.puck_diameter/2) < int(horizontal_bounds/2):
                puck_score.set_score(0, 1)
            else:
                puck_score.set_score(1, 0)
            self.reset_puck()
        for k in collidable:
            if self.rect.colliderect(k.get_rect()):
                if k.moves_horizontal:
                    self.Vy *= -1
                    pong_boing.play()
                else:
                    self.Vx *= -1
                    pong_boing.play()
        self.puck_x += self.puck_speed * self.Vx
        self.puck_y += self.puck_speed * self.Vy
        self.rect = pygame.Rect(self.puck_x, self.puck_y, self.puck_diameter, self.puck_diameter)

    def draw(self):
        pygame.draw.circle(self.surface, self.puck_color, (self.puck_x + int(self.puck_diameter/2), self.puck_y +
                                                           int(self.puck_diameter/2)), int(self.puck_diameter/2))

    def reset_puck(self):
        self.puck_x = int(horizontal_bounds / 2)
        self.puck_y = int(vertical_bounds / 2)
        ipr = random.randint(1, 4)
        if ipr == 1:
            self.Vx = -self.puck_speed
            self.Vy = self.puck_speed
        if ipr == 2:
            self.Vx = -self.puck_speed
            self.Vy = -self.puck_speed
        if ipr == 3:
            self.Vx = self.puck_speed
            self.Vy = self.puck_speed
        if ipr == 4:
            self.Vx = self.puck_speed
            self.Vy = -self.puck_speed


class Score:
    def __init__(self, surface, height, width):
        self.b1_score = 0
        self.b2_score = 0
        self.b1_score_needed = 11
        self.b2_score_needed = 11
        self.b1_game = 0
        self.b2_game = 0
        self.surface = surface
        self.height = height
        self.width = width
        self.win = 0

    def set_score(self, b2_score, b1_score):
        self.b1_score += b1_score
        self.b2_score += b2_score
        if b1_score == 1 and b2_score == 0:
            if self.b1_score > 9:
                self.b2_score_needed += 1
            self.b1_score_needed -= 1
        elif b1_score == 0 and b2_score == 1:
            if self.b2_score > 9:
                self.b1_score_needed += 1
            self.b2_score_needed -= 1
        if self.b2_score >= 11 and self.b2_score > (self.b1_score + 1):
            self.b2_game += 1
            self.b2_score = 0
            self.b2_score_needed = 11
            self.b1_score = 0
            self.b1_score_needed = 11
            pong_player_lost.play()
            if self.b2_game >= 3:
                self.win = 1
        elif self.b1_score >= 11 and self.b1_score > (self.b2_score + 1):
            self.b1_game += 1
            self.b1_score = 0
            self.b1_score_needed = 11
            self.b2_score = 0
            self.b2_score_needed = 11
            pong_player_won.play()
            if self.b1_game >= 3:
                self.win = 2

    def draw(self, font, draw_color):
        text_font_b2_score = font.render(str(self.b2_score) + "/" + str(self.b2_score_needed) + " : " +
                                         str(self.b2_game), True, draw_color)
        self.surface.blit(text_font_b2_score, (int(self.width/4), int(self.height / 8)))
        text_font_b1_score = font.render(str(self.b1_score) + "/" + str(self.b1_score_needed) + " : " +
                                         str(self.b1_game), True, draw_color)
        self.surface.blit(text_font_b1_score, (self.width - int(self.width / 4), int(self.height / 8)))

    def reset_score(self):
        self.b1_score = 0
        self.b2_score = 0
        self.b1_game = 0
        self.b2_game = 0
        self.b1_score_needed = 11
        self.b2_score_needed = 11
        self.win = 0
        pong_start.play()


# set up objects
b2 = Bumper(windowSurface, 0, int(vertical_bounds/2) - int(bumper_length/2), bumper_thickness, bumper_length, False,
            set_bumper_speed, RED, b2StretchedImage)
b2_above = Bumper(windowSurface, 0, 0, bumper_length, bumper_thickness, True, set_bumper_speed, RED,
                  b2_aboveStretchedImage)
b2_below = Bumper(windowSurface, 0, (vertical_bounds - bumper_thickness), bumper_length, bumper_thickness, True,
                  set_bumper_speed, RED, b2_belowStretchedImage)
b1 = Bumper(windowSurface, horizontal_bounds - bumper_thickness, int(vertical_bounds/2) - int(bumper_length/2),
            bumper_thickness, bumper_length, False, set_bumper_speed, BLACK, b1StretchedImage)
b1_above = Bumper(windowSurface, horizontal_bounds - bumper_length, 0, bumper_length, bumper_thickness, True,
                  set_bumper_speed, BLACK, b1_aboveStretchedImage)
b1_below = Bumper(windowSurface, horizontal_bounds - bumper_length, vertical_bounds - bumper_thickness,
                  bumper_length, bumper_thickness, True, set_bumper_speed, BLACK, b1_belowStretchedImage)
new_puck = Puck(set_puck_diameter, set_puck_speed, PURPLE)
set_collidable_list = [b1, b1_above, b1_below, b2, b2_above, b2_below]
new_score = Score(windowSurface, vertical_bounds, horizontal_bounds)
i = 0
net_dash = []
for i in range(16):
    if i % 2 != 0:
        net_dash.append(Net(windowSurface, int(horizontal_bounds/2),
                            i * int(vertical_bounds/16), int(horizontal_bounds/64), int(vertical_bounds/16), WHITE))

# movement
move_left = False
move_right = False
move_up = False
move_down = False
restart = False
intermission = False

pong_start.play()
# game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == K_UP or event.key == K_w:
                move_down = False
                move_up = True
            if event.key == K_DOWN or event.key == K_s:
                move_down = True
                move_up = False
            if event.key == K_LEFT or event.key == K_a:
                move_right = False
                move_left = True
            if event.key == K_RIGHT or event.key == K_d:
                move_right = True
                move_left = False
            if event.key == K_SPACE:
                restart = True
        if event.type == pygame.KEYUP:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == K_UP or event.key == K_w:
                move_up = False
            if event.key == K_DOWN or event.key == K_s:
                move_down = False
            if event.key == K_LEFT or event.key == K_a:
                move_left = False
            if event.key == K_RIGHT or event.key == K_d:
                move_right = False
            if event.key == K_SPACE:
                restart = False
    # draw the background
    windowSurface.blit(backgroundStretchedImage, (0, 0))
    # move the bumpers, and the puck
    b1.move(move_down, move_up)
    b1_above.move(move_left, move_right)
    b1_below.move(move_left, move_right)
    b2.follow_puck(new_puck.get_x(), new_puck.get_y())
    b2_above.follow_puck(new_puck.get_x(), new_puck.get_y())
    b2_below.follow_puck(new_puck.get_x(), new_puck.get_y())
    if not intermission:
        new_puck.move(set_collidable_list, new_score)
    # draw bumpers on surface
    for i in net_dash:
        i.draw()
    b1.draw()
    b1_above.draw()
    b1_below.draw()
    b2.draw()
    b2_above.draw()
    b2_below.draw()
    new_puck.draw()
    new_score.draw(set_font, BLACK)
    if new_score.win == 2:
        pong_player_won.play()
        global_draw(windowSurface, "Player wins", set_font, BLACK, int(horizontal_bounds/2), int(vertical_bounds/4))
        global_draw(windowSurface, "SPACE to play again", set_font, BLACK, int(horizontal_bounds / 2),
                    int(vertical_bounds / 4) + 64)
        intermission = True
        if restart:
            intermission = False
            new_puck.reset_puck()
            new_score.reset_score()
    elif new_score.win == 1:
        pong_player_lost.play()
        global_draw(windowSurface, "CPU wins", set_font, BLACK, int(horizontal_bounds/2), int(vertical_bounds/4))
        global_draw(windowSurface, "SPACE to play again", set_font, BLACK, int(horizontal_bounds / 2),
                    int(vertical_bounds / 4) + 64)
        intermission = True
        if restart:
            intermission = False
            new_puck.reset_puck()
            new_score.reset_score()
    # draw display and update it
    pygame.display.update()
    mainClock.tick(40)

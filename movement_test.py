import pygame, sys
from pygame.locals import *
# import numpy as np

pygame.init()


size = width, height = 1280, 960

screen = pygame.display.set_mode(size)
rectangle = pygame.Rect(0, 0, 64, 64)
clock = pygame.time.Clock()
black = 0, 0, 0
red = 255, 0, 0
x_v, y_v = 0, 0
max_vel = 12
x_ia = 2
x_da = -1
grav_a = 2


def on_ground(rectangle):
    if rectangle.y >= height - rectangle.height:
        # print("on the ground")
        return True
    return False

def sign(n):
    if n < 0:
        return -1
    if n == 0:
        return 0
    return 1

grounded = False
double_jump = True
up_again = True
while 1:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            pygame.quit()
            sys.exit()
    keys = pygame.key.get_pressed()
    # print(type(rectangle))
    accel_factor = 1
    xdir = sign(x_v)
    if not grounded and on_ground(rectangle):
        # print("landing")
        landing = True
        double_jump = True
    else:
        landing = False
    grounded = on_ground(rectangle)
    if rectangle.y + rectangle.height >= height:
        y_v = 0
        rectangle.y = height - rectangle.height
    if rectangle.left <= 0:
        x_v += 20
        rectangle.x = 0
    if rectangle.right >= width:
        x_v += -20
        rectangle.x = width - rectangle.width
    if keys[K_UP]:
        if grounded or double_jump and up_again:
            # print("grounded or doublejump")
            print(double_jump)
            if not grounded:
                double_jump = False
            y_v = 0
            y_v -= 25
            up_again = False
    else:
        up_again = True
    if keys[K_DOWN]:
        y_v += grav_a
        if landing:
            y_v += -30
            x_v += xdir * 10
    if keys[K_LEFT] and grounded:
        x_v += -x_ia
    if keys[K_RIGHT] and grounded:
        x_v += x_ia
    if abs(x_v) > max_vel and grounded:
        x_v = xdir * max_vel
    if abs(y_v) > max_vel + 20:
        y_v = max_vel
    if not grounded:
        y_v += grav_a
        accel_factor = 1/2
    if abs(x_v) > 0 and not landing:
        x_v += xdir * x_da * accel_factor
    x_v = round(x_v)
    y_v = round(y_v)
    if not (x_v == 0 and y_v == 0):
        # print(f"Moving by ({x_v}, {y_v}, from ({rectangle.x}, {rectangle.y}))")
        rectangle = pygame.Rect.move(rectangle, x_v, y_v)
    screen.fill(black)
    pygame.draw.rect(screen, red, rectangle)
    pygame.display.flip()

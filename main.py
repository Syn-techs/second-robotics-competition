# import tensorflow as tf
import pygame
import timeit
import random
import numpy
import math
import time
import sys
import os


FPS = 10
width = 800
height = 600

title = "SECOND ROBOTICS COMPETITION"

# To enable stable fps
stabilization = True

# To disable stable fps
# stabilization = False

pygame.init()
screen = pygame.display.set_mode((width, height))

clock = pygame.time.Clock()

players = []

colors = {
    "white": (255, 255, 255),
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "dark blue": (5, 5, 60),
    "black": (0, 0, 0),
    "gray": (125, 125, 125),
    "dark gray": (40, 40, 40),
    "light gray": (160, 160, 160),
    "gay pink": (255, 20, 147)
}

field_wh = [(80, 120), (width-80, height-80)]
(a1, a2), (a3, a4) = field_wh[0], field_wh[1]
field_wh = [field_wh[0], field_wh[1], a1, a2, a3, a4]

defaults = {
    "playerStartPos": (width//2, height//2),
    "enemyStartPos": (width//2, height//2),
    "backgroundColor": colors["black"],
    "fieldColor": colors["light gray"]
}


class Robot(pygame.Rect):
    def __init__(self, name, typee, hp, max_speed, acc, px, imagee, angle=0, pos=(0, 0)):

        self.max_speed = max_speed
        self.angle = angle
        self.cur_speed = 0
        self.y_change = 0
        self.x_change = 0
        self.a_change = 0
        self.type = typee
        self.name = name
        self.pos = pos
        self.acc = acc
        self.px = px

        super(Robot, self).__init__(pos, (px, px))
        self.original_image = pygame.image.load(imagee).convert()
        self.image = self.original_image
        (x, y) = self.pos
        self.rect = self.image.get_rect().move((x - (self.px // 2), y - (self.px // 2)))

        # (x, y) = self.pos
        # self.rect = self.image.get_rect().move((x//2, y//2))

    def draw(self):
        self.angle = self.angle % 360

        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect.center = self.pos

        x, y = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        screen.blit(self.image, self.rect)

    @staticmethod
    def calcNew_xy(pos, speed, angle_in_radians):
        (x, y) = pos
        new_y = -(speed*math.cos(angle_in_radians))
        new_x = -(speed*math.sin(angle_in_radians))
        return new_x, new_y

    @staticmethod
    def angle_of_vectors(cx, cy, tx, ty, wx, wy):
        a = numpy.array([cx, cy])
        b = numpy.array([wx, wy])
        c = numpy.array([tx, ty])
        ba = a - b
        bc = c - b
        cosine_angle = numpy.dot(
            ba, bc) / (numpy.linalg.norm(ba) * numpy.linalg.norm(bc))
        angle = (numpy.arccos(cosine_angle)) * 180 / math.pi
        return angle

    def findAngleVec(self, targetPos):
        (tx, ty) = targetPos
        (cx, cy) = self.pos
        wx, wy = self.calcNew_xy(self.pos, self.px//2,
                                 math.radians(self.angle))
        wx, wy = wx+cx, wy+cy

        ang = self.angle_of_vectors(cx, cy, tx, ty, wx, wy)
        # print("cx: " + str(cx) + " cy: " + str(cy) + " wx: " + str(wx) + " wy: " +
        #       str(wy) + " self.angle: j" + str(self.angle) + " calculated ang: " + str(ang))
        return ang

    def turn(self, angle):
        if angle != 0:
            self.a_change += angle % 360
        else:
            self.a_change = 0

    def go(self, speed):
        # Edits ONLY x/y_change stuff
        self.x_change, self.y_change = self.calcNew_xy(
            self.pos, speed, math.radians(self.angle))

    def drawPivot(self):
        (x, y) = self.pos
        pygame.draw.rect(screen, colors["gray"], [
                         x-1, 0, 2, height])

        pygame.draw.rect(screen, colors["gray"], [
                         0, y-1, width, 2])


class Field(pygame.Rect):
    def __init__(self, name, hp, posL, posR, color=defaults["fieldColor"], t=5):
        self.color = color
        self.name = name
        self.posL = posL
        self.posR = posR
        self.hp = hp
        self.t = t

        (x, y) = self.posL
        (x_r, y_r) = self.posR
        super().__init__(posL, (x_r - x, y_r - y))

        self.boundaries = {
            "left: ": [x, hp],
            "right: ": [x_r, hp],
            "up: ": [y, hp],
            "down: ": [y_r, hp]
        }

    def draw(self):
        (x, y) = self.posL
        (x_r, y_r) = self.posR
        wid, hei = x_r - x, y_r - y

        pygame.draw.rect(screen, self.color, [
                         x-(self.t//2), y-(self.t//2), self.t, hei])

        pygame.draw.rect(screen, self.color, [
                         x_r-(self.t//2), y-(self.t//2), self.t, hei])

        pygame.draw.rect(screen, self.color, [
                         x-(self.t//2), y-(self.t//2), wid, self.t])

        pygame.draw.rect(screen, self.color, [
                         x-(self.t//2), y_r-(self.t//2), wid + self.t, self.t])

    def deleteSide(self, side=None):
        self.draw()

        (x, y) = self.posL
        (x_r, y_r) = self.posR

        if side is not None:
            if side.startswith("l"):
                pygame.draw.rect(screen, defaults["backgroundColor"], [
                                 x-(self.t//2), y-(self.t//2), self.t, x_r-x])
                # x
            # elif side.startswith("r"):
            #     # x_r
            # elif side.startswith("u"):
            #     # y
            # elif side.startswith("d"):
            #     # y_r

        # elif side is None and pos is None:
        else:
            for n, v in self.boundaries.items():
                if v[1] == 0:
                    self.deleteSide(side=n)

    def reduceHp(self, b, rhp):
        self.boundaries[b] = [self.boundaries[b]
                              [0], self.boundaries[b][1] - rhp]


migField = Field(
    "Marmara Inovasyon Gunleri",
    1,
    field_wh[0],
    field_wh[1],
)

player1 = Robot(
    "UGUR ABI",
    "player",
    100,
    16,
    1.6,
    64,
    "images/spaceship64.png",
    pos=defaults["playerStartPos"])

enemy1 = Robot(
    "TITAN",
    "enemy",
    100,
    10,
    1.2,
    64,
    "images/ufo64.png",
    pos=defaults["enemyStartPos"])


players.append(player1)
players.append(enemy1)


def gameInit():
    global screen
    global title
    # Like void setup(){}
    pygame.display.set_caption(title)


def runTime():
    global players
    global colors
    global height
    global width
    # Like void loop(){}

    screen.fill(defaults["backgroundColor"])

    for curPlayer in players:
        (x, y) = curPlayer.pos

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 0

            # TUSLARLA OYNAMA
            if curPlayer.type == "player":
                if event.type == pygame.KEYDOWN:
                    # if event.key in [pygame.K_LEFT, pygame.K_RIGHT] and curPlayer.y_change == 0:
                    if event.key == pygame.K_LEFT:
                        curPlayer.turn(curPlayer.max_speed)

                    if event.key == pygame.K_RIGHT:
                        curPlayer.turn(-curPlayer.max_speed)

                    # elif event.key in [pygame.K_DOWN, pygame.K_UP] and curPlayer.a_change == 0:
                    if event.key == pygame.K_UP:
                        curPlayer.cur_speed = 1

                    if event.key == pygame.K_DOWN:
                        curPlayer.cur_speed = -1

                if event.type == pygame.KEYUP:
                    if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                        curPlayer.a_change = 0

                    elif event.key in [pygame.K_DOWN, pygame.K_UP]:
                        curPlayer.y_change = 0
                        curPlayer.x_change = 0
                        curPlayer.cur_speed = 0
                # print(curPlayer.type + str(curPlayer.angle) + " --")

        ########################################################################################

        if curPlayer.type == "enemy":
            targetPlayer = None
            for i in range(len(players)):
                if players[i].type == "player":
                    targetPlayer = players[i]
                    break

            if targetPlayer.pos != curPlayer.pos:
                # (tx, ty) = targetPlayer.pos
                # (cx, cy) = curPlayer.pos
                # curPlayer.cur_speed = 1
                oldAng = curPlayer.findAngleVec(targetPlayer.pos)
                curPlayer.angle += 1
                newAng = curPlayer.findAngleVec(targetPlayer.pos)
                curPlayer.angle -= 1

                if oldAng < newAng and newAng < 175:  # hedefe doğru (sola) dön
                    if newAng > 150:  # eğer çok solda değilse dönerek ilerle
                        curPlayer.turn(1)
                        curPlayer.cur_speed = 1

                    else:  # eğer çok soldaysa ileri gitmeden dön
                        curPlayer.turn(1)
                        curPlayer.cur_speed = 0

                # hedefe doğru (sağa) dön
                elif oldAng >= newAng and newAng < 175:
                    if newAng > 150:  # eğer çok sağda değilse dönerek ilerle
                        curPlayer.turn(-1)
                        curPlayer.cur_speed = 1

                    else:  # eğer çok sağdaysa ileri gitmeden dön
                        curPlayer.turn(-1)
                        curPlayer.cur_speed = 0

                else:
                    curPlayer.turn(0)  # Ortadaysa dönmeyi durdur

        curPlayer.cur_speed *= curPlayer.acc
        if curPlayer.cur_speed > curPlayer.max_speed:
            curPlayer.cur_speed = curPlayer.max_speed

        elif curPlayer.cur_speed < -curPlayer.max_speed:
            curPlayer.cur_speed = -curPlayer.max_speed

        if curPlayer.cur_speed != 0:
            curPlayer.x_change, curPlayer.y_change = Robot.calcNew_xy(
                curPlayer.pos, curPlayer.cur_speed, math.radians(curPlayer.angle))

        # İki farklı sınır olmasının sebebi sahanın kırılabilme özelliğinin olması

        # region SCREEN LIMITS
        if (height - (curPlayer.px // 2) < y + curPlayer.y_change and curPlayer.y_change > 0):  # aşağı sınır
            curPlayer.y_change = (height-(curPlayer.px//2)) - y

        elif (curPlayer.px//2 > y + curPlayer.y_change and curPlayer.y_change < 0):  # yukarı sınır
            curPlayer.y_change = (curPlayer.px//2) - y

        if (width - (curPlayer.px // 2) < x + curPlayer.x_change and curPlayer.x_change > 0):  # sağ sınır
            curPlayer.x_change = (width-(curPlayer.px//2)) - x

        elif (curPlayer.px//2 > x + curPlayer.x_change and curPlayer.x_change < 0):  # sol sınır
            curPlayer.x_change = (curPlayer.px//2) - x
        # endregion

        # region FIELD LIMITS
        bx, by = migField.posL
        bx_r, by_r = migField.posR

        if (abs(by_r - (curPlayer.px // 2)) < y + curPlayer.y_change and curPlayer.y_change > 0 and migField.hp > 0):  # aşağı sınır
            curPlayer.y_change = abs(by_r - (curPlayer.px // 2)) - y
            curPlayer.x_change, curPlayer.a_change = 0, 0

        elif (by + (curPlayer.px//2) > y + curPlayer.y_change and curPlayer.y_change < 0 and migField.hp > 0):  # yukarı sınır
            curPlayer.y_change = by + (curPlayer.px//2) - y
            curPlayer.x_change, curPlayer.a_change = 0, 0

        if (abs(bx_r - (curPlayer.px // 2)) < x + curPlayer.x_change and curPlayer.x_change > 0 and migField.hp > 0):  # sağ sınır
            curPlayer.x_change = abs(bx_r-(curPlayer.px//2)) - x
            curPlayer.y_change, curPlayer.a_change = 0, 0

        elif (bx + (curPlayer.px//2) > x + curPlayer.x_change and curPlayer.x_change < 0 and migField.hp > 0):  # sol sınır
            curPlayer.x_change = (bx + (curPlayer.px//2)) - x
            curPlayer.y_change, curPlayer.a_change = 0, 0
        # endregion

        curPlayer.pos = (x + curPlayer.x_change, y + curPlayer.y_change)
        curPlayer.angle += curPlayer.a_change

        curPlayer.draw()

    migField.draw()

    pygame.display.update()
    return True


def configFps(configFunc, runtimeFunc):
    global stabilization
    global FPS
    isRunning = True
    configFunc()
    if stabilization:
        while isRunning:
            clock.tick(FPS)
            isRunning = runtimeFunc()
        pygame.quit()
    else:
        while isRunning:
            isRunning = runtimeFunc()
        pygame.quit()


if __name__ == "__main__":
    configFps(gameInit, runTime)

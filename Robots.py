from settings import *
import pygame
import math
import numpy


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


players = []

player1 = Robot(
    "UGUR ABI",
    "player",
    100,
    5,
    1.2,
    64,
    "images/spaceship64.png",
    pos=defaults["playerStartPos"],
    angle=defaults["playerStartAngle"])

enemy1 = Robot(
    "TITAN",
    "enemy",
    100,
    3,
    1.2,
    64,
    "images/ufo64.png",
    pos=defaults["enemyStartPos"],
    angle=defaults["enemyStartAngle"])


players.append(player1)
# players.append(enemy1)

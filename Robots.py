from settings import *
from Field import *
import pygame
import math
import numpy


class Robot(pygame.Rect):
    global width
    global height
    global migField

    def __init__(self, name, typee, hp, max_speed, acc, px, imagee, angle=0, pos=(0, 0)):

        self.max_speed = max_speed
        self.angle = angle
        self.boundaries = []
        self.cur_speed = 0
        self.y_change = 0
        self.x_change = 0
        self.a_change = 0
        self.type = typee
        self.name = name
        self.pos = pos
        self.acc = acc
        self.hp = hp
        self.px = px

        super(Robot, self).__init__(pos, (px, px))
        self.original_image = pygame.image.load(imagee).convert()
        self.image = self.original_image
        (x, y) = self.pos
        self.rect = self.image.get_rect().move((x - (self.px // 2), y - (self.px // 2)))

        # ekran sınırı eklendi
        self.boundaries.append(["screen", (0, 0), (width, height)])
        # arena sınır eklendi
        self.boundaries.append(
            ["field", migField.posL, migField.posR, migField.hp])

    def update(self):
        (x, y) = self.pos

        # Açı sınırlaması
        self.angle = self.angle % 360

        # Hızımın artıyoooor
        self.cur_speed *= self.acc

        # Tabii sınıra kadar
        if self.cur_speed > self.max_speed:
            self.cur_speed = self.max_speed

        # Geri giderken ışık hızına çıkmak için altakki satırı sil
        elif self.cur_speed < -(self.max_speed):
            self.cur_speed = -(self.max_speed)

        # Eğer hareket ediyorsak (dönme sayılmaz) açıya göre ne tarafa gideceğimizi hesapla
        if self.cur_speed != 0:
            self.x_change, self.y_change = Robot.calcNew_xy(
                self.pos, self.cur_speed, math.radians(self.angle))

        for player in players:
            if player.name != self.name:
                self.roboControl(player)

        # Ekran sınırları
        self.boundaryControl(self.boundaries[0][1], self.boundaries[0][2])
        # Arena sınrılaması
        self.boundaryControl(
            self.boundaries[1][1], self.boundaries[1][2], self.boundaries[1][3])

        # İlerlemeyi işle
        self.pos = (x + self.x_change, y + self.y_change)
        self.angle += self.a_change

    # region boundary control funcs

    def isOnBoundary(self, leftBoundaryPos, rightBoundaryPos, fieldHp=1):
        (x, y) = self.pos
        leftl, upl = leftBoundaryPos
        rightl, downl = rightBoundaryPos

        if (abs(downl - (self.px // 2)) <= y + self.y_change and (self.y_change > 0 or self.a_change != 0) and fieldHp > 0):  # aşağı sınır
            return "down"

        elif (upl + (self.px//2) >= y + self.y_change and (self.y_change < 0 or self.a_change != 0) and fieldHp > 0):  # yukarı sınır
            return "up"

        if (abs(rightl - (self.px // 2)) <= x + self.x_change and (self.x_change > 0 or self.a_change != 0) and fieldHp > 0):  # sağ sınır
            return "right"

        elif (leftl + (self.px//2) >= x + self.x_change and (self.x_change < 0 or self.a_change != 0) and fieldHp > 0):  # sol sınır
            return "left"

        return "none"

    def boundaryControl(self, leftBoundaryPos, rightBoundaryPos, fieldHp=1):
        (x, y) = self.pos
        bx, by = leftBoundaryPos
        bx_r, by_r = rightBoundaryPos

        isOnBound = self.isOnBoundary(
            leftBoundaryPos, rightBoundaryPos, fieldHp)

        if isOnBound.startswith("d"):  # aşağı sınır
            self.y_change = abs(by_r - (self.px // 2)) - y
            self.x_change, self.a_change = 0, 0

        elif isOnBound.startswith("u"):  # yukarı sınır
            self.y_change = by + (self.px // 2) - y
            self.x_change, self.a_change = 0, 0

        if isOnBound.startswith("r"):  # sağ sınır
            self.x_change = abs(bx_r - (self.px // 2)) - x
            self.y_change, self.a_change = 0, 0

        elif isOnBound.startswith("l"):  # sol sınır
            self.x_change = (bx + (self.px // 2)) - x
            self.y_change, self.a_change = 0, 0

    # endregion

    def isOnRobotBound(self, curEnemy):
        (x, y) = self.pos
        x_new, y_new = x + self.x_change, y + self.y_change

        (leftl, upl) = ((curEnemy.pos[0] - (self.px // 2 + curEnemy.px // 2)),
                        (curEnemy.pos[1] - (self.px // 2 + curEnemy.px // 2)))

        (rightl, downl) = ((curEnemy.pos[0] + (self.px // 2 + curEnemy.px // 2)),
                           (curEnemy.pos[1] + (self.px // 2 + curEnemy.px // 2)))

        # Eğer aktifkonumu onun içinde değilse ve oraya girmeye çalışırsa durdur

        if ((x_new > leftl) and (x_new < rightl) and (y_new > upl) and (y_new < downl)) or ((x > leftl) and (x < rightl) and (y > upl) and (y < downl)):
            if x < leftl:
                return "left"

            elif x > rightl:
                return "right"

            if y < upl:
                return "up"

            elif y > downl:
                return "down"

            # else:
            return "inside"

        else:
            return "none"

    def roboControl(self, curEnemy):
        isOnBound = self.isOnRobotBound(curEnemy)
        isEnemyOnBound = curEnemy.isOnBoundary(
            migField.posL, migField.posR, migField.hp)

        if not isEnemyOnBound.startswith("n") and curEnemy.type == "player":
            print(curEnemy.name + " " + isEnemyOnBound)

        (leftl, upl) = (curEnemy.pos[0] - self.px, curEnemy.pos[1] - self.px)

        (rightl, downl) = (curEnemy.pos[0] +
                           self.px, curEnemy.pos[1] + self.px)

        if isOnBound.startswith("n") or (curEnemy.x_change > 0 and self.x_change > 0) or (curEnemy.x_change < 0 and self.x_change < 0) or (curEnemy.y_change > 0 and self.y_change > 0) or (curEnemy.y_change < 0 and self.y_change < 0):
            pass

        elif isEnemyOnBound.startswith("n"):
            # X DEĞİŞİMİ

            if abs(self.x_change) == abs(curEnemy.x_change):
                self.x_change, self.a_change = 0, 0

            elif abs(curEnemy.x_change) > abs(self.x_change):
                if curEnemy.x_change > 0:
                    self.x_change, self.a_change = (
                        curEnemy.x_change - self.x_change), 0
                else:
                    self.x_change, self.a_change = (
                        curEnemy.x_change + self.x_change), 0

            elif abs(curEnemy.x_change) < abs(self.x_change):
                if self.x_change > 0:
                    self.x_change, self.a_change = (
                        self.x_change - curEnemy.x_change), 0
                else:
                    self.x_change, self.a_change = (
                        self.x_change + curEnemy.x_change), 0

            # Y DEĞİŞİMİ

            if abs(self.y_change) == abs(curEnemy.y_change):
                self.y_change, self.a_change = 0, 0

            elif abs(curEnemy.y_change) > abs(self.y_change):
                if curEnemy.y_change > 0:
                    self.y_change, self.a_change = (
                        curEnemy.y_change - self.y_change), 0
                else:
                    self.y_change, self.a_change = (
                        curEnemy.y_change + self.y_change), 0

            elif abs(curEnemy.y_change) < abs(self.y_change):
                if self.y_change > 0:
                    self.y_change, self.a_change = (
                        self.y_change - curEnemy.y_change), 0
                else:
                    self.y_change, self.a_change = (
                        self.y_change + curEnemy.y_change), 0

        else:
            self.x_change, self.y_change, self.a_change, self.cur_speed = 0, 0, 0, 0

    def draw(self):
        self.update()

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
        return ang

    def turn(self, angle):
        angle = 0 - angle  # sağ sol olayını ters çevirdim
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
        self.draw()
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
players.append(enemy1)

# import tensorflow as tf
from settings import *
from Robots import *
from Field import *
import pygame
import timeit
import random
import numpy
import math
import time
import sys
import os


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

                # print(newAng)

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

        curPlayer.boundaryControl((0, 0), (width, height))
        curPlayer.boundaryControl(migField.posL, migField.posR, migField.hp)

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

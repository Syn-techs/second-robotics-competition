import pygame

FPS = 60
width = 800
height = 600

title = "SECOND ROBOTICS COMPETITION"

# To enable stable fps
stabilization = True

# To disable stable fps
# stabilization = False

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
    "playerStartPos": (field_wh[2] + 100, field_wh[3] + 100),
    "playerStartAngle": 219.80557109226518,
    "enemyStartPos": (field_wh[4] - 100, field_wh[5] - 100),
    "enemyStartAngle": 39.80557109226519,
    "backgroundColor": colors["black"],
    "fieldColor": colors["light gray"]
}


pygame.init()
screen = pygame.display.set_mode((width, height))

clock = pygame.time.Clock()

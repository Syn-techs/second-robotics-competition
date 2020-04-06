import pygame

width, height = 800, 600

pygame.init()
screen = pygame.display.set_mode((width, height))


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


def main():
    isRunning = True
    while isRunning:
        screen.fill(colors["gray"])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                isRunning = False

        rect = pygame.Rect((100, 100), (width-100, height-100))

        pygame.draw.rect(screen, colors["red"], [100, 100, 600, 400], 5)
        pygame.display.update()


if __name__ == "__main__":
    main()

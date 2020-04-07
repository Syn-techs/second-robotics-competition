from settings import *


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

import arcade

WIDTH = 800
HEIGHT = 600
beer_speed = 7


class Beer(arcade.Sprite):  # changed this class
    def __init__(self, image, scale, full):
        super().__init__(image, scale)
        self.full = full

    def update(self):
        if self.full is True:
            self.center_x -= beer_speed
            if self.left < 0:
                self.kill()
        else:
            self.center_x += beer_speed
            if self.right > WIDTH:
                self.kill()

    def get_full(self):
        return self.full

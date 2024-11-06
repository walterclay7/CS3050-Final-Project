import arcade

WIDTH = 800
HEIGHT = 600


# class for player sprite
class Player(arcade.Sprite):
    def update(self):
        # check for out of bounds
        if self.left < 0:
            self.left = 0
        elif self.right > WIDTH - 1:
            self.right = WIDTH - 1

        if self.bottom < 0:
            self.bottom = 0
        elif self.top > HEIGHT - 1:
            self.top = HEIGHT - 1
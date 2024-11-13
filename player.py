import arcade

WIDTH = 800
HEIGHT = 600


# class for player sprite
class Player(arcade.Sprite):

    def __init__(self, image, scale, moving_left, moving_right, *args, **kwargs):
        super().__init__(image, scale)
        self.moving_left = moving_left
        self.moving_right = moving_right

    def update(self):
        # horizontal movement - Move left or right if the respective key is held down
        if self.moving_left:
            self.center_x -= 6
        if self.moving_right:
            self.center_x += 6

        # check for out of bounds
        if self.left < 90:
            self.left = 90
        elif self.right > WIDTH - 50:
            self.right = WIDTH - 50

        if self.bottom < 0:
            self.bottom = 0
        elif self.top > HEIGHT - 1:
            self.top = HEIGHT - 1

    def get_moving_left(self):
        return self.moving_left

    def set_moving_left(self, moving_left):
        self.moving_left = moving_left

    def get_moving_right(self):
        return self.moving_right

    def set_moving_right(self, moving_right):
        self.moving_right = moving_right

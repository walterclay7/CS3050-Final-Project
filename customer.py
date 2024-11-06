import arcade
from beer import Beer

WIDTH = 800
HEIGHT = 600
person_speed = 2


class Customer(arcade.Sprite):
    def __init__(self, image, scale, bar_index, view, *args, **kwargs):
        super().__init__(image, scale, *args, **kwargs)
        self.bar_index = bar_index
        self.view = view
        self.drinking = False

    def throw_empty_glass(self, all_bars_y):  # changed this method
        empty_glass = Beer("images/Tapper_mug_empty.png", 0.55, False)
        empty_glass.center_x = self.center_x
        empty_glass.center_y = all_bars_y[self.bar_index] + 50
        self.view.beer_list.append(empty_glass)

    def update(self):
        self.center_x += person_speed  # change to += beer_speed to reverse
        if self.right > WIDTH:  # reversed
            self.kill()

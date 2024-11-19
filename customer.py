import arcade
from beer import Beer
import time

WIDTH = 800
HEIGHT = 600
person_speed = 2


class Customer(arcade.Sprite):
    def __init__(self, image, scale, bar_index, view, *args, **kwargs):
        super().__init__(image, scale, *args, **kwargs)
        self.bar_index = bar_index
        self.view = view
        self.drinking = False
        self.all_bars_y = None
        self.distance_moved = 0

    def hit_customer(self, all_bars_y):
        # also pushes customer back from being hit by beer
        self.drinking = True
        self.all_bars_y = all_bars_y

    def update(self):
        if not self.drinking:
            self.center_x += person_speed  # standard customer movement moving forward
        if self.drinking:
            self.center_x -= person_speed*3   # when customer gets hit with beer it moves backward
            self.distance_moved += person_speed*3  # keeps track of distance

        if self.distance_moved == 300:  # when reached that distance, stops moving backward
            self.drinking = False  # this var is used to switch customers between when they have beer and when they dont
            self.throw_empty_beer_glass()   # throws glass
            self.distance_moved = 0  # resets distance moved

        if self.right > WIDTH:  # bounds checker
            self.kill()

    def throw_empty_beer_glass(self):
        # actually creates empty mug and sends it
        empty_glass = Beer("images/Tapper_mug_empty.png", 0.55, False)
        empty_glass.center_x = self.center_x
        empty_glass.center_y = self.all_bars_y[self.bar_index] + 50
        self.view.beer_list.append(empty_glass)

    def get_drinking(self):
        return self.drinking

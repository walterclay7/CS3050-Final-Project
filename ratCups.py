from typing import Tuple

import arcade
import random
import math

WIDTH = 800
HEIGHT = 600
num_cups = 6

class RatGame(arcade.Window):
    def __init__(self):
        super().__init__(WIDTH, HEIGHT, 'Rat Bonus Round')
        self.cup_list=arcade.SpriteList()
        self.rat= None
        self.untouched_cup= None
        self.guy = None
        self.correct=False
        #keep track of stuff...
        self.current_touch_index=0
        self.is_shuffling= False
        self.touch_order = []
        self.shuffle_time = 0.0
        self.steps=[]


    def setup(self):
        for i in range(num_cups):
            cup = arcade.Sprite('images/cup_image.jpg', 0.2)
            cup.center_x = 100 + i * 100
            cup.center_y = HEIGHT // 2
            cup.target_x = cup.center_x
            cup.target_y = cup.center_y
            self.cup_list.append(cup)

        self.rat = arcade.Sprite('images/rat_image.png', 0.5) #my rat <3
        self.untouched_cup = random.choice(self.cup_list)
        self.touch_order = [cup for cup in self.cup_list if cup != self.untouched_cup]
        random.shuffle(self.touch_order)
        arcade.schedule(self.touch_next_cup, 0.5)

    def touch_next_cup(self, dt):
        if self.current_touch_index >= len(self.touch_order):
            arcade.unschedule(self.touch_next_cup)
            self.start_shuffling()
            return
        cup = self.touch_order[self.current_touch_index]
        self.rat.center_x=cup.center_x
        self.rat.center_y=cup.center_y

        self.current_touch_index += 1


    def start_shuffling(self):
        self.is_shuffling = True
        self.shuffle_time=0.0
        self.rat.visible=False
        arcade.schedule(self.shuffle_cups, 0.3)



    def stop_shuffling(self):
        self.is_shuffling = False
        arcade.unschedule(self.shuffle_cups)
        self.guy = arcade.Sprite('images/guy_image.png', 0.2)
        # make him sart at the first cup
        self.guy.center_x = 100
        self.guy.center_y = HEIGHT // 2 + 50

    def shuffle_cups(self, dt):
        if not self.is_shuffling:
            return

        cup1, cup2 = random.sample(list(self.cup_list), 2)

        cup1.target_x = cup2.center_x
        cup1.target_y = cup2.center_y
        cup2.target_x = cup1.center_x
        cup2.target_y = cup1.center_y

        speed = 7
        cup1.change_x = (cup1.target_x-cup1.center_x)/ speed
        cup1.change_y = (cup1.target_y-cup1.center_y)/ speed
        cup2.change_x = (cup2.target_x-cup2.center_x)/ speed
        cup2.change_y = (cup2.target_y-cup2.center_y)/ speed

        self.shuffle_time += dt
        if self.shuffle_time >= 3.0:
            self.stop_shuffling()

    def on_update(self, delta_time):
        for cup in self.cup_list:
            cup.center_x += cup.change_x
            cup.center_y += cup.change_y

            if abs(cup.center_x - cup.target_x) < 1 and abs(cup.center_y - cup.target_y) < 1:
                cup.center_x = cup.target_x
                cup.center_y = cup.target_y
                cup.change_x = 0
                cup.change_y = 0

    def on_key_press(self, symbol, modifiers):
        if self.guy and self.guy.visible:
            if symbol == arcade.key.RIGHT:
                self.guy.center_x += 100
            elif symbol == arcade.key.LEFT:
                self.guy.center_x -= 100
            elif symbol == arcade.key.ENTER:
                if abs(self.guy.center_x - self.untouched_cup.center_x) < 50:
                    print("Correct! You guessed the right cup.")
                    self.correct=True
                else:
                    print("Wrong! Try again.")

    def on_draw(self):
        arcade.start_render()
        arcade.draw_rectangle_filled(WIDTH // 2, HEIGHT // 2, WIDTH, HEIGHT, arcade.color.BLUE)
        if self.guy:
            self.guy.draw()
        if self.rat:
            self.rat.draw()
        arcade.draw_rectangle_filled(WIDTH // 2, HEIGHT // 4, WIDTH, 300, arcade.color.BRONZE)
        #ninas budweiser sign
        tpoints = [
            (385, 575),  # top center **
            (500, 600),  # top right
            (500, 500),  # bottom right
            (385, 530),  # bottom center **
            (300, 500),  # bottom left
            (300, 600)  # top left
        ]

        arcade.draw_polygon_filled(tpoints, arcade.color.RED)

        arcade.draw_text("Budweiser", WIDTH / 2, HEIGHT - 55,
                         arcade.color.WHITE, font_size=20, anchor_x="center")

        self.cup_list.draw()
        if self.rat:
            self.rat.draw()




game = RatGame()
game.setup()
arcade.run()


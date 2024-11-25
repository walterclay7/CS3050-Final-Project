import arcade
from tapper import Tapper
from ratCups import RatGame
from player import Player
from beer import Beer
import os


# variables for MenuView
WIDTH = 800
HEIGHT = 600

FONT_PATH = "fonts/Galada-Regular.ttf"
arcade.load_font(FONT_PATH)

class MenuView(arcade.View):
    def __init__(self):
        super().__init__()
        self.player_sprite = None
        self.beer_list = None
    def on_show_view(self):
        arcade.set_background_color(arcade.color.WHITE)

        self.player_sprite = Player("images/Tapper_bartender.png", 1, moving_left=False, moving_right=False,
                                    flipped_horizontally=True)
        # self.player_sprite = Player("images/Tapper_bartender.png", .75)
        self.player_sprite.center_x = WIDTH / 2 - 35
        self.player_sprite.center_y = HEIGHT / 2

        self.beer_list = arcade.SpriteList()
        beer_sprite = Beer("images/Tapper_mug_full.png", scale=0.7, full=True)
        # flip so the handle is on the left
        beer_sprite.texture = arcade.load_texture("images/Tapper_mug_full.png", mirrored=True)
        beer_sprite.center_x = WIDTH / 2 + 45
        beer_sprite.center_y = HEIGHT / 2 + 18
        self.beer_list.append(beer_sprite)

    def on_draw(self):

        # arcade.draw_rectangle_filled(WIDTH / 2, HEIGHT / 2, 20, arcade.color.ORANGE_PEEL)
        # arcade.draw_rectangle_filled(WIDTH / 2, HEIGHT / 2, WIDTH * 0.75, 200, arcade.color.BLUE)

        self.clear()
        scale = 1.5

        # Screen center
        screen_center_x = WIDTH / 2
        screen_center_y = HEIGHT / 2 + 130

        # Original points
        points = [
            (385, 575),  # top center **
            (500, 600),  # top right
            (500, 500),  # bottom right
            (385, 530),  # bottom center **
            (300, 500),  # bottom left
            (300, 600)  # top left
        ]

        # center of the original points
        original_center_x = sum(x for x, _ in points) / len(points)
        original_center_y = sum(y for _, y in points) / len(points)

        # rescale
        scaled_points = [
            (
                int((x - original_center_x) * scale + screen_center_x),
                int((y - original_center_y) * scale + screen_center_y)
            )
            for x, y in points
        ]

        # draw budweiser sign
        arcade.draw_polygon_filled(scaled_points, arcade.color.RED)

        arcade.draw_text("TAPPER", WIDTH / 2, HEIGHT / 2 + 103,
                          arcade.color.BLACK, font_size=50, anchor_x="center", font_name=FONT_PATH)

        if self.player_sprite:
            self.player_sprite.draw()

        if self.player_sprite:
            self.beer_list.draw()


        arcade.draw_text("Click to advance", WIDTH / 2, HEIGHT / 2 - 100,
                         arcade.color.GRAY, font_size=20, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        instructions_view = InstructionView()
        self.window.show_view(instructions_view)


class InstructionView(arcade.View):
    def on_show_view(self):
        arcade.set_background_color(arcade.color.ORANGE_PEEL)

    def on_draw(self):
        self.clear()
        arcade.draw_text("Instructions: ", WIDTH / 2, HEIGHT / 2 + 40,
                         arcade.color.BLACK, font_size=20, anchor_x="center", multiline=True)
        arcade.draw_text("Move using the up and down arrows.", WIDTH / 2, HEIGHT / 2 + 10,
                         arcade.color.BLACK, font_size=20, anchor_x="center", multiline=True)
        arcade.draw_text("Use the space bar to serve the drinks", WIDTH / 2, HEIGHT / 2 - 20,
                         arcade.color.BLACK, font_size=20, anchor_x="center", multiline=True)
        arcade.draw_text("Click to advance", WIDTH / 2, HEIGHT / 2 - 95,
                         arcade.color.GRAY, font_size=20, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = Tapper()
        self.window.show_view(game_view)


class GameOverView(arcade.View):
    def __init__(self):
        super().__init__()

    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        self.clear()
        """
        Draw "Game over" across the screen.
        """
        arcade.draw_text("Game Over", 240, 400, arcade.color.WHITE, 54)
        arcade.draw_text("Click to restart", 310, 300, arcade.color.WHITE, 24)

        output_total = f"Total Score: {self.window.total_score}"
        arcade.draw_text(output_total, 10, 10, arcade.color.WHITE, 14)



    def on_mouse_press(self, _x, _y, _button, _modifiers):
        self.window.lives = 3
        self.window.total_score = 0
        game_view = Tapper()
        self.window.show_view(game_view)


class RoundWinView(arcade.View):
    def __init__(self, round_number):
        super().__init__()
        self.round_number = round_number

    def on_show_view(self):
        arcade.set_background_color(arcade.color_from_hex_string("#FFD700"))  # Gold background for a win

    def on_draw(self):
        self.clear()
        arcade.draw_text(f"Round {self.round_number} Complete!", WIDTH / 2, HEIGHT / 2 + 50,
                         arcade.color.BLACK, font_size=40, anchor_x="center")
        arcade.draw_text("Click to start the next round", WIDTH / 2, HEIGHT / 2 - 50,
                         arcade.color.GRAY, font_size=20, anchor_x="center")
        if self.round_number == 2 or self.round_number == 4:
            arcade.draw_text("GET READY", WIDTH / 2, HEIGHT / 2 - 200,
                             arcade.color.BLACK, font_size=40, anchor_x="center")
            arcade.draw_text("Press 'Enter' to select the beer that has not been poisoned", WIDTH / 2, HEIGHT / 2 - 250,
                             arcade.color.BLACK, font_size=20, anchor_x="center", multiline=True)

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        # Transition back to the game view
        game_view = Tapper()
        game_view.round = self.round_number + 1  # Increment the round
        game_view.reset_round()  # Reset for the next round
        #after round 2 bring up rat round
        if game_view.round == 3 or game_view.round == 5:
            rat_game = RatGame(game_view.score, self.round_number)
            rat_game.setup()
            self.window.show_view(rat_game)
        else:
            self.window.show_view(game_view)
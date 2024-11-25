import arcade
from tapper import Tapper
from ratCups import RatGame

# variables for MenuView
WIDTH = 800
HEIGHT = 600


class MenuView(arcade.View):
    def on_show_view(self):
        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        self.clear()
        arcade.draw_text("Tapper!", WIDTH / 2, HEIGHT / 2,
                         arcade.color.BLACK, font_size=50, anchor_x="center")
        arcade.draw_text("Click to advance", WIDTH / 2, HEIGHT / 2 - 75,
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
        arcade.draw_text("Click to advance", WIDTH / 2, HEIGHT / 2 - 75,
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

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        # Transition back to the game view
        game_view = Tapper()
        game_view.round = self.round_number + 1  # Increment the round
        game_view.reset_round()  # Reset for the next round
        #after round 2 bring up rat round
        if game_view.round == 3 or game_view.round == 5:
            rat_game = RatGame(game_view.score,self.round_number)
            rat_game.setup()
            self.window.show_view(rat_game)
        else:
            self.window.show_view(game_view)
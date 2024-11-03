import arcade
import random
# from tester import RootBeerTapper

# variables for MenuView
width = 800
height = 600
# SPRITE_SCALING = 0.5
beer_speed = 7
person_speed = 2
bars = 4

class MenuView(arcade.View):
    def on_show_view(self):
        arcade.set_background_color(arcade.color.WHITE)
    # def on_show(self):
    #     arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        self.clear()
        arcade.draw_text("Tapper!", width / 2, height / 2,
                         arcade.color.BLACK, font_size=50, anchor_x="center")
        arcade.draw_text("Click to advance", width / 2, height / 2 - 75,
                         arcade.color.GRAY, font_size=20, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        instructions_view = InstructionView()
        self.window.show_view(instructions_view)


class InstructionView(arcade.View):
    # def on_show(self):
    #     arcade.set_background_color(arcade.color.ORANGE_PEEL)
    def on_show_view(self):
        arcade.set_background_color(arcade.color.ORANGE_PEEL)

    def on_draw(self):
        self.clear()
        arcade.draw_text("Move using the up and down arrows.", width / 2, height / 2 + 15,
                         arcade.color.BLACK, font_size=20, anchor_x="center", multiline=True)
        arcade.draw_text("Use the space bar to serve the drinks", width / 2, height / 2 - 15,
                         arcade.color.BLACK, font_size=20, anchor_x="center", multiline=True)
        arcade.draw_text("Click to advance", width / 2, height / 2 - 75,
                         arcade.color.GRAY, font_size=20, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = RootBeerTapper()
        self.window.show_view(game_view)

class GameOverView(arcade.View):
    def __init__(self, score=0):
        super().__init__()
        self.score = score

    # def on_show(self):
    #     arcade.set_background_color(arcade.color.BLACK)
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

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP and self.current_bar < bars - 1:
            self.current_bar += 1
            self.player_sprite.center_y = self.all_bars_y[self.current_bar]
        elif key == arcade.key.DOWN and self.current_bar > 0:
            self.current_bar -= 1
            self.player_sprite.center_y = self.all_bars_y[self.current_bar]
        if key == arcade.key.SPACE:
            beer = Beer("beer_image.png", 0.3)
            beer.center_x = self.player_sprite.center_x + 50
            beer.center_y = self.player_sprite.center_y
            self.beer_list.append(beer)

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        instructions_view = InstructionView()
        self.window.show_view(instructions_view)

class Beer(arcade.Sprite):
    def __init__(self, image, scaling, view):
        super().__init__(image, scaling)
        self.view = view
    def update(self):
        self.center_x += beer_speed
        if self.right > width:
            self.kill()

# class for the empty glass -johnna
#guys this is so bad i swear it does not work
class Glass(arcade.Sprite):
    def __init__(self, image, scaling, view):
        super().__init__(image, scaling)
        self.view = view
    def update(self):
        self.center_x -= beer_speed
        if self.right  <0:
            game_over_view = GameOverView()
            self.view.window.show_view(game_over_view)

class Customer(arcade.Sprite):
    def __init__(self, view, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.view = view  # Store the reference to the view
        self.drinking = False


    def update(self):
        if not self.drinking:
            self.center_x -= person_speed
            if self.center_x < 100:
                self.drinking = True
                # arcade.schedule(self.throw_glass_back, 0)

    def throw_glass_back(self, delta_time: float):
        if self.drinking:
            glass = Glass("glass_image.png", 0.3, self.view)
            glass.center_x = self.center_x
            glass.center_y = self.center_y
            self.view.beer_list.append(glass)
            self.kill()

    #original code for customer class
    # def update(self):
    #     self.center_x -= person_speed
    #     if self.left < 0:
    #         self.kill()

class RootBeerTapper(arcade.View):
    def __init__(self):
        super().__init__()
        self.player_sprite = None
        self.beer_list = None
        self.customer_list = None
        self.current_bar = 0
        self.all_bars_y = [150, 250, 350, 450]
        self.score = 0

        self.player_sprite = arcade.SpriteSolidColor(50, 50, arcade.color.BROWN)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = self.all_bars_y[self.current_bar]
        self.beer_list = arcade.SpriteList()
        self.customer_list = arcade.SpriteList()
        arcade.schedule(self.add_customer, 2)

    def on_show_view(self):
        arcade.set_background_color(arcade.color_from_hex_string("#454545"))

    def add_customer(self, delta_time: float):
        customer = Customer(self, "customer_image.png", 0.25)  # Pass `self` as the view
        customer.center_x = width - 50
        customer.center_y = random.choice(self.all_bars_y)
        self.customer_list.append(customer)

    def on_draw(self):
        arcade.start_render()

        wall_width = 100  # Thickness of the wall
        wall_color = arcade.color.NAVY_BLUE  # Color of the wall
        tilt_amount = 60  # How much to tilt the inner side

        # right wall
        # bottom right
        x1, y1 = width, 0
        # top right
        x2, y2 = width, height
        # top left
        x3, y3 = width - wall_width, height - 100
        # bottom left
        x4, y4 = width - wall_width + tilt_amount, 0

        # draw the right wall
        arcade.draw_polygon_filled([(x1, y1), (x2, y2), (x3, y3), (x4, y4)], wall_color)
        # back wall
        arcade.draw_rectangle_filled(width//2, height, width*0.75, 200, arcade.color.BLUE)

        # right triangle
        # top left
        x1, y1 = width - wall_width, height
        # top right
        x2, y2 = width, height
        # bottom left
        x3, y3 = width - wall_width, height - 100

        arcade.draw_triangle_filled(x1, y1, x2, y2, x3, y3, arcade.color.NAVY_BLUE)

        perp_rec = 10
        bar_width = width + 10
        bar_height = 30
        rect_width = bar_width // perp_rec
        shadow_height = 4

        bar_start_x = width // 3 - bar_width // 2

        # add background bars
        for y_position in self.all_bars_y:

            # TODO: tilt bar parallel to wall
            arcade.draw_rectangle_filled(width // 3, y_position + 25, bar_width, bar_height,
                                         arcade.color_from_hex_string("#622A0F"))

            arcade.draw_rectangle_filled(width // 3, y_position + 17, bar_width, shadow_height, arcade.color.BLACK)

            arcade.draw_rectangle_filled(width // 3, y_position, bar_width, bar_height, arcade.color_from_hex_string("#923B1B"))

            # perpendicular bars underneath
            for i in range(perp_rec):
                rect_x = bar_start_x + i * rect_width + rect_width // 2
                rect_y = y_position

                # actually draw them
                arcade.draw_rectangle_filled(rect_x, rect_y, rect_width / perp_rec, bar_height, arcade.color_from_hex_string("#53220F"))

        # left wall
        # bottom right
        x1, y1 = wall_width - tilt_amount, 0
        # top right
        x2, y2 = 100, 500
        # top left
        x3, y3 = 0, height
        # bottom left
        x4, y4 = 0, 0

        arcade.draw_polygon_filled([(x1, y1), (x2, y2), (x3, y3), (x4, y4)], arcade.color.NAVY_BLUE)

        # left triangle
        # top left
        x1, y1 = 0, height
        # top right
        x2, y2 = wall_width, height
        # bottom right
        x3, y3 = 100, 500

        arcade.draw_triangle_filled(x1, y1, x2, y2, x3, y3, arcade.color.NAVY_BLUE)

        # budweiser sign
        points = [
            (385, 575),  # top center **
            (500, 600),  # top right
            (500, 500),  # bottom right
            (385, 530),  # bottom center **
            (300, 500),  # bottom left
            (300, 600)  # top left
        ]

        arcade.draw_polygon_filled(points, arcade.color.RED)

        arcade.draw_text("Budweiser", width / 2, height - 55,
                     arcade.color.WHITE, font_size=20, anchor_x="center")

        self.player_sprite.draw()
        self.beer_list.draw()
        self.customer_list.draw()
        arcade.draw_text(f"Score: {self.score}", 10, height - 30, arcade.color.WHITE, 20)

    def on_update(self, delta_time):
        self.beer_list.update()
        self.customer_list.update()
        for beer in self.beer_list:
            customers_hit = arcade.check_for_collision_with_list(beer, self.customer_list)
            for customer in customers_hit:
                beer.kill()
                customer.drinking = True
                print("customer got beer")
                arcade.schedule(customer.throw_glass_back, 2)  # Schedule throwing glass
                self.score += 1
                self.window.total_score += 1
        if self.score == 10:
            game_over_view = GameOverView(self.score)
            self.window.show_view(game_over_view)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP and self.current_bar < bars - 1:
            self.current_bar += 1
            self.player_sprite.center_y = self.all_bars_y[self.current_bar]
        elif key == arcade.key.DOWN and self.current_bar > 0:
            self.current_bar -= 1
            self.player_sprite.center_y = self.all_bars_y[self.current_bar]
        if key == arcade.key.SPACE:
            beer = Beer("beer_image.png", 0.3, self)
            beer.center_x = self.player_sprite.center_x + 50
            beer.center_y = self.player_sprite.center_y
            self.beer_list.append(beer)
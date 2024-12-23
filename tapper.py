import arcade
import random
from beer import Beer
from customer import Customer
from player import Player
import math
from ratCups import RatGame

# I import gameOverView and RoundWinView from view.py below in the code block shortly before I call game over view

# variables for MenuView
WIDTH = 800
HEIGHT = 600
bars = 4
radius = 25


def calc_hexagon(center_x_coord, center_y_coord, radius):
    # def
    vertices = []
    for i in range(6):
        angle = math.radians(60 * i + 45) + 20
        # cos is x axis, sin is y axis
        x = center_x_coord + radius * math.cos(angle)
        y = center_y_coord + radius * math.sin(angle - 10)
        vertices.append((x, y))
    return vertices

class Tapper(arcade.View):
    def __init__(self):
        super().__init__()
        self.round = 1
        self.player_sprite = None
        self.beer_list = None
        self.customer_list = None
        self.rat_view = None

        self.customer_speed = 1  # Default speed for customers
        self.customers_per_bar = 2  # Default number of customers per bar

        self.level_config = {
            1: {"speed": 1.25, "count": 2},  # Slow, 2 customers
            2: {"speed": 1.75, "count": 2},  # Fast, 2 customers
            3: {"speed": 1.25, "count": 3},  # Slow, 3 customers
            4: {"speed": 1.75, "count": 3},  # Fast, 3 customers
            5: {"speed": 1, "count": 4},  # Slow, 4 customers
            6: {"speed": 1.5, "count": 4},  # Fast, 4 customers
        }

        self.current_bar = 0
        self.all_bars_y = [150, 250, 350, 450]
        self.end_x_positions = [WIDTH - 89, WIDTH - 90, WIDTH - 90,
                                WIDTH - 91]  # TODO: change to be more precise to end of bar
        self.start_x_positions = [91, 90, 90, 89]
        self.score = 0

        self.player_sprite = Player("images/Tapper_bartender.png", .75, moving_left=False, moving_right=False,
                                    flipped_horizontally=True)
        self.player_sprite.center_x = WIDTH - 100
        self.player_sprite.center_y = self.all_bars_y[self.current_bar]
        self.beer_list = arcade.SpriteList()
        self.customer_list = arcade.SpriteList()

        self.patron_count = {i: 0 for i in range(len(self.all_bars_y))}  # Track patrons per bar

        self.initial_wave_spawned = False

        # Spawn initial wave of customers
        self.spawn_initial_wave()
        self.initial_wave_spawned = True

        arcade.schedule(self.add_customer, 2)



    def on_show_view(self):
        arcade.set_background_color(arcade.color_from_hex_string("#454545"))

    def update_level_settings(self):
        """Update customer speed and bar limits based on the current round."""
        level_settings = self.level_config.get(self.round, {"speed": 2, "count": 2})
        self.customer_speed = level_settings["speed"]
        self.customers_per_bar = level_settings["count"]
        for customer in self.customer_list:
            customer.speed = self.customer_speed  # Update existing customers

    def spawn_initial_wave(self):
        """Spawns the initial wave of customers for the round."""
        self.update_level_settings()
        for bar_index in range(len(self.all_bars_y)):  # Iterate over each bar
            while self.patron_count[bar_index] < self.customers_per_bar:  # Ensure exact count per bar
                customer = Customer("images/Tapper_cowboy1.png", 1.5, bar_index, self, flipped_horizontally=False)
                # Stagger initial x-positions to avoid overlap
                customer.center_x = 50 + (self.patron_count[bar_index] * 60)
                customer.center_y = self.all_bars_y[bar_index] + 65
                customer.speed = self.customer_speed
                self.customer_list.append(customer)
                self.patron_count[bar_index] += 1

    def add_customer(self, delta_time: float):
        """Adds a customer to the game, respecting the level settings."""
        self.update_level_settings()
        bar_index = random.randint(0, len(self.all_bars_y) - 1)
        if self.patron_count[bar_index] >= self.customers_per_bar:
            return

        customer = Customer("images/Tapper_cowboy1.png", 1.5, bar_index, self, flipped_horizontally=False)
        customer.center_x = 50
        customer.center_y = self.all_bars_y[bar_index] + 65
        customer.speed = self.customer_speed  # Set speed
        self.customer_list.append(customer)
        self.patron_count[bar_index] += 1

    def on_draw(self):
        arcade.start_render()

        wall_width = 100  # Thickness of the wall
        wall_color = arcade.color.NAVY_BLUE  # Color of the wall
        tilt_amount = 60  # How much to tilt the inner side

        # right wall
        # bottom right
        x1, y1 = WIDTH, 0
        # top right
        x2, y2 = WIDTH, HEIGHT
        # top left
        x3, y3 = WIDTH - wall_width, HEIGHT - 100
        # bottom left
        x4, y4 = WIDTH - wall_width + tilt_amount, 0

        # draw the right wall
        arcade.draw_polygon_filled([(x1, y1), (x2, y2), (x3, y3), (x4, y4)], wall_color)
        # back wall
        arcade.draw_rectangle_filled(WIDTH // 2, HEIGHT, WIDTH * 0.75, 200, arcade.color.BLUE)

        # right triangle
        # top left
        x1, y1 = WIDTH - wall_width, HEIGHT
        # top right
        x2, y2 = WIDTH, HEIGHT
        # bottom left
        x3, y3 = WIDTH - wall_width, HEIGHT - 100

        arcade.draw_triangle_filled(x1, y1, x2, y2, x3, y3, arcade.color.NAVY_BLUE)

        perp_rec = 10
        bar_width = WIDTH + 10
        bar_height = 30
        rect_width = bar_width // perp_rec
        shadow_height = 4

        bar_start_x = WIDTH // 3 - bar_width // 2

        # bottom right
        x1, y1 = wall_width - tilt_amount, 0
        # top right
        x2, y2 = 100, 500

        slope = (y2 - y1) / (x2 - x1)

        # add background bars
        for i, y_position in enumerate (self.all_bars_y):

            # TODO: tilt bar parallel to wall
            arcade.draw_rectangle_filled(WIDTH // 3, y_position + 25, bar_width, bar_height,  # was width//3
                                         arcade.color_from_hex_string("#622A0F"))
            arcade.draw_rectangle_filled(WIDTH // 3, y_position + 17, bar_width, shadow_height, arcade.color.BLACK)
            arcade.draw_rectangle_filled(WIDTH // 3, y_position, bar_width, bar_height,
                                         arcade.color_from_hex_string("#923B1B"))

            # perpendicular bars underneath

            for j in range(perp_rec):
                rect_x = bar_start_x + j * rect_width + rect_width // 2
                rect_y = y_position

                # actually draw them
                arcade.draw_rectangle_filled(rect_x, rect_y, rect_width / perp_rec, bar_height,
                                             arcade.color_from_hex_string("#53220F"))

        # left wall
        # bottom right
        x1, y1 = wall_width - tilt_amount, 0
        # top right
        x2, y2 = 100, 500
        # top left
        x3, y3 = 0, HEIGHT
        # bottom left
        x4, y4 = 0, 0

        arcade.draw_polygon_filled([(x1, y1), (x2, y2), (x3, y3), (x4, y4)], arcade.color.NAVY_BLUE)

        # left triangle
        # top left
        x1, y1 = 0, HEIGHT
        # top right
        x2, y2 = wall_width, HEIGHT
        # bottom right
        x3, y3 = 100, 500

        arcade.draw_triangle_filled(x1, y1, x2, y2, x3, y3, arcade.color.NAVY_BLUE)

        # left bar door
        for i, y_position in enumerate(self.all_bars_y):
            adjusted_wall_width = wall_width + slope * (i + 1)
            adjusted_bar_height = bar_height - 5

            rect_y = y_position + 5

            triangle_y = y_position + 20 + bar_height

            # bottom of the door
            arcade.draw_rectangle_filled(adjusted_wall_width - 45, rect_y, 25, adjusted_bar_height,
                                         arcade.color_from_hex_string("#fe6c01"))

            # shadow
            arcade.draw_rectangle_filled(adjusted_wall_width - 45, rect_y, 18, adjusted_bar_height - 6,
                                         arcade.color_from_hex_string("#db4504"))


            # right triangle
            # top left
            x1, y1 = (adjusted_wall_width - 45) - 12.5, rect_y + adjusted_bar_height / 2 + 20
            # bottom right
            x2, y2 = (adjusted_wall_width - 45) + 12.5, rect_y + adjusted_bar_height / 2
            # bottom left
            x3, y3 = (adjusted_wall_width - 45) - 12.5, rect_y + adjusted_bar_height / 2

            arcade.draw_triangle_filled(x1, y1, x2, y2, x3, y3, arcade.color_from_hex_string("#fe6c01"))

            # top left
            x1, y1 = (adjusted_wall_width - 44) - 10.5, rect_y - 6 + adjusted_bar_height / 2 + 20
            # bottom right
            x2, y2 = (adjusted_wall_width - 44) + 5.5, rect_y + 1 + adjusted_bar_height / 2
            # bottom left
            x3, y3 = (adjusted_wall_width - 44) - 10.5, rect_y + 1 + adjusted_bar_height / 2
            arcade.draw_triangle_filled(x1, y1, x2, y2, x3, y3, arcade.color_from_hex_string("#db4504"))

            # left side of the door
            arcade.draw_line(
                # top
                (adjusted_wall_width - 45) - 12.5,
                rect_y + adjusted_bar_height / 2 + 20,

                # bottom
                (adjusted_wall_width - 45) - 12.5,
                rect_y + adjusted_bar_height / 2 - 40,
                arcade.color.GOLD,
                line_width = 2
            )


        # right bar door
        for i, y_position in enumerate(self.all_bars_y):
            adjusted_wall_width = wall_width + slope * (i + 1) - 25
            adjusted_bar_height = bar_height - 15

            rect_y = y_position + 50

            triangle_y = y_position + 20 + bar_height

            # bottom of the door
            arcade.draw_rectangle_filled(adjusted_wall_width, rect_y, 25, adjusted_bar_height,
                                         arcade.color_from_hex_string("#fe6c01"))

            # shadow
            arcade.draw_rectangle_filled(adjusted_wall_width, rect_y, 20, adjusted_bar_height - 6,
                                         arcade.color_from_hex_string("#db4504"))

            # right triangle
            # top left
            x1, y1 = (adjusted_wall_width) - 12.5, rect_y + adjusted_bar_height / 2 + 20
            # bottom right
            x2, y2 = (adjusted_wall_width) + 12.5, rect_y + adjusted_bar_height / 2
            # bottom left
            x3, y3 = (adjusted_wall_width) - 12.5, rect_y + adjusted_bar_height / 2

            arcade.draw_triangle_filled(x1, y1, x2, y2, x3, y3, arcade.color_from_hex_string("#fe6c01"))

            # top left
            x1, y1 = (adjusted_wall_width) - 10.5, rect_y - 6 + adjusted_bar_height / 2 + 20
            # bottom right
            x2, y2 = (adjusted_wall_width) + 8.5, rect_y + 1 + adjusted_bar_height / 2
            # bottom left
            x3, y3 = (adjusted_wall_width) - 10.5, rect_y + 1 + adjusted_bar_height / 2
            arcade.draw_triangle_filled(x1, y1, x2, y2, x3, y3, arcade.color_from_hex_string("#db4504"))

            # connect the top of the doors
            arcade.draw_line(
                # top right
                (adjusted_wall_width) - 12.5,
                rect_y + adjusted_bar_height / 2 + 20,

                # bottom left
                (adjusted_wall_width - 45) + 12.5,
                rect_y + adjusted_bar_height / 2 - 20,
                arcade.color.GOLD,
                line_width = 2
            )

        # budweiser sign
        points = [
            (385, 575),  # top center **
            (500, 600),  # top right
            (500, 500),  # bottom right
            (385, 530),  # bottom center **
            (300, 500),  # bottom left
            (300, 600)  # top left
        ]

        arcade.draw_polygon_filled(points, arcade.color_from_hex_string("#fe6c01"))

        # outline budweiser sign
        points = [
            (385, 572),  # top center **
            (498, 598),  # top right
            (498, 502),  # bottom right
            (385, 532),  # bottom center **
            (302, 502),  # bottom left
            (302, 598)  # top left
        ]

        arcade.draw_polygon_filled(points, arcade.color.RED)

        arcade.draw_text("Budweiser", WIDTH / 2, HEIGHT - 55,
                         arcade.color.WHITE, font_size=20, anchor_x="center", bold=True)

        self.player_sprite.draw()
        self.beer_list.draw()
        self.customer_list.draw()
        arcade.draw_text(f"Score: {self.window.total_score}", 10, HEIGHT - 30, arcade.color.WHITE, 20)

        # lives
        arcade.draw_text(f"Lives: {self.window.lives}", 10, HEIGHT - 60, arcade.color.WHITE, 20)



        # left side of the right wall
        x3, y3 = WIDTH - wall_width, HEIGHT - 100
        x4, y4 = WIDTH - wall_width + tilt_amount, 0

        # calc the slope of the line
        slope = (y4 - y3) / (x4 - x3)

        # space between taps
        keg_spacing = 70
        keg_width = 30
        keg_height = 30
        y_offset = 20

        # draw all 4 taps
        for i, y_position in enumerate(self.all_bars_y[:4]):
            adjusted_y_position = y_position + y_offset
            # find x-coordinate so that its parallel to the left side of the right wall
            keg_x = x3 + (adjusted_y_position - y3) / slope + 30
            hexagon_vertices = calc_hexagon(keg_x, adjusted_y_position, radius)
            small_hexagon_vertices = calc_hexagon(keg_x-5, adjusted_y_position, radius-10)

            # draw the tap, larger
            arcade.draw_polygon_filled(hexagon_vertices, arcade.color_from_hex_string("#982204"))
            arcade.draw_polygon_outline(hexagon_vertices, arcade.color_from_hex_string("#4e2200"), 2)

            # smaller
            arcade.draw_polygon_filled(small_hexagon_vertices, arcade.color_from_hex_string("#722500"))
            arcade.draw_polygon_outline(small_hexagon_vertices, arcade.color_from_hex_string("#d1970f"), 2)

            # extrusion
            arcade.draw_line(
                # right
                keg_x - 5,adjusted_y_position,

                # left
                keg_x - 35,adjusted_y_position,
                arcade.color_from_hex_string("#6c6b70"),
                line_width = 5
            )

            # part where the liquid comes out
            arcade.draw_line(keg_x - 35, adjusted_y_position,
                             keg_x - 35, adjusted_y_position - 10,
                             arcade.color_from_hex_string("#6c6b70"),
                             line_width = 3)

            # handle outline
            arcade.draw_line(keg_x - 35, adjusted_y_position,
                             keg_x - 35, adjusted_y_position + 22,
                             arcade.color.BLACK,
                             line_width=7)

            # handle
            arcade.draw_line(keg_x - 35, adjusted_y_position,
                             keg_x - 35, adjusted_y_position + 20,
                             arcade.color_from_hex_string("#653733"),
                             line_width=5)

    def reset_round(self):
        """Resets the round when a life is lost or a round is won."""
        # Clear existing beer and customer sprites
        self.beer_list = arcade.SpriteList()
        self.customer_list = arcade.SpriteList()

        # Reset patron counts
        self.patron_count = {i: 0 for i in range(len(self.all_bars_y))}

        # Reset player position
        self.player_sprite.center_x = WIDTH - 100
        self.player_sprite.center_y = self.all_bars_y[self.current_bar]

        # Stop and restart customer spawning
        arcade.unschedule(self.add_customer)
        self.initial_wave_spawned = False  # Reset for the new round

        # Spawn initial wave of customers for the next round
        self.spawn_initial_wave()
        self.initial_wave_spawned = True

        # Resume regular customer spawning
        arcade.schedule(self.add_customer, max(1, 2 - self.round * 0.1))

    def on_update(self, delta_time):
        from view import GameOverView, RoundWinView  # to avoid cyclical imports - could not find a way around this

        self.player_sprite.update()
        self.beer_list.update()
        for customer in self.customer_list:
            customer.update()

        #This is for when the customer gets hit by a full beer - initiates push back and drinking feature
        for beer in self.beer_list:
            if beer.get_full() == True:
                customers_hit = arcade.check_for_collision_with_list(beer, self.customer_list)
                for customer in customers_hit:
                    if not customer.get_drinking():
                        beer.kill()
                        customer.hit_customer(
                            self.all_bars_y)  # pushes back customer and then throws glass or kills customer
                        customer.texture = arcade.load_texture("images/tapper_cowboy_drinking_part1.png")


        for beer in self.beer_list:
            # if player catches empty beer as it is sliding back
            if isinstance(beer, Beer) and arcade.check_for_collision(beer, self.player_sprite):
                self.window.total_score += 100
                beer.kill()
                # lives run out = game over
                if self.window.lives <= 0:
                    game_over_view = GameOverView()
                    self.window.show_view(game_over_view)
            # If empty beer reaches end of bar without getting caught
            if beer.right >= WIDTH - 100:
                self.window.lives -= 1
                # reset round
                self.reset_round()
                beer.kill()
                # lives run out = game over
                if self.window.lives <= 0:
                    game_over_view = GameOverView()
                    self.window.show_view(game_over_view)
            # if full beer reaches end door without hitting customer
            if beer.right <= 90:
                self.window.lives -= 1
                # reset round
                self.reset_round()
                beer.kill()
                # lives run out = game over
                if self.window.lives <= 0:
                    game_over_view = GameOverView()
                    self.window.show_view(game_over_view)
        # check all customers to make sure they do not get to end of bar before being served
        for customer in self.customer_list:
            bar_end_x = self.end_x_positions[customer.bar_index]
            bar_start_x = self.start_x_positions[customer.bar_index]
            if customer.center_x >= bar_end_x:
                customer.kill()
                self.window.lives -= 1
                # reset round
                self.reset_round()
                # lives run out = game over
                if self.window.lives <= 0:
                    game_over_view = GameOverView()
                    self.window.show_view(game_over_view)
            # checks whether customer hit back wall and kills it if it gets pushed back enough
            if customer.get_drinking() and customer.center_x <= bar_start_x:
                customer.kill()

        # Check if all customers are gone and win the round
        if len(self.customer_list) == 0:
            round_win_view = RoundWinView(self.round)  # Pass the current round number
            self.window.total_score += 1000
            if self.round == 6:
                game_over_view = GameOverView()
                self.window.show_view(game_over_view)
            else:
                self.window.show_view(round_win_view)


    def on_key_press(self, key, modifiers):
        # Move up and down between bars including cyclical movement
        if key == arcade.key.UP and self.current_bar < bars - 1:
            self.current_bar += 1
            self.player_sprite.center_y = self.all_bars_y[self.current_bar]
            self.player_sprite.center_x = WIDTH - 100
        elif key == arcade.key.DOWN and self.current_bar > 0:
            self.current_bar -= 1
            self.player_sprite.center_y = self.all_bars_y[self.current_bar]
            self.player_sprite.center_x = WIDTH - 100
        elif key == arcade.key.DOWN and self.current_bar == 0:
            self.current_bar = 3
            self.player_sprite.center_y = self.all_bars_y[self.current_bar]
            self.player_sprite.center_x = WIDTH - 100
        elif key == arcade.key.UP and self.current_bar == 3:  # and top to bottom
            self.current_bar = 0
            self.player_sprite.center_y = self.all_bars_y[self.current_bar]
            self.player_sprite.center_x = WIDTH - 100

        # Move left and right down bars
        if key == arcade.key.LEFT:
            self.player_sprite.set_moving_left(True)
        elif key == arcade.key.RIGHT:
            self.player_sprite.set_moving_right(True)

        # Launch beers on press
        if key == arcade.key.SPACE:
            # set player back to keg side of bar
            self.player_sprite.center_x = WIDTH - 100

            beer = Beer("images/Tapper_mug_full.png", .55, True)
            beer.center_x = self.player_sprite.center_x - 50
            beer.center_y = self.player_sprite.center_y + 50  # places beers right on top of bars

            self.beer_list.append(beer)

    def on_key_release(self, key, modifiers):
        # release means stop movement - horizontal
        if key == arcade.key.LEFT:
            self.player_sprite.set_moving_left(False)
        elif key == arcade.key.RIGHT:
            self.player_sprite.set_moving_right(False)

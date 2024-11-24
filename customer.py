import arcade
from beer import Beer
import time

WIDTH = 800
HEIGHT = 600
person_speed = 2


class Customer(arcade.Sprite):
    def __init__(self, image, scale, bar_index, game_view, *args, **kwargs):
        super().__init__(image, scale, *args, **kwargs)
        self.bar_index = bar_index
        self.game_view = game_view
        self.drinking = False
        self.drink_timer = 0
        self.all_bars_y = None
        self.distance_moved = 0

        self.target_x = None

    def hit_customer(self, all_bars_y):
        """Push the customer back slightly on the bar or make them drink."""
        push_back_distance = 299  # Adjust this value for the amount they move back
        door_x = self.game_view.start_x_positions[self.bar_index]

        # Calculate new position
        new_x = self.center_x - push_back_distance

        if new_x <= door_x:
            # Set target to door for smooth sliding
            self.target_x = door_x
        else:
            self.target_x = new_x

    def start_drinking(self):
        """Start the drinking animation or pause."""
        self.drinking = True
        self.drink_timer = 60  # Adjust this duration (e.g., 60 = 1 second at 60 FPS)

    def update(self):
        """Update the customer state."""
        if self.target_x is not None:
            # Move gradually toward the target position
            if self.center_x > self.target_x:
                self.center_x -= person_speed * 3  # Adjust speed for smooth movement
            else:
                # Reached target position
                if self.target_x == self.game_view.start_x_positions[self.bar_index]:
                    # If the target was the door, remove the customer
                    self.kill()
                    self.game_view.window.total_score += 50
                # Reached target position
                self.target_x = None
                # If not at the door, start drinking
                if not self.drinking:
                    self.start_drinking()
            return  # Do nothing else while moving to the target

        if self.drinking:
            self.texture = arcade.load_texture("images/tapper_cowboy_drinking_part2.png")
            # Handle drinking
            self.drink_timer -= 1
            if self.drink_timer <= 0:
                self.drinking = False  # Resume movement after drinking
                self.throw_empty_beer_glass()
                self.texture = arcade.load_texture("images/tapper_cowboy1.png")
            return  # Do nothing else while drinking

        # Normal forward movement when not drinking or moving backward
        self.center_x += person_speed

        if self.right > WIDTH:  # Remove customer if they go off-screen
            self.kill()

    def throw_empty_beer_glass(self):
        """Create and throw an empty beer glass."""
        empty_glass = Beer("images/Tapper_mug_empty.png", 0.55, False)
        empty_glass.center_x = self.center_x
        empty_glass.center_y = self.game_view.all_bars_y[self.bar_index] + 50
        self.game_view.beer_list.append(empty_glass)

    def get_drinking(self):
        """Return whether the customer is drinking."""
        return self.drinking

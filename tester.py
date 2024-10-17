import arcade
import random


width = 800
height = 600
title = "tapper"
beer_speed = 7
person_speed = 2
bars = 4

class Beer(arcade.Sprite):
    def update(self):
        self.center_x += beer_speed
        if self.right > width:
            self.kill()


class Customer(arcade.Sprite):
    def update(self):
        self.center_x -= person_speed
        if self.left < 0:
            self.kill()

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
        arcade.set_background_color(arcade.color.BLACK)


    def add_customer(self, delta_time: float):
        customer = Customer("customer_image.png", 0.5)
        customer.center_x = width - 50
        customer.center_y = random.choice(self.all_bars_y)
        self.customer_list.append(customer)

    def on_draw(self):
        arcade.start_render()
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
                customer.kill()
                self.score += 1
                self.window.total_score += 1
        from start_and_end_screen import GameOverView   ##hella jenky idk if you can even do this but i was getting circular import errors otherwise
        #I think its a bigger issue with the code structure but we can fix it later, this will be good to turn in for now
        if self.score == 3:
            game_over_view = GameOverView()
            self.window.show_view(game_over_view)



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





if __name__ == "__main__":
    main()
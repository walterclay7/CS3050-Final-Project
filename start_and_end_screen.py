import arcade
from view import MenuView

WIDTH = 800
HEIGHT = 600


def main():
    window = arcade.Window(WIDTH, HEIGHT, "Tapper")
    window.total_score = 0
    menu_view = MenuView()
    x = window.show_view(menu_view)
    arcade.run()


if __name__ == "__main__":
    main()

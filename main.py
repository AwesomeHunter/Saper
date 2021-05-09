from app import App

if __name__ == "__main__":
    game_size = 18, 14
    bombs_count = 10
    game = App(game_size, bombs_count)
    game.run()

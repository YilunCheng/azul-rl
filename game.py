import random

COLORS = ["blue", "yellow", "red", "black", "white"]
COUNT = 20
    
class Bag:
    def __init__(self):
        self.tiles = COLORS * COUNT
        self.discard_tiles = []

    def add_tiles(self, tiles):
        self.tiles.extend(tiles)

    def draw_tile(self):
        if len(self.tiles) == 0:
            if len(self.discard_tiles) == 0:
                return None
            else:
                self.refill_bag()
        
        random_index = random.randint(0, len(self.tiles) - 1)
        drawn_tile = self.tiles.pop(random_index)
        return drawn_tile
    
    def refill_bag(self):
        self.tiles.extend(self.discard_tiles)
        self.discard_tiles = []

class Factory:
    def __init__(self):
        self.tiles = []

    def add_tile(self, tile):
        self.tiles.append(tile)

    def remove_tile(self, tile):
        self.tiles.remove(tile)

class CenterDisplay(Factory):
    def __init__(self):
        self.tiles = []
        self.first_player_token = True

class PlayerBoard:
    def __init__(self, player_name):
        self.player_name = player_name
        self.pattern_lines = {color: [] for color in COLORS}
        self.wall = {color: [] for color in COLORS}
        self.floor_line = []

class Game:
    def __init__(self, num_players):
        self.players = [PlayerBoard(f"Player {i + 1}") for i in range(num_players)]
        self.bag = Bag()
        self.factories = [Factory() for _ in range(num_players * 2 + 1)]
        self.center_display = Factory()
        self.first_player_token = 1
        self.current_player = 0
    
    def initialize_factories(self):
        for _ in range(4):
            for factory in self.factories:
                drawn_tile = self.bag.draw_tile()
                if drawn_tile:
                    factory.add_tile(drawn_tile)
    
    def display_factories(self):
        for factory in self.factories:
            print(factory.tiles)
        print(self.center_display.tiles)
            


# class PlayerBoard:
#     def __init__(self, player_name):
#         self.player_name = player_name
#         self.pattern_lines = {color: [] for color in COLORS}
#         self.wall = {color: [] for color in COLORS}
#         self.floor_line = []

#     def place_tile_in_pattern_line(self, color, tile):
#         # Implement logic to place a tile in the pattern line

#     def place_tile_in_wall(self, color, row, tile):
#         # Implement logic to place a tile in the wall

#     def place_tile_in_floor_line(self, tile):
#         # Implement logic to place a tile in the floor line

#     def score_board(self):
#         # Implement scoring logic for the player's board

# class Game:
#     def __init__(self, num_players):
#         self.players = [PlayerBoard(f"Player {i + 1}") for i in range(num_players)]
#         self.factories = [Factory() for _ in range(5)]
#         self.center_display = Factory()
#         self.current_player = 0

#     def initialize_factories(self):
#         for factory in self.factories:
#             factory.tiles = [Tile(random.choice(COLORS)) for _ in range(4)]

#     def display_factories(self):
#         for i, factory in enumerate(self.factories):
#             print(f"Factory {i + 1}: {[tile.color for tile in factory.tiles]}")

#     def take_tiles_from_factory(self, factory_index, color):
#         # Implement logic to take tiles from a factory

#     def end_round(self):
#         # Implement end-of-round logic

#     def play_game(self):
#         while not self.game_over():
#             self.display_factories()
#             current_player = self.players[self.current_player]
#             # Implement player's turn logic
#             # - Select tiles from factories
#             # - Place tiles on player board
#             # - Score points
#             # - Handle end-of-round conditions
#             self.current_player = (self.current_player + 1) % len(self.players)

#     def game_over(self):
#         # Implement the game-over condition
#         return True

#     def determine_winner(self):
#         # Implement logic to determine the winner
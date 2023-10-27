import random
from players import *

COLORS = ["blue", "yellow", "red", "black", "white"]
COUNT = 20

class Bag:
    def __init__(self):
        self.tiles = COLORS * COUNT
        self.discard_tiles = []

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

    def add_tiles(self, tiles_list):
        self.tiles.extend(tiles_list)

    def remove_tiles_by_color(self, color):
        self.tiles = [tile for tile in self.tiles if tile != color]
        
    def is_empty(self):
        if len(self.tiles) == 0:
            return True
        else:
            return False
    

class Game:
    def __init__(self, players):
        self.num_players = len(players)
        self.players = players
        
        self.bag = Bag()
        self.factory_count = self.num_players * 2 + 1
        self.factories = [Factory() for _ in range(self.factory_count)]
        self.center_display = Factory()
        
        self.first_player_token = True
        self.current_player = 0

    def next_player(self):
        if self.current_player == (self.num_players - 1):
            self.current_player = 0
        else:
            self.current_player += 1
       
    def display_factories(self):
        print("Current factories:")
        for factory in self.factories:
            print(sorted(factory.tiles))
        print("Current Center:")
        print(sorted(self.center_display.tiles))
        
    def display_player_score(self):
        for player_index in range(self.num_players):
            self.players[player_index].display_score()
        
    def num_remaining_tiles_in_factory(self):
        return sum([len(factory.tiles) for factory in self.factories]) + len(self.center_display.tiles)
    
    def game_end(self):
        for player_index in range(self.num_players):
            for j in range(5):
                if None not in [x[j] for x in self.players[player_index].wall]:
                    return True
        return False
                
    def calculate_place_to_wall_score(self, i, j, wall):
        return 1
    
    def calculate_game_end_score(self):
        return 1
    
    def initialize_factories(self, random=True):
        if random:
            for _ in range(4):
                for factory in self.factories:
                    drawn_tile = self.bag.draw_tile()
                    if drawn_tile:
                        factory.add_tiles([drawn_tile]) 
        
    def take_tiles_from_factory(self, factory_index, color):
        factory_index -= 1
        
        # Check if the factory index is valid
        if factory_index < 0 or factory_index > self.factory_count:
            raise Exception("Invalid factory index.")
                   
        if factory_index == self.factory_count:
            selected_factory = self.center_display
        else:
            selected_factory = self.factories[factory_index]

        # Check if the selected factory is empty
        if not selected_factory.tiles:
            raise Exception("Selected factory is empty.")

        selected_tiles = [tile for tile in selected_factory.tiles if tile == color]

        # Check if there are tiles of the selected color in the factory
        if not selected_tiles:
            raise Exception(f"No {color} tiles in the selected factory.")
        
        if factory_index == self.factory_count:
            self.center_display.remove_tiles_by_color(color)
            if self.first_player_token:
                self.first_player_token = False
                selected_tiles.append("1")
        else:
            unselected_tiles = [tile for tile in selected_factory.tiles if tile != color]
            self.factories[factory_index].tiles = []
            self.center_display.add_tiles(unselected_tiles)
            
        return selected_tiles
    
    def place_tiles_in_pattern_line(self, line_index, tiles):
        line_index -= 1
        
        if line_index not in [0, 1, 2, 3, 4, 5]:
            raise Exception("Invalid line index.")
    
        if line_index == 5:
            self.players[self.current_player].floor_line.extend(tiles)
            
        else:
            selected_line = self.players[self.current_player].pattern_lines[line_index]
            selected_wall = self.players[self.current_player].wall[line_index]
            if tiles[0] in selected_wall:
                raise Exception(f"{tiles[0]} has been filled in wall for line {line_index}")
                
            if len(selected_line) == (line_index+1):
                raise Exception(f"Selected line {line_index} is full.")
            
            if (len(selected_line) > 0) and (selected_line[0] != tiles[0]):
                Exception("Selected line has unmatched color.")
            
            if "1" in tiles:
                self.players[self.current_player].floor_line.append("1")
                tiles.pop()
                
            result_line = selected_line + tiles
            self.players[self.current_player].pattern_lines[line_index] = result_line[0:line_index+1]
            self.players[self.current_player].floor_line.extend(result_line[line_index+1:])
           
    def place_tile_in_wall_and_score(self, verbose=True):
        for player_index in range(self.num_players):
            if verbose:
                print(f"Calculate score for {self.players[player_index].player_name}.")
            for i in range(5):
                if len(self.players[player_index].pattern_lines[i]) == (i+1):
                    color = self.players[player_index].pattern_lines[i][0]
                    j = (COLORS.index(color) + i) % 5
                    self.players[player_index].wall[i][j] = color
                    score = self.calculate_place_to_wall_score(i, j, self.players[player_index].wall)
                    self.players[player_index].pattern_lines[i] = []
                    self.players[player_index].score += score
                    if verbose:
                        print(f"Line {i+1} is full with {color} tiles. Get {score} score.")
            if verbose:
                self.players[player_index].display_board()
                self.players[player_index].display_wall()
                print("\n\n")
                
    def prepare_next_round(self, verbose=True):
        if verbose:
            print("-----------------------------------------------------------")
            print("ROUND START")
        for player_index in range(self.num_players):
            if "1" in self.players[player_index].floor_line:
                self.current_player = player_index
            self.players[player_index].floor_line = []
        self.initialize_factories()
        if verbose:
            self.display_player_score()
            self.display_factories()
            print("-----------------------------------------------------------\n\n")
    
    def play(self, verbose=True):
        while not self.game_end():
            self.prepare_next_round(verbose=verbose)
            while self.num_remaining_tiles_in_factory():
                if verbose:
                    print(f"{self.players[self.current_player].player_name}'s turn:")
                while True:
                    try:
                        factory_index, color, line_index = self.players[self.current_player].choose_action(self)
                        factory_index = int(factory_index)
                        tiles = self.take_tiles_from_factory(factory_index, color)
                        break
                    except Exception as e:
                        print(e)
                while True:
                    try:
                        line_index = int(line_index)
                        self.place_tiles_in_pattern_line(line_index, tiles)
                        break
                    except Exception as e:
                        print(e)
                        line_index = int(input("Reselect line index: "))

                if verbose:
                    print(f"{self.players[self.current_player].player_name} takes {len(tiles)} {tiles[0]} tiles from factory {factory_index}.")
                    print(f"{self.players[self.current_player].player_name} places {len(tiles)} {tiles[0]} tiles to line {line_index}.")
                    self.players[self.current_player].display_board()
                    self.display_factories()
                    print("\n")

                self.next_player()
            
            self.place_tile_in_wall_and_score(verbose=verbose)
        self.calculate_game_end_score()
import random

class Player:
    def __init__(self, player_name):
        self.player_name = player_name
        self.pattern_lines = [[],[],[],[],[]]
        self.wall = [[None]*5,[None]*5,[None]*5,[None]*5,[None]*5]
        self.floor_line = []
        self.score = 0
            
    def display_score(self):
        print(f"{self.player_name}'s Score: {self.score}")

    def display_board(self):
        print(f"{self.player_name}'s Board:")
        for i in range(5):
            print(self.pattern_lines[i])
        print(f"Floor line:")
        print(self.floor_line)
        
    def display_wall(self):
        print(f"{self.player_name}'s Wall:")
        for i in range(5):
            print(self.wall[i])

        
class RandomPlayer(Player):
    def __init__(self, name):
        super().__init__(name)

    def choose_action(self, game): 
        factory_index_with_tiles = []
        for i in range(game.factory_count):
            if not game.factories[i].is_empty():
                factory_index_with_tiles.append(i)
        if not game.center_display.is_empty():
            factory_index_with_tiles.append(game.factory_count)
        factory_index = random.choice(factory_index_with_tiles)
        
        if factory_index == game.factory_count:
            color = random.choice(game.center_display.tiles)
        else:
            color = random.choice(game.factories[factory_index].tiles)
            
        valid_line_index = []
        for i in range(5):
            if color in self.wall[i]:
                continue
            if len(self.pattern_lines[i]) == 0:
                valid_line_index.append(i)
            elif (self.pattern_lines[i][0] == color) and (len(self.pattern_lines[i]) != (i+1)):
                valid_line_index.append(i)
        if valid_line_index:
            line_index = random.choice(valid_line_index)
        else:
            line_index = 5
            
        return factory_index + 1, color, line_index + 1


class HumanPlayer(Player):
    def __init__(self, name):
        super().__init__(name)

    def choose_action(self, game):
        factory_index = input("Factory index: ")
        color = input("Color: ")       
        line_index = input("Line index: ")
        
        return factory_index, color, line_index
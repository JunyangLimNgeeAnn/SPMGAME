import random
import json
from datetime import datetime


def get_adjacent_positions(row, col, rows=20, cols=20):
    """Get a list of adjacent positions for a given cell in the grid."""
    adjacent_positions = []
    for r, c in [(row-1, col), (row+1, col), (row, col-1), (row, col+1)]:
        if 0 <= r < rows and 0 <= c < cols:
            adjacent_positions.append((r, c))
    return adjacent_positions

def calculate_score_and_coins(grid):
    """Calculate the score and coins based on the grid's current state."""
    rows, cols = len(grid), len(grid[0])
    score = 0
    coins = 0

    for row in range(rows):
        for col in range(cols):
            building = grid[row][col]
            if building == 'P':
                continue

            adjacent_positions = get_adjacent_positions(row, col)
            adjacent_buildings = [grid[r][c] for r, c in adjacent_positions]

            if building == 'R':
                if 'I' in adjacent_buildings:
                    score += 1
                else:
                    score += 1  # Count only 1 point for each 'R' placed next to 'R', 'C', or 'O'
            elif building == 'I':
                score += adjacent_buildings.count('I')
                coins += sum(1 for r, c in adjacent_positions if grid[r][c] == 'R')
            elif building == 'C':
                score += adjacent_buildings.count('C')
            elif building == 'O':
                if 'O' in adjacent_buildings:
                    score += 1
            elif building == '*':
                if '*' in adjacent_buildings:
                    score += 1

    return score, coins

def calculate_additional_coins(grid, new_building, row, col):
    """Calculate additional coins based on the placement of a new building."""
    coins = 0
    if new_building == 'C':
        adjacent_positions = get_adjacent_positions(row, col)
        coins += sum(1 for r, c in adjacent_positions if grid[r][c] == 'R')
    return coins


def choose_building_freeplay(grid):
    """Randomly select two buildings and allow the user to choose one."""
    buildings = ["R", "I", "C", "*", "O"]
    randombuildings = random.sample(buildings, 2)
    print("Randomly selected buildings:", randombuildings)

    ansbuilding = input("Choose which building to build: ").strip().upper()

    if ansbuilding in randombuildings:
        print(f"{ansbuilding} is in the randomly selected buildings.")
        while True:
            try:
                row = int(input(f"Enter the row number (0-{len(grid)-1}) to place {ansbuilding}: "))
                col = int(input(f"Enter the column number (0-{len(grid[0]) - 1}) to place {ansbuilding}: "))

                if 0 <= row < len(grid) and 0 <= col < len(grid[0]):
                    if grid[row][col] == 'P':
                        return ansbuilding, row, col
                    else:
                        print("Invalid position. The spot is taken.")
                else:
                    print("Invalid position. Please enter valid row and column numbers.")
            except ValueError:
                print("Invalid input. Please enter numeric values.")
    else:
        print(f"{ansbuilding} is not in the randomly selected buildings.")
        return None, None, None


def calculate_score_free_play(grid):
    """Calculate the score based on the grid's current state in Free Play mode."""
    rows, cols = len(grid), len(grid[0])
    score = 0

    for row in range(rows):
        for col in range(cols):
            building = grid[row][col]
            if building == 'P':
                continue

            adjacent_positions = get_adjacent_positions(row, col, rows, cols)
            adjacent_buildings = [grid[r][c] for r, c in adjacent_positions]

            if building == 'R':
                if 'I' in adjacent_buildings:
                    score += 1
                else:
                    score += 1  # Count only 1 point for each 'R' placed next to 'R', 'C', or 'O'
            elif building == 'I':
                score += adjacent_buildings.count('I')
            elif building == 'C':
                score += adjacent_buildings.count('C')
            elif building == 'O':
                if 'O' in adjacent_buildings:
                    score += 1
            elif building == '*':
                if '*' in adjacent_buildings:
                    score += 1

    return score


def choose_building(grid, first_building):
    """Randomly select two buildings and allow the user to choose one."""
    buildings = ["R", "I", "C", "*", "O"]
    randombuildings = random.sample(buildings, 2)
    print("Randomly selected buildings:", randombuildings)

    ansbuilding = input("Choose which building to build: ").strip().upper()

    if ansbuilding in randombuildings:
        print(f"{ansbuilding} is in the randomly selected buildings.")
        while True:
            try:
                row = int(input(f"Enter the row number (0-19) to place {ansbuilding}: "))
                col = int(input(f"Enter the column number (0-19) to place {ansbuilding}: "))

                if 0 <= row < 20 and 0 <= col < 20:
                    if first_building or (grid[row][col] == 'P' and any(grid[r][c] != 'P' for r, c in get_adjacent_positions(row, col))):
                        return ansbuilding, row, col
                    else:
                        print("Invalid position. The spot is either taken or not adjacent to an existing building.")
                else:
                    print("Invalid position. Please enter valid row and column numbers.")
            except ValueError:
                print("Invalid input. Please enter numeric values.")
    else:
        print(f"{ansbuilding} is not in the randomly selected buildings.")
        return None, None, None

def save_game(grid, coins, score, filename='game_save.json'):
    """Save the current game state to a file."""
    game_state = {
        'grid': grid,
        'coins': coins,
        'score': score
    }
    with open(filename, 'w') as f:
        json.dump(game_state, f)
    print("Game progress saved.")

def load_game(filename='game_save.json'):
    """Load the game state from a file."""
    try:
        with open(filename, 'r') as f:
            game_state = json.load(f)
        print("Game progress loaded.")
        return game_state['grid'], game_state['coins'], game_state['score']
    except FileNotFoundError:
        print("No saved game found. Starting a new game.")
        return None, None, None

def save_high_score(score, filename='high_scores.json'):
    """Save the new high score to the high score file with the current date and time."""
    try:
        with open(filename, 'r') as f:
            high_scores = json.load(f)
    except FileNotFoundError:
        high_scores = []

    # Get the current date and time
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Append the new score with the current date and time
    high_scores.append({'score': score, 'date': current_datetime})
    
    # Keep top 10 scores, sorted by score in descending order
    high_scores = sorted(high_scores, key=lambda x: x['score'], reverse=True)[:10]

    with open(filename, 'w') as f:
        json.dump(high_scores, f)
        
    print("High score saved.")

def load_high_scores(filename='high_scores.json'):
    try:
            with open(filename, 'r') as f:
                return json.load(f)
    except json.JSONDecodeError:
            # Handle the case where the file is empty or invalid
            print(f"Warning: {filename} is empty or contains invalid JSON. Returning empty high scores.")
            return []
    else:
        # If the file doesn't exist, return an empty list
        print(f"Warning: {filename} does not exist. Returning empty high scores.")
        return []

def display_high_scores():
    """Display the high scores."""
    high_scores = load_high_scores()
    if high_scores:
        print("High Scores:")
        for idx, score in enumerate(high_scores, 1):
            print(f"{idx}. {score}")
    else:
        print("No high scores yet.")

def arcade_mode():
    """Main game loop for placing buildings on the grid."""
    rows, cols = 20, 20

    # Ask the user if they want to load the previous game
    load_prev_game = input("Do you want to load the previous game? (y/n): ").strip().lower() == 'y'
    if load_prev_game:
        grid, coins, score = load_game()
        if grid is None:  # No saved game found
            grid = [['P' for _ in range(cols)] for _ in range(rows)]
            coins = 16
            score = 0
    else:
        grid = [['P' for _ in range(cols)] for _ in range(rows)]
        coins = 16
        score = 0

    def print_grid(grid):
        for row in grid:
            print(' '.join(row))

    print("Initial grid:")
    print_grid(grid)
    print(f"Initial coins: {coins}")

    # Determine if this is the first building
    first_building = all(cell == 'P' for row in grid for cell in row)

    while coins > 0:
        ansbuilding, row, col = choose_building(grid, first_building)
        if ansbuilding is None:
            continue

        grid[row][col] = ansbuilding
        coins -= 1
        first_building = False  # After the first building is placed

        score, generated_coins = calculate_score_and_coins(grid)
        coins += generated_coins

        print("Updated grid:")
        print_grid(grid)
        print(f"Remaining coins: {coins}")
        print(f"Current score: {score}")

        if coins <= 0:
            save_high_score(score, filename='high_scores.json')
            print("No more coins left. Exiting the game.")
            choose()
            break

        # Ask if the user wants to save the game progress
        if input("Do you want to save the game progress? (y/n): ").strip().lower() == 'y':
            save_game(grid, coins, score)
            choose()
        


    # Save the final score as a high

def expand_grid(grid, expansion_size=5):
    """Expand the grid by adding expansion_size rows and columns to the perimeter."""
    rows, cols = len(grid), len(grid[0])
    new_size = rows + 2 * expansion_size
    new_grid = [['P' for _ in range(new_size)] for _ in range(new_size)]

    for r in range(rows):
        for c in range(cols):
            new_grid[r + expansion_size][c + expansion_size] = grid[r][c]
    
    return new_grid


def choose_building(grid, first_building, free_play=False):
    """Randomly select two buildings and allow the user to choose one."""
    buildings = ["R", "I", "C", "*", "O"]
    randombuildings = random.sample(buildings, 2)
    print("Randomly selected buildings:", randombuildings)

    ansbuilding = input("Choose which building to build: ").strip().upper()

    if ansbuilding in randombuildings:
        print(f"{ansbuilding} is in the randomly selected buildings.")
        while True:
            try:
                row = int(input(f"Enter the row number (0-{len(grid)-1}) to place {ansbuilding}: "))
                col = int(input(f"Enter the column number (0-{len(grid[0]) - 1}) to place {ansbuilding}: "))

                if 0 <= row < len(grid) and 0 <= col < len(grid[0]):
                    if free_play or first_building or (grid[row][col] == 'P' and any(grid[r][c] != 'P' for r, c in get_adjacent_positions(row, col, len(grid), len(grid[0])))):
                        return ansbuilding, row, col
                    else:
                        print("Invalid position. The spot is either taken or not adjacent to an existing building.")
                else:
                    print("Invalid position. Please enter valid row and column numbers.")
            except ValueError:
                print("Invalid input. Please enter numeric values.")
    else:
        print(f"{ansbuilding} is not in the randomly selected buildings.")
        return None, None, None


def save_game_free_play(grid, coins, score, filename='game_save_free_play.json'):
    """Save the current Free Play game state to a file."""
    game_state = {
        'grid': grid,
        'coins': coins,
        'score': score
        # Add more attributes as needed, e.g., grid size
    }
    with open(filename, 'w') as f:
        json.dump(game_state, f)
    print("Free Play game progress saved.")


def load_game_free_play(filename='game_save_free_play.json'):
    """Load the Free Play game state from a file."""
    try:
        with open(filename, 'r') as f:
            game_state = json.load(f)
        print("Free Play game progress loaded.")
        return game_state['grid'], game_state['coins'], game_state['score']
    except FileNotFoundError:
        print("No saved Free Play game found. Starting a new game.")
        return None, None, None

def load_freeplaygame(filename='game_save.json', free_play=False):
    """Load the game state from a file."""
    try:
        with open(filename, 'r') as f:
            game_state = json.load(f)
        print("Game progress loaded.")

        if free_play:
            # Ensure the loaded game state matches Free Play mode requirements
            grid = game_state.get('grid', None)
            coins = game_state.get('coins', None)
            score = game_state.get('score', None)
            
            # Validate the loaded game state for Free Play mode
            if grid is None or coins is None or score is None:
                print("Invalid saved game state for Free Play mode. Starting a new game.")
                return None, None, None
            else:
                return grid, coins, score
        else:
            # For other modes, just return the loaded game state
            return game_state['grid'], game_state['coins'], game_state['score']
    
    except FileNotFoundError:
        print("No saved game found. Starting a new game.")
        return None, None, None



def free_play_mode():
    """Main game loop for Free Play mode with unlimited coins and grid expansion."""
    load_prev_game = input("Do you want to load the previous game? (y/n): ").strip().lower() == 'y'
    if load_prev_game:
        grid, coins, score = load_freeplaygame()
        if grid is None:  # No saved game found or invalid
            grid = [['P' for _ in range(cols)] for _ in range(rows)]
            coins = float('inf')  # Reset coins for new game
            score = 0



    rows, cols = 5, 5
    grid = [['P' for _ in range(cols)] for _ in range(rows)]
    coins = 999999999999999999  # Unlimited coins
    score = 0

    def print_grid(grid):
        for row in grid:
            print(' '.join(row))

    print("Initial grid:")
    print_grid(grid)

    first_building = True

    while True:
        ansbuilding, row, col = choose_building(grid, first_building, free_play=True)
        if ansbuilding is None:
            continue

        grid[row][col] = ansbuilding
        first_building = False
        score = calculate_score_free_play(grid)
        
        print("Updated grid:")
        print_grid(grid)
        print(f"Current score: {score}")

        if row in [0, len(grid) - 1] or col in [0, len(grid[0]) - 1]:
            grid = expand_grid(grid)
            print("Grid expanded:")
            print_grid(grid)

        if input("Do you want to save the game progress? (y/n): ").strip().lower() == 'y':
            save_game_free_play(grid, coins, score)
            choose()



        
        






   

def choose():
    print("Ngee Ann City")
    print("1.) Arcade Mode")
    print("2.) FreePlay Mode")
    print("3.) LeaderBoard")
    ans = int(input("Choose option:"))
    if ans == 1:
      print("You entered Arcade Mode.")
      arcade_mode()
    elif ans == 2:
      print("You entered FreePlay Mode.")
      free_play_mode()
      
    elif ans == 3:
      print("You entered LeaderBoard.")
      display_high_scores()
      if input("Do you want to go back mainpage? (y/n): ").strip().lower() == 'y':
          choose()
      else:
          print('Game will exit')
    else:
      print("You entered a number other than 1, 2, or 3.")
      print("Try again")
      choose()




choose()




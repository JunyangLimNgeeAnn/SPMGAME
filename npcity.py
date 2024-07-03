import random

def get_adjacent_positions(row, col, rows=20, cols=20):
    """Get a list of adjacent positions for a given cell in the grid."""
    adjacent_positions = []
    for r, c in [(row-1, col), (row+1, col), (row, col-1), (row, col+1)]:
        if 0 <= r < rows and 0 <= c < cols:
            adjacent_positions.append((r, c))
    return adjacent_positions

def calculate_score_and_coins(grid):
    rows, cols = len(grid), len(grid[0])
    score = 0
    coins = 0
    industry_count = sum(row.count('I') for row in grid)

    for row in range(rows):
        for col in range(cols):
            building = grid[row][col]
            if building == 'P':
                continue

            adjacent_positions = get_adjacent_positions(row, col)

            if building == 'R':
                adjacent_buildings = [grid[r][c] for r, c in adjacent_positions]
                if 'I' in adjacent_buildings:
                    score += 1
                else:
                    score += adjacent_buildings.count('R')
                    score += adjacent_buildings.count('C')
                    score += 2 * adjacent_buildings.count('O')
            elif building == 'I':
                score += industry_count
                coins += sum(1 for r, c in adjacent_positions if grid[r][c] == 'R')
            elif building == 'C':
                adjacent_buildings = [grid[r][c] for r, c in adjacent_positions]
                score += adjacent_buildings.count('C')
                coins += adjacent_buildings.count('R')
            elif building == 'O':
                adjacent_buildings = [grid[r][c] for r, c in adjacent_positions]
                score += adjacent_buildings.count('O')
            elif building == '*':
                score += len([cell for cell in grid[row] if cell == '*'])

    return score, coins


    




def choosebuilding():
    buildings = ["R", "I", "C", "*", "O"]

    # Pick 2 random elements
    randombuildings = random.sample(buildings, 2)
    print("Randomly selected buildings:", randombuildings)

    # Ask the user to choose a building
    ansbuilding = input("Choose which building to build: ").strip().upper()

    # Check if the chosen building is in the randomly selected buildings
    if ansbuilding in randombuildings:
        print(f"{ansbuilding} is in the randomly selected buildings.")
        while True:
            try:
                row = int(input(f"Enter the row number (0-19) to place {ansbuilding}: "))
                col = int(input(f"Enter the column number (0-19) to place {ansbuilding}: "))

                # Check if the chosen position is within grid boundaries
                if 0 <= row < 20 and 0 <= col < 20:
                    return ansbuilding, row, col  # Return building and position
                else:
                    print("Invalid position. Please enter valid row and column numbers.")
            except ValueError:
                print("Invalid input. Please enter numeric values.")
    else:
        print(f"{ansbuilding} is not in the randomly selected buildings.")
        return None, None, None

def arcademode():
    buildings = ["R", "I", "C", "*", "O"]
    rows, cols = 20, 20

    # Create grid filled with 'P'
    grid = [['P' for _ in range(cols)] for _ in range(rows)]

    # Initial number of coins
    coins = 10

    # Function to print the grid
    def print_grid(grid):
        for row in grid:
            print(' '.join(row))

    # Print the initial grid
    print("Initial grid:")
    print_grid(grid)
    print(f"Initial coins: {coins}")

    # Loop to place buildings
    while coins > 0:
        # Call the function to choose a building
        ansbuilding, row, col = choosebuilding()
        if ansbuilding is None:
            continue

        # Check if the chosen spot is already taken
        if grid[row][col] != 'P':
            print(f"Spot at row {row} and column {col} is already taken by {grid[row][col]}. Choose another spot.")
            continue

        # Place the chosen building on the grid
        grid[row][col] = ansbuilding
        coins -= 1  # Deduct one coin

        # Calculate the score and coins after placing the building
        score, generated_coins = calculate_score_and_coins(grid)
        coins += generated_coins  # Add generated coins

        # Print the updated grid and score
        print("Updated grid:")
        print_grid(grid)
        print(f"Remaining coins: {coins}")
        print(f"Current score: {score}")

        if coins <= 0:
            print("No more coins left. Exiting the game.")
            break

        # Ask the user if they want to place another building
        

# Start the arcade mode
arcademode()



   
 







print("Ngee Ann City")
print("1.) Arcade Mode")
print("2.) FreePlay Mode")
print("3.) LeaderBoard")
def choose():
    ans = int(input("Choose option:"))
    if ans == 1:
      print("You entered Arcade Mode.")
      arcademode()
    elif ans == 2:
      print("You entered FreePlay Mode.")
    elif ans == 3:
      print("You entered LeaderBoard.")
    else:
      print("You entered a number other than 1, 2, or 3.")
      print("Try again")
      choose()

choose()




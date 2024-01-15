import random

#classes we later use for any cellular automaton
class Cell:     #class for a single cell
    def __init__(self, state=0, position=(0, 0)):
        self.state = state  
        self.position = position

    def __repr__(self):
        return f"Cell({self.state}, {self.position})"


class Grid:         #class for a grid of cells
    def __init__(self, width, height):  
        self.width = width
        self.height = height
        self.cells = [[Cell(position=(x, y)) for x in range(width)] for y in range(height)]

    def get_cell(self, x, y):
        return self.cells[y][x]

    def set_cell_state(self, x, y, state):
        self.cells[y][x].state = state

    def __repr__(self):
        return f"Grid({self.width}x{self.height})"

#Adding new rules ontop of the basic cellular automaton

class BioCell(Cell):
    def __init__(self, cell_type='cell', lifespan=10, position=(0, 0), state=1):
        super().__init__(state=state, position=position)
        self.cell_type = cell_type
        self.lifespan = lifespan

    def move(self, width, height, grid):
        # Check for food in adjacent cells
        x, y = self.position
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < width and 0 <= ny < height:
                adjacent_cell = grid.get_cell(nx, ny)
                if adjacent_cell.state == 2:
                    # Move to the food cell and consume it
                    self.position = (nx, ny)
                    adjacent_cell.state = 0  # Update the state of the food cell
                    return BioCell(position=(x, y), state=1, lifespan=10)  # Return a new cell to be added to the grid

        # If no food was found, move randomly
        direction = random.choice(['up', 'down', 'left', 'right'])
        if direction == 'up' and y > 0:
            y -= 1
        elif direction == 'down' and y < height - 1:
            y += 1
        elif direction == 'left' and x > 0:
            x -= 1
        elif direction == 'right' and x < width - 1:
            x += 1
        self.position = (x, y)
        self.age()
        return (x, y)

    def age(self):
        self.lifespan -= 1
        if self.lifespan <= 0:
            self.state = 2  # state 0 for dead
            self.cell_type = 'food'  # Dead cells become food

class Food(Cell):
    def __init__(self, position=(0, 0)):
        super().__init__(state=2, position=position)  # state 2 for food

class BioGrid(Grid):
    def __init__(self, width, height, initial_cells=None):
        super().__init__(width, height)
        self.cells = [[BioCell(position=(x, y), state=0) for x in range(width)] for y in range(height)]  # state 0 for empty fields

        if initial_cells:
            for cell_info in initial_cells:
                if cell_info[2] == 'food':
                    x, y, cell_type = cell_info
                    self.cells[y][x] = Food(position=(x, y))
                else:
                    x, y, cell_type, lifespan = cell_info
                    self.cells[y][x] = BioCell(cell_type=cell_type, lifespan=lifespan, position=(x, y), state=1)


    def update(self):
        new_cells = [[BioCell(position=(x, y), state=0) for x in range(self.width)] for y in range(self.height)]  #grid with empty cells
        for y in range(self.height):
            for x in range(self.width):
                cell = self.cells[y][x]
                if cell.state == 1:  # If the cell is alive
                    result = cell.move(self.width, self.height, self)
                    if isinstance(result, BioCell):  # If the cell moved to a food cell and duplicated
                        new_cells[y][x] = result  # Place the new cell at the old position
                        new_cells[cell.position[1]][cell.position[0]] = cell  # Move the original cell to the new position
                    else:  # If the cell moved to an empty cell
                        new_x, new_y = result
                        if cell.lifespan > 0:  # If the cell still has lifespan left after moving
                            new_cells[new_y][new_x] = BioCell(position=result, lifespan=cell.lifespan, state=1)  # Move the cell
                        elif cell.lifespan == 0:  # If the cell's lifespan has reached 0 after moving
                            new_cells[new_y][new_x] = Food(position=result)  # Replace the cell with food
                elif cell.state == 2:  # If the cell is food
                    new_cells[y][x] = Food(position=(x, y))
        self.cells = new_cells


    def print_grid(self):
        # First, print the grid
        for row in self.cells:
            for cell in row:
                if cell.state == 1:
                    print('1', end=' ')
                elif cell.state == 2:
                    print('2', end=' ')
                else:
                    print('0', end=' ')
            print()

        # Then, print the cell information
        for row in self.cells:
            for cell in row:
                if cell.state == 1:
                    print(f"Cell at {cell.position} with lifespan {cell.lifespan}")


def run_simulation(cycles):
    initial_config = [
        (5, 5, 'cell', 7),  # One cell at position (5, 5) with lifespan 7
        (7, 7, 'food'), 
        (3, 3, 'food')
    ]
    grid = BioGrid(width=10, height=10, initial_cells=initial_config)  # Create a grid with the initial configuration
    for _ in range(cycles):
        grid.print_grid()
        print()
        grid.update()

run_simulation(10)


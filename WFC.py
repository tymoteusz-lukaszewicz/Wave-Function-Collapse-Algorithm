import random as r
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

# Define the possible states (tiles) and their connectivity rules (Top, Right, Bottom, Left)
# 0: horizontal, 1: vertical, 2: bottom_left, 3: bottom_right, 4: top_left, 5: top_right, 6: blank
states = [[0, 1, 0, 1], [1, 0, 1, 0], [0, 0, 1, 1], [0, 1, 1, 0], [1, 0, 0, 1], [1, 1, 0, 0], [0, 0, 0, 0]]
matrix = []        # Will store the grid of cells
size = 10          # Size of the output map (size x size)

class Cell():
    """Represents a single cell in the grid."""
    def __init__(self) -> None:
        self.state = None   # The index of the tile in the 'states' list
        self.top = None     # Connection on the top edge (0 or 1)
        self.right = None   # Connection on the right edge (0 or 1)
        self.bottom = None  # Connection on the bottom edge (0 or 1)
        self.left = None    # Connection on the left edge (0 or 1)


class Map():
    """Represents the map being generated using the WFC algorithm."""
    def __init__(self, size) -> None:
        self.size = size

    def build_map(self):
        """Initializes the map with empty cells."""
        for i in range(self.size):
            row = []
            for j in range(self.size):
                cell = Cell()
                row.append(cell)
            matrix.append(row)


    def check_match(self, x, y):
        """
        Checks which tile options are compatible with the neighboring cells.

        Args:
            x (int): The x-coordinate of the cell.
            y (int): The y-coordinate of the cell.

        Returns:
            tuple: A tuple containing the number of valid options and a list of their indices.
                   Returns a large number (1000) and an empty list if the cell is already collapsed.
        """
        cell = matrix[y][x]
        options = []
        if cell.state is None:  # If the cell is not yet collapsed
            # Get the bottom connection of the top neighbor (if exists)
            if y > 0:
                top_connection = matrix[y - 1][x].bottom
            else:
                top_connection = None

            # Get the left connection of the right neighbor (if exists)
            if x < self.size - 1:
                right_connection = matrix[y][x + 1].left
            else:
                right_connection = None

            # Get the top connection of the bottom neighbor (if exists)
            if y < self.size - 1:
                bottom_connection = matrix[y + 1][x].top
            else:
                bottom_connection = None

            # Get the right connection of the left neighbor (if exists)
            if x > 0:
                left_connection = matrix[y][x - 1].right
            else:
                left_connection = None

            # The current state of the neighbors' connections [Top, Right, Bottom, Left] for the current cell
            my_state = [top_connection, right_connection, bottom_connection, left_connection]

            # Iterate through all possible tile states
            for i, state in enumerate(states):
                is_compatible = True
                # Check if the current tile's connections are compatible with the neighbors' connections
                for a, b in zip(my_state, state):
                    if a == b or a is None:  # If connections match or the neighbor is not yet collapsed (None)
                        is_compatible = True
                    else:
                        is_compatible = False
                        break  # If any connection is incompatible, move to the next tile state
                if is_compatible:
                    options.append(i)  # Add the index of the compatible tile state

            return len(options), options
        else:
            return 1000, []  # Cell already collapsed, high entropy


    def find_min_enthropy_and_collapse(self):
        """
        Finds the cell with the minimum entropy (fewest possible states) and collapses it
        to a random compatible state.
        """
        min_entropy = float('inf')
        best_options = []
        best_pos = [0, 0]

        # Iterate through all cells in the grid
        for y in range(self.size):
            for x in range(self.size):
                entropy, options = self.check_match(x, y)
                if entropy < min_entropy and matrix[y][x].state is None:
                    min_entropy = entropy
                    best_options = options
                    best_pos = [y, x]

        # If there are valid options for the cell with minimum entropy
        if best_options:
            collapsed_state_index = r.choice(best_options)
            matrix[best_pos[0]][best_pos[1]].state = collapsed_state_index
            matrix[best_pos[0]][best_pos[1]].top = states[collapsed_state_index][0]
            matrix[best_pos[0]][best_pos[1]].right = states[collapsed_state_index][1]
            matrix[best_pos[0]][best_pos[1]].bottom = states[collapsed_state_index][2]
            matrix[best_pos[0]][best_pos[1]].left = states[collapsed_state_index][3]


    def return_indices_of_pieces(self):
        """Returns a 2D list representing the map with the indices of the chosen tiles."""
        image_indices = []
        for row in matrix:
            indices_row = [cell.state for cell in row]
            image_indices.append(indices_row)
        return image_indices


if __name__ == '__main__':
    map_generator = Map(size)
    map_generator.build_map()

    # Run the WFC algorithm for size^2 iterations to collapse most cells
    for _ in range(size ** 2):
        map_generator.find_min_enthropy_and_collapse()

    generated_map_indices = map_generator.return_indices_of_pieces()

    # Create a blank image to draw the tiles onto
    image = np.zeros((len(generated_map_indices) * 30, len(generated_map_indices) * 30))

    # Load the tile images
    tile_filenames = ('collapse_hor.png collapse_vert.png collapse_bottom_left.png collapse_bottom_right.png collapse_top_left.png collapse_top_right.png collapse_blank.png').split()
    pixel_tiles = []
    for filename in tile_filenames:
        img = Image.open(filename)
        grayscale_image = img.convert("L")  # Convert to grayscale
        pixel_tiles.append(np.array(grayscale_image))

    # Paste the loaded tiles onto the main image based on the generated map indices
    for y_index, column in enumerate(generated_map_indices):
        for x_index, tile_index in enumerate(column):
            current_tile_pixels = pixel_tiles[generated_map_indices[y_index][x_index]]
            for i in range(x_index * 30, (x_index + 1) * 30):
                for j in range(y_index * 30, (y_index + 1) * 30):
                    image[j][i] = current_tile_pixels[j % 30][i % 30]

    # Display the generated image
    plt.imshow(image, cmap='inferno')
    plt.title("Generated Map using Wave Function Collapse")
    plt.axis('off')  # Turn off axis labels and ticks
    plt.show()
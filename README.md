# Wave-Function-Collapse-Algorithm

# 2D Map Generation using Wave Function Collapse Algorithm

## Purpose

Presentation of the final version of the project for my portfolio. This project implements the Wave Function Collapse (WFC) algorithm to generate 2D tile-based maps. The algorithm works by iteratively collapsing the state of cells in a grid based on constraints imposed by neighboring cells.

## Files in Repository

* `WFC.py`: The Python script containing the implementation of the WFC algorithm.
* `collapse_hor.png`, `collapse_vert.png`, `collapse_bottom_left.png`, `collapse_bottom_right.png`, `collapse_top_left.png`, `collapse_top_right.png`, `collapse_blank.png`: Image files representing the different tile types used in the generation.

## Technologies Used

* Programming Language: Python
* Libraries: random, matplotlib, numpy, PIL (Pillow)

## Setup Instructions

1.  Make sure you have Python 3.x installed.
2.  Install the required libraries if you haven't already:
    ```bash
    pip install matplotlib numpy Pillow
    ```
3.  Ensure that all the `collapse_*.png` tile images are in the same directory as the `wfc_algorithm.py` script.

## Running the Code

To generate a map using the WFC algorithm, simply run the Python script:

```bash
python wfc_algorithm.py

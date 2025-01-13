# New England 39-Bus System Interaction Factors Tool

This Python tool calculates interaction factors among buses in the New England 39-bus transmission grid. It uses a manually defined list of connection lines, 
performs shortest-path analysis using Dijkstra's algorithm, and computes interaction factors based on short-circuit voltage values provided in an Excel file.

## Features

- **Input Format**: Accepts short-circuit voltage values in Excel format for flexibility and convenience.
- **Shortest Path Analysis**: Uses Dijkstra's algorithm to compute minimum-length paths between all bus pairs based on a manually defined connection list.
- **Interaction Factors**: Calculates interaction factors using computed shortest paths and voltage data.
- **Visualization**: Provides an optional plotting function to visualize interaction factors.

## Workflow

1. **Define Connection Lines**: The connection lines between buses are defined manually as a list of triples:  
   Each triple has the format `(starting_bus, ending_bus, length_of_connection_line)`.
2. **Adjacency List Creation**: The connection list is used to create an adjacency list (a dictionary) for the grid.
3. **Shortest Path Analysis**: The Dijkstra algorithm calculates the shortest paths between buses.
4. **Interaction Factor Calculation**: Using short-circuit voltage values from the Excel file, interaction factors are computed.
5. **Plotting** (Optional): Interaction factors can be plotted by calling a dedicated function.

## Requirements

- **Python Version**: Python 3.8 or later.
- **Dependencies**: 
  - `openpyxl`: For reading Excel files containing short-circuit voltage values.
  - `numpy`: For numerical computations.
  - `matplotlib`: For plotting interaction factors.
  - `heapq`: For implementing Dijkstra's algorithm efficiently.

## Contact
If you have any questions, feel free to reach out:

- **Linkedin**: www.linkedin.com/in/bartu-badem-4a726b283

from openpyxl import Workbook, load_workbook
from openpyxl.utils import get_column_letter
import numpy as np
import matplotlib.pyplot as plt
import heapq

# Loading the excel file
wb_voltages = load_workbook('Kurzschlussspannungen.xlsx')

# Loading the worksheet from excel file
ws_voltages = wb_voltages['Kurzschluss']

trafo_distance = 0.2

# Converting the bus system to an edge list (starting bus, ending bus, distance of the line between the busses in km)
edge_list = [('Bus01', 'Bus02', 163 ), ('Bus01', 'Bus39', 99 ), ('Bus02', 'Bus03', 60), ('Bus02', 'Bus25', 34 ), ('Bus02', 'Bus30', trafo_distance), ('Bus03', 'Bus04', 85 ), ('Bus03', 'Bus18', 53 ),
    ('Bus04', 'Bus05', 51 ), ('Bus04', 'Bus14', 51 ), ('Bus05', 'Bus06', 10 ), ('Bus05', 'Bus08', 44 ), ('Bus06', 'Bus07', 37 ), ('Bus06', 'Bus11', 33 ), ('Bus06', 'Bus31', trafo_distance ),
    ('Bus07', 'Bus08', 18 ), ('Bus08', 'Bus09', 144 ), ('Bus09', 'Bus39', 99 ), ('Bus10', 'Bus11', 17 ), ('Bus10', 'Bus13', 17 ), ('Bus10', 'Bus32', trafo_distance ), ('Bus12', 'Bus11', trafo_distance ),
    ('Bus12', 'Bus13', trafo_distance ), ('Bus13', 'Bus14', 40 ), ('Bus14', 'Bus15', 86 ), ('Bus15', 'Bus16', 37), ('Bus16', 'Bus17', 35 ), ('Bus16', 'Bus19', 77 ), ('Bus16', 'Bus21', 54 ),
    ('Bus16', 'Bus24', 23 ), ('Bus17', 'Bus18', 33 ), ('Bus17', 'Bus27', 69 ), ('Bus19', 'Bus20', trafo_distance ), ('Bus19', 'Bus33', trafo_distance ), ('Bus20', 'Bus34', trafo_distance ), 
    ('Bus21', 'Bus22', 56 ), ('Bus22', 'Bus23', 38 ), ('Bus22', 'Bus35', trafo_distance ), ('Bus23', 'Bus24', 139 ), ('Bus23', 'Bus36', trafo_distance ), ('Bus25', 'Bus26', 128 ), 
    ('Bus25', 'Bus37', trafo_distance ), ('Bus26', 'Bus27', 58 ), ('Bus26', 'Bus28', 188 ), ('Bus26', 'Bus29', 248 ), ('Bus28', 'Bus29', 60 ), ('Bus29', 'Bus38', trafo_distance )]



def edge_list_to_adjacency_list(edge_list):
    """
    Converts the edge list to a adjacency list

    Parameters:
    edge_list (list): A list of tuples, where each tuple contains three elements: (starting bus, ending bus, distance)

    Returns:
    adj_list: A dictionary where the keys are bus identifiers and the values are the distances (float) to the 'start' bus. 
    But this contains only direct connections. For all possible connections see the function dijkstra below.

    """
    adj_list = {}
    for (src, dest, weight) in edge_list:
        if src not in adj_list:
            adj_list[src] = {}
        if dest not in adj_list:
            adj_list[dest] = {}
        
        adj_list[src][dest] = weight
        adj_list[dest][src] = weight

    return adj_list



#Dijkstra's Algorithm to find the shortest path between two nodes


def dijkstra(adj_list, start):
    """
    Calculates the distances between a specified 'start' bus and all other buses.

    Parameters:
    start (str): The identifier of the starting bus.
    buses (dict): A dictionary containing bus identifiers as keys and their coordinates (e.g., tuples of latitude and longitude) as values.

    Returns:
    sorted_distances: A dictionary where the keys are bus identifiers and the values are the distances (float) to the 'start' bus.

    Notes:
    The distance calculation assumes a 2D Euclidean distance between coordinates.
    """
    distances = {node: float('inf') for node in adj_list}
    distances[start] = 0

    # Priority queue to track nodes and current shortest distance
    priority_queue = [(0, start)]

    while priority_queue:
        # Pop the node with the smallest distance from the priority queue
        current_distance, current_node = heapq.heappop(priority_queue)

        # Skip if a shorter distance to current_node is already found
        if current_distance > distances[current_node]:
            continue

        # Explore neighbors and update distances if a shorter path is found
        for neighbor, weight in adj_list[current_node].items():
            distance = current_distance + weight

            # If shorter path to neighbor is found, update distance and push to queue
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(priority_queue, (distance, neighbor))

    sorted_distances = {key: distances[key] for key in sorted(distances)}
    return sorted_distances



def interaction_factors(start, worksheet):
    """
    Calculates the interaction factors for a given (starting) bus.

    Parameters:
    start (str): The identifier of the starting bus.
    worksheet : An excel worksheet where the information for the calculations is stored
    
    Returns:
    interaction_factors: A list containing the interaction factors between the starting bus and other buses

    """

    interaction_factors = np.empty(worksheet.max_column -1)
    
    for col_index in range(1, worksheet.max_column +1):
        col_letter = get_column_letter(col_index)  # Get the column letter (e.g., "A", "B")
        
        if worksheet[f"{col_letter}1"].value == start:
            array_index = 0
            
            for line_index in range(2, worksheet.max_row +1):
                interaction_factors[array_index] = 1 - worksheet[f"{col_letter}{line_index}"].value
                array_index += 1

    return interaction_factors
                


def plot_interaction_factors(start, worksheet, dictionary):
    """
    Plots the interaction factors for a given (starting) bus.

    Parameters:
    start (str): The identifier of the starting bus.
    worksheet : An excel worksheet where the information for the calculations is stored
    dictionary : A dictionary where the keys are bus identifiers and the values are the distances (float) to the 'start' bus.
    
    """

    interaction_factors = np.empty(worksheet.max_column -1)
    
    for col_index in range(1, worksheet.max_column +1):
        col_letter = get_column_letter(col_index)  # Get the column letter (e.g., "A", "B")
        
        if worksheet[f"{col_letter}1"].value == start:
            array_index = 0
            
            for line_index in range(2, worksheet.max_row +1):
                interaction_factors[array_index] = 1 - worksheet[f"{col_letter}{line_index}"].value
                array_index += 1
    
    x_axis_values = list(dictionary.values())

    plt.plot(x_axis_values, interaction_factors, 'o', linestyle = 'None')
    plt.show()

  
                

adj_list = edge_list_to_adjacency_list(edge_list)

plot_interaction_factors('Bus25', ws_voltages, dijkstra(adj_list, 'Bus01'))


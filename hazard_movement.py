#This file contains the methods for hazard propagation or movement

''' Purpose: This function propagates hazard to all adjacent cells (suitable for fire-style hazards).
Input: The input to this function are current state of complete environemnt and the hazard's current positions.
Output: The function returns the updated hazard positions.
Method: The function simply updates all adjacent cells of a hazard affected cell as hazarad affected.'''
#Takes current fire affected cells as input, and propagates the fire to all adjacent cells
def fire_propagate(environment, hazard_positions):
    new_hazard_positions = []
    for cell in hazard_positions:
        x = cell[0]
        y = cell[1]
        movement = [[0, -1], [0, 1], [-1, 0], [1, 0], [-1, -1], [-1, 1], [1, -1], [1, 1]]
        for possible_move in movement:
            new_x = x+possible_move[0]
            new_y = y+possible_move[1]
            if new_x >= 0 and new_x < len(environment) and new_y >= 0 and new_y < len(environment[0]):
                if [new_x, new_y] not in new_hazard_positions:
                    new_hazard_positions.append([new_x, new_y])
    hazard_positions.extend(new_hazard_positions)

''' Purpose: This function moves hazard to an adjacent cell.
Input: The input to this function are current state of complete environemnt and the hazard's current position.
Output: The function returns the updated hazard position.
Method: The function simply moves the hazard to an adjacent cell.'''
#Takes current suspect cell as input, and moves suspect to an adjacent cell
def suspect_move(environment, hazard_position):
    potential_hazard_positions = []
    x = hazard_position[0]
    y = hazard_position[1]
    movement = [[0, -1], [0, 1], [-1, 0], [1, 0], [-1, -1], [-1, 1], [1, -1], [1, 1]]
    for possible_move in movement:
        new_x = x+possible_move[0]
        new_y = y+possible_move[1]
        if new_x >= 0 and new_x < len(environment) and new_y >= 0 and new_y < len(environment[0]):
            potential_hazard_positions.append([new_x, new_y])
    hazard_position = potential_hazard_positions[0]

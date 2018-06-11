#This file contains the methods for repellence

''' Purpose: This function propagates repellents to all adjacent cells (suitable for liquid repellents).
Input: The input to this function are current state of complete environemnt and the repellent's current positions.
Output: The function returns the updated repellent positions.
Method: The function simply updates all adjacent cells of a repellent cell as repellent.'''
#Takes current repellent cells as input, and propagates repellents to adjacent cells
def repellent_propagate(environment, repellent_positions):
    new_repellent_positions = []
    for cell in repellent_positions:
        x = cell[0]
        y = cell[1]
        movement = [[0, -1], [0, 1], [-1, 0], [1, 0], [-1, -1], [-1, 1], [1, -1], [1, 1]]
        for possible_move in movement:
            new_x = x+possible_move[0]
            new_y = y+possible_move[1]
            if new_x >= 0 and new_x < len(environment) and new_y >= 0 and new_y < len(environment[0]):
                if [new_x, new_y] not in new_repellent_positions:
                    new_repellent_positions.append([new_x, new_y])
    repellent_positions.extend(new_repellent_positions)

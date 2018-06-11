import random
''' Purpose: This is a helper function for breadth first search.'''
def backtrace(parent, start, end):
    path = [end]
    while path[-1] != start:
        path.append(eval(parent[str(path[-1])]))
    path.reverse()
    return path

''' Purpose: This function computes the optimal exit plan for an agent.
Input: The input to this function are current state of complete environemnt and the agent's current position.
Output: The function returns the shortest path from agent's current location to the nearest exit.
Method: The function uses breadth first search to find the path from agent's current ocation to nearest exit.'''
def path_to_nearest_exit(environment, agent_position):
    visited = [[0 for i in xrange(len(environment))] for j in xrange(len(environment[0]))]
    x = agent_position[0]
    y = agent_position[1]
    visited[x][y] = 1
    queue = []
    queue.append(agent_position)
    parent = {}
    
    movement = [[0, -1], [0, 1], [-1, 0], [1, 0], [-1, -1], [-1, 1], [1, -1], [1, 1]]
    
    while queue:
        #print 'Current Queue:', queue
        node = queue.pop(0)
        #print 'Current Node:', node
        if environment[node[0]][node[1]] == 2 or environment[node[0]][node[1]] == 3:
            #print 'Path Found'
            path = backtrace(parent, agent_position, node)
            return path
        for possible_move in movement:
            new_x = node[0]+possible_move[0]
            new_y = node[1]+possible_move[1]
            if new_x >= 0 and new_x < len(environment) and new_y >= 0 and new_y < len(environment[0]):
                if environment[new_x][new_y] <> 0 and environment[new_x][new_y] <> 4 and visited[new_x][new_y] == 0:
                    parent[str([new_x, new_y])] = str(node)
                    queue.append([new_x, new_y])
                    visited[new_x][new_y] = 1
    return [agent_position]

''' Purpose: This function computes a random move for an agent.
Input: The input to this function are current state of complete environemnt and the agent's current position.
Output: The function returns a random safe move for the agent. 
Method: The function searches for safe next moves and returns one of these moves.'''
def random_move(environment, agent_position):
    x = agent_position[0]
    y = agent_position[1]
    potential_agent_positions = []
    movement = [[0, -1], [0, 1], [-1, 0], [1, 0], [-1, -1], [-1, 1], [1, -1], [1, 1]]
    for possible_move in movement:
        new_x = x+possible_move[0]
        new_y = y+possible_move[1]
        if new_x >= 0 and new_x < len(environment) and new_y >= 0 and new_y < len(environment[0]):
            if environment[new_x][new_y] <> 0 and environment[new_x][new_y] <> 4:
                potential_agent_positions.append([new_x, new_y])
    potential_agent_positions.append(agent_position)
    return random.choice(potential_agent_positions)

''' Purpose: This function computes the exit plan for an agent that belongs to a group with predetermined destination.
Input: The input to this function are current state of complete environemnt, the agent's current position and the predetermined destination.
Output: The function returns the shortest safe path from agent's current location to the predetermined destination.
Method: The function uses breadth first search to find the shortest safe path from agent's current ocation to predetermined destination.'''
def path_to_given_exit(environment, agent_position, given_destination):
    visited = [[0 for i in xrange(len(environment))] for j in xrange(len(environment[0]))]
    x = agent_position[0]
    y = agent_position[1]
    visited[x][y] = 1
    queue = []
    queue.append(agent_position)
    parent = {}
    
    movement = [[0, -1], [0, 1], [-1, 0], [1, 0], [-1, -1], [-1, 1], [1, -1], [1, 1]]
    
    while queue:
        #print 'Current Queue:', queue
        node = queue.pop(0)
        #print 'Current Node:', node
        if node[0] == given_destination[0] and node[1] == given_destination[1]:
            #print 'Path Found'
            path = backtrace(parent, agent_position, node)
            return path
        for possible_move in movement:
            new_x = node[0]+possible_move[0]
            new_y = node[1]+possible_move[1]
            if new_x >= 0 and new_x < len(environment) and new_y >= 0 and new_y < len(environment[0]):
                if environment[new_x][new_y] <> 0 and environment[new_x][new_y] <> 4 and visited[new_x][new_y] == 0:
                    parent[str([new_x, new_y])] = str(node)
                    queue.append([new_x, new_y])
                    visited[new_x][new_y] = 1
    return [agent_position]
                    
                    
                    

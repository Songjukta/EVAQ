import random
from random import randint

environment_file = open("environment.txt", "w")
agent_characteristics_file = open("agent_characteristics.txt", "w")

row = 10
col = 10
exit_count = 2
agent_count = 6
object_count = 7
hazard_location_count = 2

environment = [[1 for c in range(col)] for r in range(row)]

boundary_cells = []

for c in range(col):
    boundary_cells.append((0, c))
    boundary_cells.append((row-1, c))

for r in range(row):
    boundary_cells.append((r, 0))
    boundary_cells.append((r, col-1))

for ex in range(exit_count):
    r = random.choice(boundary_cells)[0]
    c = random.choice(boundary_cells)[1]
    environment[r][c] = 2
        
ob = 0

while ob <object_count:
    ob_w = 3
    ob_h = 3
    ob_type = randint(0, 2)
    
    r = randint(0, row-ob_w-1)
    c = randint(0, col-ob_h-1)
    print r, c
    
    if ob_type == 0:        
        marker = 0
        for l in range(ob_w):
            if environment[r+l][c] <> 1:
                marker = 1
                break
        if marker == 0:
            for l in range(ob_w):
                environment[r+l][c] = 0
            ob += 1
            
    elif ob_type == 1:
        marker = 0
        for l in range(ob_h):
            if environment[r][c+l] <> 1:
                marker = 1
                break
        if marker == 0:
            for l in range(ob_h):
                environment[r][c+l] = 0
            ob += 1
            
    elif ob_type == 2:
        marker = 0
        for l1 in range(ob_w):
            for l2 in range(ob_h):
                if environment[r+l1][c+l2] <> 1:
                    marker = 1
                    break
        if marker == 0:
            for l1 in range(ob_w):
                for l2 in range(ob_h):
                    environment[r+l1][c+l2] = 0
            ob += 1
        
hc = 0

while hc <hazard_location_count:
    r = randint(0, row-1)
    c = randint(0, col-1)
    if environment[r][c] == 1:
        environment[r][c] = 4
        hc += 1

ag = 0

while ag < agent_count:
    r = randint(0, row-1)
    c = randint(0, col-1)
    if environment[r][c] == 1:
        environment[r][c] = ag+5 
        agent_characteristics_file.write(str(ag+5)+', '+str(randint(0, 1))+', '+str(randint(0, 2))+', '+str(randint(0, 1))+'\n')
        ag += 1
    

for r in range(row):
    for c in range(col):
        environment_file.write(str(environment[r][c]))
        if c <> (col -1):
            environment_file.write(', ')
    environment_file.write('\n')

environment_file.close()
agent_characteristics_file.close()
    
    



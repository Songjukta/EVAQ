import random
import copy
import numpy as np
import matplotlib.pyplot as plt

from hazard_movement import fire_propagate
from repellence import repellent_propagate
from agent_path_planning import path_to_nearest_exit
from agent_path_planning import path_to_given_exit
from agent_path_planning import random_move

''' The following code fragment initializes the environment matrix based on user input.'''
f = open ( 'environment.txt' , 'r')
environment = [map(int,line.split(',')) for line in f ]
#print 'Environment:', environment

''' The following lists hold the static positions: exits and objects.'''
object_positions = []
exit_positions = []
special_exit_positions = []

''' The following lists hold the dynamic positions: agents and hazards.'''
hazard_positions = []
agent_positions = {}

agent_count = 0

''' The following list holds the planned agent destinations (based on agent plan).'''
agent_destinations = []

''' The  following code fragment initializes the static and dynamic position lists from environment.'''
for i, row in enumerate(environment):
    for j, elem in enumerate(row):
        if elem == 1:
            object_positions.append([i, j])
        if elem == 2:
            exit_positions.append([i, j])
        elif elem == 3:
            special_exit_positions.append([i, j])
        elif elem == 4:
            hazard_positions.append([i, j])
        elif elem >= 5:
            agent_positions[elem] = [i, j]
            agent_count +=1

#print 'Object Positions:', object_positions
print 'Exit Positions:', exit_positions
print 'Special Exit Positions:', special_exit_positions
#print 'Hazard Initial Positions:', hazard_positions
#print 'Agent Initial Positions:', agent_positions

agent_speeds = {}

'''The dimesnions of each cell is: 1.5' x 1.5'.'''

print '**************************************************************************'

'''The following dictionary stores the parameters (mean, sd) of speed distribution for different agent classes.
Classes: Gender = {Male (0), Female (1)}, Age = {Child, (0), Adult (1), Elderly (2)}, Disability = {No (0), Yes (1)}''' 
speed_distribution = {(0, 0, 0):(1.08, 0.26),
                      (0, 0, 1):(0.92, 0.34),
                      (0, 1, 0):(1.24, 0.45),
                      (0, 1, 1):(1.06, 0.26),
                      (0, 2, 0):(1.05, 0.15),
                      (0, 2, 1):(0.91, 0.13),
                      (1, 0, 0):(1.08, 0.26),
                      (1, 0, 1):(0.92, 0.34),
                      (1, 1, 0):(1.30, 0.38),
                      (1, 1, 1):(1.06, 0.26),
                      (1, 2, 0):(1.04, 0.16),
                      (1, 2, 1):(0.89, 0.14)}

'''The following code fragment samples the speed of each agent based on his/her characterictics (Gender, Age, and Disability).
Note that, here the speed varaiables store inverse speed, i.e., how much simulation time is required for crossing a single cell.'''
with open('agent_characteristics.txt') as f:
    lines = f.read().splitlines()
for line in lines:
    agent_id = int(line.split(',')[0])
    agent_characteristics = (int(line.split(',')[1]), int(line.split(',')[2]), int(line.split(',')[3]))
    speed_mean = speed_distribution[agent_characteristics][0]
    speed_variance = speed_distribution[agent_characteristics][1]
    speed_sample = np.random.normal(speed_mean, speed_variance)
    agent_speed = int(1.5*4/(speed_sample*3.28))+1   
    gender = {0: 'Male', 1:'Female'}
    age = {0: 'Child', 1:'Adult', 2: 'Elderly'}
    disability = {0: 'Regular', 1:'Disable'}
    print 'Agent', agent_id, 'Characteristics:', gender[agent_characteristics[0]], ', ', age[agent_characteristics[1]], ', ', disability[agent_characteristics[2]], ', ', speed_sample, ' m/s', ', ', agent_speed
    agent_speeds[agent_id] = agent_speed

#common_speed = 1
#if common_speed == 1:
    #for agent in agent_speeds:
        #agent_speeds[agent] = 2
    
print '**************************************************************************\n'

''' The following lists hold the agent groups (family, friends, etc.), and their common desitnations respectively.'''
agent_groups = []
agent_group_destinations = []

''' The  following code fragment initializes the agent groups based on user input.
Then, it assigns an exit location as a common destination for the group.'''
with open('agent_groups.txt') as f:
    lines = f.read().splitlines()
for line in lines:
    agent_list = line.split(',')
    min_speed = 1
    current_agent_group = []
    for agent_id in agent_list:
        current_agent_group.append(int(agent_id))
        if agent_speeds[int(agent_id)] > min_speed:
            min_speed = agent_speeds[int(agent_id)]
    for agent_id in agent_list:
        agent_speeds[int(agent_id)] = min_speed
    agent_groups.append(current_agent_group)

for group in agent_groups:
    agent_group_destinations.append(random.choice(exit_positions))
    #agent_group_destinations.append([5, 0])

group_agents = [j for i in agent_groups for j in i]

print 'Agent Groups:', agent_groups
print 'Agent Speeds:', agent_speeds
print 'Agent Group Destinations:', agent_group_destinations

''' The following lists hold the repellent cells.'''
repellent_positions = [(2, 4)]
degree_of_repellence = 2
repellent_initiation_time = 10
repellent_duration = 10


hazard_speed = 4

simulation_time = 0
survivor_count = 0
death_count = 0

agent_exit_time = {}

#Allocating agent destinations

time_axis = []
death_over_time = []
survival_over_time = []

text_file = open("Environment_States.csv", "w")
repellence_file = open("Repellent_States.csv", "w")

''' The  following code fragment is the main body of the simulation process.
The simulation ends when the fate of all agents have been decided (either survived or compromised).'''
while survivor_count+death_count < agent_count:
    simulation_time += 1
    print '**************************************', 'Time:', simulation_time, '**************************************'
    time_axis.append(simulation_time)
    
    ''' The  following code fragment implies that an agent's intial position has no object or hazard.'''
    for i, row in enumerate(environment):
        for j, elem in enumerate(row):
            if elem >= 5:
                environment[i][j] = 1

    if simulation_time >= repellent_initiation_time and (simulation_time - repellent_initiation_time) <= degree_of_repellence-1:
            repellent_propagate(environment, repellent_positions)
            print 'Repellent Cells:', repellent_positions
                
    ''' The  following code fragment invokes the hazard propagation method, if hazard is bound to move at this simulation time.
    It then updates the environment based on the updated hazard status.'''
    if simulation_time % hazard_speed == 0:
        fire_propagate(environment, hazard_positions)
        print 'Hazard is affecting adjacent cells'
        if simulation_time >= repellent_initiation_time and simulation_time <= repellent_initiation_time+repellent_duration:
            print 'Hazard can not propagate to repellent cells'
            for positions in hazard_positions:
                environment[positions[0]][positions[1]] = 4
        else:
            for positions in hazard_positions:
                if positions not in repellent_positions:
                    environment[positions[0]][positions[1]] = 4
        #print environment

    ''' The  following code fragment determines if any agent is compromised as hazard status is updated.
    It then puts the ids of compromised afents in a list.'''
    compromised_agent = []
    for agent in agent_positions:
        if environment[agent_positions[agent][0]][agent_positions[agent][1]] == 4:
            compromised_agent.append(agent)
            death_count += 1
            
    death_over_time.append(death_count)

    ''' The  following code fragment removes the compromised agents from active agent list.'''
    for agent in compromised_agent:
        del agent_positions[agent]
        print 'Agent', agent, 'has been compromised'

    ''' agent_plans stores each agent's (current) optimal exit plan.
    moving_agent_list tracks which agents will be moving at this simulation time.
    survived_agent tracks the agents who will reach their destination at this simulation time'''           
    agent_plans = {}
    moving_agent_list = []
    survived_agent = []

    ''' The  following code fragment invokes the path planning method (path_to_nearest_exit) for each agent.
    It then updates the exit plan for each agent.
    Note that, if an agent doesn't have a safe path to exit, the agent's plan is to wait in current cell for an arbitrary time period, until a path becomes available'''
    for agent in agent_positions:
        path = path_to_nearest_exit(environment, agent_positions[agent])
        path_length = len(path)
        if path[path_length-1] not in exit_positions and path[path_length-1] not in special_exit_positions:
            for ts in range(1, 10):
                path.append(path[path_length-1])
        agent_plans[agent] = path
        #print 'Agent', agent,'Current Exit Plan:', path
        
    #print agent_plans

    ''' The  following code fragment updates the plan for agents who are part of a group.
    The members of a given group have a predetermined common destination in mind.'''
    for index, group in enumerate(agent_groups):
        common_destination = agent_group_destinations[index]
        for agent in group:
            # print 'aaa', agent
            if agent in agent_positions:
                path = path_to_given_exit(environment, agent_positions[agent], common_destination)
                path_length = len(path)
                if path[path_length-1] not in exit_positions and path[path_length-1] not in special_exit_positions:
                    for ts in range(1, 10):
                        path.append(path[path_length-1])
                agent_plans[agent] = path
        #print 'Agent', agent,'Current Exit Plan:', path

    ''' The  following code fragment determines two things: which agents are moving at this simulation time, and
    subsequently which agents survive at this simulation time.'''
    for agent in agent_positions:
        if simulation_time % int(agent_speeds[agent]) == 0:
            path_length = len(agent_plans[agent])
            if path_length == 1 and  (agent_plans[agent][path_length-1] in exit_positions or agent_plans[agent][path_length-1] in special_exit_positions):
                survived_agent.append(agent)
            else:
                moving_agent_list.append((agent, len(agent_plans[agent])))
                
    print '***************** Agent Optimal Exit Plans ***************** '
    for agent_id in agent_plans:
        print 'Agent', agent_id, 'Optimal Exit Plan:', agent_plans[agent_id]
        
    print '***************** Agent Movement ***************** '

    if len(moving_agent_list) == 0 and len(survived_agent) == 0:
        print 'No agent is moving at this time'

    ''' The  following code fragment removes the survived agents from active agent list.'''
    for agent in survived_agent:
        del agent_plans[agent]
        del agent_positions[agent]
        print 'Agent', agent, 'survives'
        survivor_count += 1

    survival_over_time.append(survivor_count)
    
    ''' The  following code fragment determines the distance of each moving agent from exit.
    This is required for conflict resolution, where agents closer to exit move before agent far from the exit.'''               
    agent_movement_order = sorted(moving_agent_list, key=lambda tup: tup[1])
    
    for agent_tuple in agent_movement_order:
        print 'Agent', agent_tuple[0], 'is', (agent_tuple[1]-1), 'cells away from exit'

    

    ''' The  following code fragment probabilistically executes one of the following two steps for a moving agent.
    (1) The agent follows optimal plan and executes current step accordingly.
    (2) Agent drifts from optimal plan and executes a random step.
    These two steps are controlled using fate_control variable, which probabilistically selects one of the two alternatives.'''
    for agent_tuple in agent_movement_order:
        if agent_tuple[1] > 1:
            drift_flag = 0
            next_cell = agent_plans[agent_tuple[0]][1]           
            fate_control = random.uniform(0, 1)
            if fate_control < 0 and agent_tuple[0] not in group_agents:
                drift_flag = 1
                next_cell = random_move(environment, agent_plans[agent_tuple[0]][0])
            environment_print = copy.deepcopy(environment)
            for agent in agent_positions:
                environment_print[agent_positions[agent][0]][agent_positions[agent][1]] = agent
            for hd, row in enumerate(environment_print):
                for dh, col in enumerate(row):
                    if environment_print[hd][dh] == 2 or environment_print[hd][dh] == 3:
                        environment_print[hd][dh] = 1
            congestion_flag = 1
            #print next_cell[0], ' ', next_cell[1], ' ', environment_print[next_cell[0]][next_cell[1]], ' ', agent_tuple[0]
            if environment_print[next_cell[0]][next_cell[1]] == 1 or environment_print[next_cell[0]][next_cell[1]] == int(agent_tuple[0]):
                congestion_flag = 0
            if congestion_flag == 0:
                agent_positions[agent_tuple[0]] = next_cell
                if drift_flag <> 0:
                    print 'Agent', agent_tuple[0], 'may not be making an optimal decision'
                print 'Agent', agent_tuple[0], 'moves to cell', next_cell
            else:
                print 'Agent', agent_tuple[0], 'could not move due to congestion'
                print next_cell[0], ' ', next_cell[1], ' ', environment_print[next_cell[0]][next_cell[1]], ' ', agent_tuple[0]

    environment_print = copy.deepcopy(environment)
    for agent in agent_positions:
        environment_print[agent_positions[agent][0]][agent_positions[agent][1]] = agent
    for r in environment_print: 
        text_file.write(str(r)[1:-1])
        text_file.write('\n')

    repellent_print = copy.deepcopy(environment)
    if simulation_time >= repellent_initiation_time and simulation_time <= repellent_initiation_time+repellent_duration:
        for repellent in repellent_positions:
            environment_print[repellent[0]][repellent[1]] = -4
    for r in environment_print: 
        repellence_file.write(str(r)[1:-1])
        repellence_file.write('\n')

text_file.close()
repellence_file.close()
            
print '**************************************************************************'
print '**************************************************************************'
print 'Out of', agent_count, ',', survivor_count, 'agents survived and', death_count, 'compromised'

fig, ax = plt.subplots(nrows=1, ncols=1) 
ax.plot(time_axis, death_over_time)
ax.set_xlabel('Simulation Time')
ax.set_ylabel('# of Dead Agents')
fig.savefig('Death_Time'+'.png')
plt.close(fig)

fig, ax = plt.subplots(nrows=1, ncols=1) 
ax.plot(time_axis, survival_over_time)
ax.set_xlabel('Simulation Time')
ax.set_ylabel('# of Survived Agents')
fig.savefig('Survival_Time'+'.png')
plt.close(fig)





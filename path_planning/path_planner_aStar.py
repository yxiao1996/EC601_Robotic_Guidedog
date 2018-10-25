# Path Planner with A* algorith

#######################################################
#################### Assumptions ######################
#######################################################

# the starting position is the center position of the map, one layer below.
# the first step the person can take is directly in front of them or
# the diagonal in front of them

#######################################################
#######################################################


#Import Libraries
import sys
import cv2
import numpy as np
import math
m_v = float("inf")

# Define Path Planning Class
class path_planner(object):
	def __init__(self, map, goal=None):
		self.map = map

		height = len(map)
		width = len(map[1])
		center = int(int(width) / int(2))

		# If no goal provided, then assume the goal is the center position
		# at the end of the map.
		if goal == None:
			goal = [height-1, center]
		else:
			self.goal = goal

		# Initialize the heuristics map
		m_v_map = []
		[m_v_map.append([m_v]*width) for x in range(0,height)]
		self.heuristics = m_v_map.copy()
		self.heuristics[goal[0]][goal[1]] = 0 

		# Initialize the graph map
		the_graph=[]
		[the_graph.append([m_v]*width) for x in range(0,height)]
		self.graph = the_graph.copy()	

		# Initialize the openset with a starting location. For us this will be the center point
		# of the first row.
		self.openset = [[0,center]]

		self.closedsed = []

	def __str__(self):
		return str(self.map)

	def __repr__(self):
		return str(self.map)

	def gen_heuristics(self, heuristic_function=1):
		# loop over the heuristics map adding distances to each cell from the goal 
		# get the list of neighbors that are decided
		# If the heuristic_function is 1 then use diagonal distance max(abs(x-x_goal), abs(y-y_goal)),
		# otherwise use the euclidean distance
		for iHeight in range(len(self.heuristics)):
			for iWidth in range(len(self.heuristics)):
				# Use the diagonal distance as the heuristic function
				if heuristic_function==1:
					self.heuristics[iHeight][iWidth] = max(abs(iHeight-self.goal[0]), abs(iWidth-self.goal[1]))
				else:
					self.heuristics[iHeight][iWidth] = math.sqrt((iHeight-self.goal[0])**2 + (iWidth-self.goal[1])**2)
		return self.heuristics



	def gen_nearest_decided_neighbors(self, Nquery, which_map=1):
		# Get the 8 nearest neighbors to NQuery (i,j)
		# Need each point to be within the boundary
		# | (i-1, j-1) | (i-1, j,) |  (i-1, j+1) |
		# | (i, j-1)   |  (i, j,)  |  (i, j+1)   |
		# | (i+1, j-1) | (i+1, j,) |  (i+1, j+1) |

		if which_map==1:
			the_map = self.map
		else:
			the_map = self.heuristics
		
		# for the given nQuery get the 8 neighbors and their corresponding cost.
		# Send it back in a dictionary maybe with the keys set to the position of the neighbor?
		list_of_neighbors = [[Nquery[0]-1, Nquery[1]-1], [Nquery[0]-1, Nquery[1]], [Nquery[0]-1, Nquery[1]+1],
							[Nquery[0], Nquery[1]-1], [Nquery[0], Nquery[1]+1], 
							[Nquery[0]+1, Nquery[1]-1], [Nquery[0]+1, Nquery[1]], [Nquery[0]+1, Nquery[1]+1]]

		# Loop over all of the neighbors. Check if the neighbor is
		# 1. Defined! (it's not inf)
		# 2. Within the boundary of the map
		nearest_decided_neighbors = []

		for iNeigh in range(len(list_of_neighbors)):
			# Now check if you're within the boundary (0 < index < size_map)
			if (list_of_neighbors[iNeigh][0] >= 0 and list_of_neighbors[iNeigh][0] <= len(the_map) and
			list_of_neighbors[iNeigh][1] >= 0 and list_of_neighbors[iNeigh][1] <= len(the_map[1])):
				# Check if the value is Decided
				if the_map[list_of_neighbors[iNeigh][0]][list_of_neighbors[iNeigh][1]]!=m_v:
					nearest_decided_neighbors.append(list_of_neighbors[iNeigh])
		
		return nearest_decided_neighbors

	def gen_graph(self):
		# also need to define a gen_graph function and set that up based on where the obstacles are
		# the graph is the same size as the map. however it will have m_v's where obstacles are.
		# it will then be passed to the path_planner for use in calculating the total cost of moving
		# to each node?

		print("still writing")

	def path_planner(self):
		# The starting location is always from the row beneath, so our first row
		# will always be the heuristics + cost for the immediate three positions. need to add the 
		# center position to the open list. 

		# Run the path planner while the open set is not empty!
		print("still writiting.")

		

## Things to implement:
# - in the graph, the first row will be 2,1,2 centered at the center of the graph.
# - before we set the first row, we need to check if all three of those locations
# 	are an obstacle. if that's the case then send back an empty list.
# - not sure if i need the nearest neighbors algorithm?
# - 





# Testing Here!
default_map = [
        [0, 0, 0],
        [1, 0, 0],
        [0, 0, 0],
        [0, 1, 0],
        [0, 1, 1],
        [0, 0, 0],
        [0, 1, 0],
        [1, 1, 0]
    ]

big_map = [
    [0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0],
    [0, 0, 1, 0, 0],
    [0, 0, 0, 0, 1],
    [0, 0, 0, 1, 0]]


# Test the Class
p = path_planner(big_map, [3,1])
#print(p.map)
#print(p.graph)
print(p.heuristics)
#print(p.gen_nearest_decided_neighbors([3,1], 0))
t=p.gen_heuristics(0)
for i in range(len(t)):
	print(t[i])


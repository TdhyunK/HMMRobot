#author: Thomas Kim
#date: 11/02/17

from Maze import Maze
from Matrix import Matrix

class hmm_robot():
    
    def __init__(self, maze, num_timesteps):
        self.maze = maze
        self.transition_model = None
        self.sensor_model = None
        self.num_timesteps = num_timesteps
        self.create_sensor_model()
        self.create_transition_model()
        self.init_probability_distribution()

#    def forward(self):
#        i = 0
#        while i <= num_timesteps:
                    

    def init_probability_distribution(self):
        distribution_list = []
        for i in range(self.maze.num_states):
            distribution_list.append([1.0/float(self.maze.num_states)])
        self.maze.probability_distribution = Matrix(distribution_list)
    
    def create_transition_model(self):
        transition_model = [[0 for i in range(self.maze.num_states)] for j in range(self.maze.num_states)]
        for row in range(self.maze.width):
            for col in range(self.maze.height):
                coord_tuple = (row,col)
                if coord_tuple in self.maze.state_dict:
                    row_index = self.maze.state_dict[coord_tuple]
                    neighbor_list = self.maze.find_neighbors(coord_tuple[0], coord_tuple[1])
                    num_walls = 4 - len(neighbor_list)
                    prob_same_loc = num_walls/4.0
                    for neighbor in neighbor_list:
                        col_index = self.maze.state_dict[neighbor]
                        transition_model[row_index][col_index] = 0.25
                    transition_model[row_index][row_index] = prob_same_loc 
        self.transition_model = Matrix(transition_model)

    def create_sensor_model(self):
        wrong_reading = 0.04
        correct_reading = 0.88
        red_sensor = [[0.00 for i in range(self.maze.num_states)] for j in range(self.maze.num_states)]       
        blue_sensor = [[0.00 for i in range(self.maze.num_states)] for j in range(self.maze.num_states)]       
        green_sensor = [[0.00 for i in range(self.maze.num_states)] for j in range(self.maze.num_states)]        
        yellow_sensor = [[0.00 for i in range(self.maze.num_states)] for j in range(self.maze.num_states)]       
        #print("num states: " + str(self.maze.num_states))
        
        for row in range(self.maze.width):        
            for col in range(self.maze.height):
                if((row,col) in self.maze.state_dict):
                    index = self.maze.state_dict[(row,col)] 
        #            print("row,col : " + str((row,col)))
        #            print("index: " + str(index))
                    loc_color = self.maze.get_cell_color(row, col) 
                    if loc_color == "r":
                        red_sensor[index][index] = correct_reading
                        blue_sensor[index][index] = wrong_reading
                        green_sensor[index][index] = wrong_reading
                        yellow_sensor[index][index] = wrong_reading
                    elif loc_color == "g":
                        red_sensor[index][index] = wrong_reading
                        blue_sensor[index][index] = wrong_reading
                        green_sensor[index][index] = correct_reading
                        yellow_sensor[index][index] = wrong_reading
                    elif loc_color == "b":
                        red_sensor[index][index] = wrong_reading 
                        blue_sensor[index][index] = correct_reading
                        green_sensor[index][index] = wrong_reading
                        yellow_sensor[index][index] = wrong_reading
                    elif loc_color == "y":
                        red_sensor[index][index] = wrong_reading 
                        blue_sensor[index][index] = wrong_reading 
                        green_sensor[index][index] = wrong_reading
                        yellow_sensor[index][index] = correct_reading 
        self.sensor_model = [Matrix(red_sensor), Matrix(green_sensor), Matrix(blue_sensor), Matrix(yellow_sensor)]
    
    
test_maze = Maze("maze2.maz")
test = hmm_robot(test_maze, 50)
#test.create_sensor_model() 
#matrix_num = 0
#for matrix in test.sensor_model:
#    print("Matrix num: " + str(matrix_num))
#    print(matrix)
#    matrix_num += 1
#print(test.maze.find_neighbors(1,1))
#print(test.transition_model)
print(test.maze)

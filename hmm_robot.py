#author: Thomas Kim
#date: 11/02/17

from Maze import Maze
from Matrix import Matrix
from random import uniform
from time import sleep

class hmm_robot():
    
    def __init__(self, maze, num_timesteps):
        self.maze = maze
        #By default transition model is transposed
        self.transition_model = None
        self.sensor_model = None
        self.num_timesteps = num_timesteps
        self.create_sensor_model()
        self.create_transition_model()
        self.init_probability_distribution()

    def forward(self, color):
        sensor_model = None
        if color == "r":
            sensor_model = self.sensor_model[0]
        elif color == "g":
            sensor_model = self.sensor_model[1]
        elif color == "b":
            sensor_model = self.sensor_model[2]
        elif color == "y":
            sensor_model = self.sensor_model[3]
       # print("sensor model \n" + str(sensor_model))
       # print("transition model \n" + str(self.transition_model))
       # print("probability distribution \n" + str(self.maze.probability_distribution))
        self.maze.probability_distribution = sensor_model.multiply_matrix(self.transition_model).multiply_matrix(self.maze.probability_distribution)
        print("NOT NORMALIZED DISTRIBUTION: " + str(self.maze.probability_distribution))
        self.maze.probability_distribution.normalize()   
        print("NORMALIZED DISTRIBUTION: " + str(self.maze.probability_distribution))
 
    def random_move_decision(self, probability):
        if probability >= 0.00 and probability <= 0.25:
            return "r"
        elif probability >= 0.26 and probability <= 0.50:
            return "l"
        elif probability >= 0.51 and probability <= 0.75:
            return "u"
        elif probability >= 0.76 and probability <= 1.00:
            return "d"
  
    def generate_random_moves(self):
        robot_x = self.maze.robotloc[0]
        robot_y = self.maze.robotloc[1]
        robot_loc_list = []
        i = 0
        while i <= self.num_timesteps:
            probability = uniform(0,1)
            move = self.random_move_decision(probability) 
            if move == "r":
                if self.maze.valid_coord(robot_x + 1, robot_y) and self.maze.map[self.maze.position_dict[self.maze.index(robot_x + 1, robot_y)]] != "#":
                    robot_x = robot_x + 1
                else:
                    robot_x
            elif move == "l":
                if self.maze.valid_coord(robot_x - 1, robot_y) and self.maze.map[self.maze.position_dict[self.maze.index(robot_x - 1, robot_y)]] != "#":
                    robot_x = robot_x - 1
                else:
                    robot_x
            elif move == "u":
                if self.maze.valid_coord(robot_x, robot_y + 1) and self.maze.map[self.maze.position_dict[self.maze.index(robot_x, robot_y + 1)]] != "#":
                    robot_y = robot_y + 1 
                else:
                    robot_y
            elif move == "d":
                if self.maze.valid_coord(robot_x, robot_y - 1) and self.maze.map[self.maze.position_dict[self.maze.index(robot_x, robot_y - 1)]] != "#":
                    robot_y = robot_y - 1
                else: 
                    robot_y
            robot_loc_list.append([robot_x, robot_y]) 
            i += 1
        return robot_loc_list             

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
        self.transition_model.transpose()
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

    def read_color(self, actual_color):
        full_color_list = ["r", "g", "b", "y"]
        full_color_list = [color for color in full_color_list if color is not actual_color]
        random_probability = round(uniform(0,1), 2)
        print("random probability: " + str(random_probability))
        if random_probability <= 0.88:
            return actual_color
        elif random_probability >= 0.89 and random_probability <= 0.92:
            return full_color_list[0]
        elif random_probability >= 0.93 and random_probability <= 0.96:
            return full_color_list[1]
        elif random_probability >= 0.97 and random_probability <= 1.00:
            return full_color_list[2]
    
    def animate_path(self, path):
        print(str(self.maze))
        for location in path:
            self.maze.robotloc = location
            actual_color = self.maze.map[self.maze.position_dict[self.maze.index(location[0], location[1])]]
            print("actual color: " + str(actual_color))
            read_color = self.read_color(actual_color) 
            print("read color: " + str(read_color))
            self.forward(read_color)
            sleep(1)
            print(str(self.maze))
    
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
random_move_list = test.generate_random_moves()
print("random move list: \n" + str(random_move_list))
test.animate_path(random_move_list)

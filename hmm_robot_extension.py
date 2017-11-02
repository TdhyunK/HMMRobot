#author: Thomas Kim
#date: 11/02/17

from Maze import Maze
from Matrix import Matrix
from random import uniform
import curses
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
        """
        Implement forward inference on the maze.
        @param: color: color of the sensor to perform forward calculation
        """
        sensor_model = None
        if color == "r":
            sensor_model = self.sensor_model[0]
        elif color == "g":
            sensor_model = self.sensor_model[1]
        elif color == "b":
            sensor_model = self.sensor_model[2]
        elif color == "y":
            sensor_model = self.sensor_model[3]
        self.maze.probability_distribution = sensor_model.multiply_matrix(self.transition_model).multiply_matrix(self.maze.probability_distribution)
        self.maze.probability_distribution.normalize()   
 
    def init_probability_distribution(self):
        """
        Initialize the probability distribution of the maze
        """
        distribution_list = []
        for i in range(self.maze.num_states):
            distribution_list.append([1.0/float(self.maze.num_states)])
        self.maze.probability_distribution = Matrix(distribution_list)
    
    def create_transition_model(self):
        """
        Create the transition model of the maze.
        By default, transpose the transition model.
        """
        transition_model = [[0 for i in range(self.maze.num_states)] for j in range(self.maze.num_states)]
        for row in range(self.maze.width):
            for col in range(self.maze.height):
                coord_tuple = (row,col)
               #if coord_tuple is a valid state
                if coord_tuple in self.maze.state_dict:
                    row_index = self.maze.state_dict[coord_tuple]
                    neighbor_list = self.maze.find_neighbors(coord_tuple[0], coord_tuple[1])
                    num_walls = 4 - len(neighbor_list)
                    prob_same_loc = num_walls/4.0
                    for neighbor in neighbor_list:
                        #update transition model with probability of 25%
                        col_index = self.maze.state_dict[neighbor]
                        transition_model[row_index][col_index] = 0.25
                    transition_model[row_index][row_index] = prob_same_loc 
        self.transition_model = Matrix(transition_model)
        self.transition_model.transpose()

    def create_sensor_model(self):
        """
        Create the sensor model of the maze.
        """
        wrong_reading = 0.04
        correct_reading = 0.88
        red_sensor = [[0.00 for i in range(self.maze.num_states)] for j in range(self.maze.num_states)]       
        blue_sensor = [[0.00 for i in range(self.maze.num_states)] for j in range(self.maze.num_states)]       
        green_sensor = [[0.00 for i in range(self.maze.num_states)] for j in range(self.maze.num_states)]        
        yellow_sensor = [[0.00 for i in range(self.maze.num_states)] for j in range(self.maze.num_states)]       
        
        for row in range(self.maze.width):        
            for col in range(self.maze.height):
                if((row,col) in self.maze.state_dict):
                    index = self.maze.state_dict[(row,col)] 
                    loc_color = self.maze.get_cell_color(row, col) 
                    #depending on the color of the location
                    #update the correct sensor model
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
        """
        Read the color at a certain location.
        @param: actual_color: correct color to read and return
        """

        full_color_list = ["r", "g", "b", "y"]
        full_color_list = [color for color in full_color_list if color is not actual_color]
        random_probability = round(uniform(0,1), 2)
        #Depending on the probability, return either the correct or incorrect color
        if random_probability <= 0.88:
            return actual_color
        elif random_probability >= 0.89 and random_probability <= 0.92:
            return full_color_list[0]
        elif random_probability >= 0.93 and random_probability <= 0.96:
            return full_color_list[1]
        elif random_probability >= 0.97 and random_probability <= 1.00:
            return full_color_list[2]
    
    def animate_path(self):
        """
        Animate the path given user input
        """
        while(True):
            move = raw_input("Enter which direction you want to move and press enter.")
            robot_x = self.maze.robotloc[0]
            robot_y = self.maze.robotloc[1]
            if move == "\x1b[C":
                if self.maze.valid_coord(robot_x + 1, robot_y) and self.maze.map[self.maze.position_dict[self.maze.index(robot_x + 1, robot_y)]] != "#":
                    robot_x = robot_x + 1
                else:
                    robot_x
            elif move == "\x1b[D":
                if self.maze.valid_coord(robot_x - 1, robot_y) and self.maze.map[self.maze.position_dict[self.maze.index(robot_x - 1, robot_y)]] != "#":
                    robot_x = robot_x - 1
                else:
                    robot_x
            elif move == "\x1b[A":
                if self.maze.valid_coord(robot_x, robot_y + 1) and self.maze.map[self.maze.position_dict[self.maze.index(robot_x, robot_y + 1)]] != "#":
                    robot_y = robot_y + 1 
                else:
                    robot_y
            elif move == "\x1b[B":
                if self.maze.valid_coord(robot_x, robot_y - 1) and self.maze.map[self.maze.position_dict[self.maze.index(robot_x, robot_y - 1)]] != "#":
                    robot_y = robot_y - 1
                else: 
                    robot_y
            self.maze.robotloc = [robot_x, robot_y]    
            actual_color = self.maze.map[self.maze.position_dict[self.maze.index(robot_x, robot_y)]]
            print("actual color: " + str(actual_color))
            read_color = self.read_color(actual_color)
            print("read color: " + str(read_color))
            self.forward(read_color)
            sleep(1)
            print(str(self.maze))
    


test_maze = Maze("maze2.maz")
#test_maze = Maze("maze1.maz")
test = hmm_robot(test_maze, 50)
test.animate_path()

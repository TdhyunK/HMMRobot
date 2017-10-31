#author: Thomas Kim
#date: 11/0.002/17

from Maze import Maze
from Matrix import Matrix

class hmm_robot():
    
    def __init__(self, maze):
        self.maze = maze
        self.transition_model = None
        self.sensor_model = None
        self.probability_distribution = None
        self.create_sensor_model()
   #     self.create_transition_model()

   # def create_transition_model(self):
   #     transition_model = [[0 for i in range(self.maze.num_states)] for j in range(self.maze.num_states)]
   #     for row in range(self.maze.width):
   #         for col in range(self.maze.mheight):
   #             coord_tuple = (row,col)
   #             if coord_tuple in self.maze.state_dict:
                    

    def create_sensor_model(self):
        wrong_reading = "0.04"
        correct_reading = "0.88"
        red_sensor = [["0.00" for i in range(self.maze.num_states)] for j in range(self.maze.num_states)]       
        blue_sensor = [["0.00" for i in range(self.maze.num_states)] for j in range(self.maze.num_states)]       
        green_sensor = [["0.00" for i in range(self.maze.num_states)] for j in range(self.maze.num_states)]        
        yellow_sensor = [["0.00" for i in range(self.maze.num_states)] for j in range(self.maze.num_states)]       
        print("num states: " + str(self.maze.num_states))
        
        for row in range(self.maze.width):        
            for col in range(self.maze.height):
                if((row,col) in self.maze.state_dict):
                    index = self.maze.state_dict[(row,col)] 
                    print("row,col : " + str((row,col)))
                    print("index: " + str(index))
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
test = hmm_robot(test_maze)
test.create_sensor_model() 
matrix_num = 0
#for matrix in test.sensor_model:
#    print("Matrix num: " + str(matrix_num))
#    print(matrix)
#    matrix_num += 1
print(test.maze.find_neighbors(1,1))

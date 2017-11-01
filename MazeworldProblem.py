#Author: Thomas Kim
#Date: 9/27/17
#Class: CS76 17F

from Maze import Maze
from time import sleep
from hmm_robot import hmm_robot
class MazeworldProblem:

    #Mazeworld Constructor
    def __init__(self, maze, start_robot=0):
        self.maze = maze
        startList = []
        startList.append(0)
        for location in maze.robotloc:
            startList.append(location)
        self.start_state = tuple(startList)
        self.num_robots = int((len(startList) / 2))
        
    #Returns string representation of the Mazeworld Problem.
    def __str__(self):
        string =  "Mazeworld problem: "
        return string

    # given a sequence of states (including robot turn), modify the maze and print it out.
    #  (Be careful, this does modify the maze!)
    def animate_path(self, path):
        # reset the robot locations in the maze
        self.maze.robotloc = tuple(self.start_state[1:])

        for state in path:
            print(str(self))
            self.maze.robotloc = tuple(state[1:])
            sleep(1)

            print(str(self.maze))

    #Update robot location list 
    def update_robot_loc(self, locations):
        self.maze.robotloc = locations

## A bit of test code. You might want to add to it to verify that things
#  work as expected.

if __name__ == "__main__":
    test_maze2 = Maze("maze2.maz")
    test_hmm = hmm_robot(test_maze2, 10)
    random_move_list = test_hmm.generate_random_moves()
    print("random move list: \n" + str(random_move_list))
   test_hmm.animate_path(random_move_list)

#Author: Thomas Kim
#Date: 9/27/17
#Class: CS76 17F

from time import sleep

# Maze.py
#  original version by db, Fall 2017
#  Feel free to modify as desired.

# Maze objects are for loading and displaying mazes, and doing collision checks.
#  They are not a good object to use to represent the state of a robot mazeworld search
#  problem, since the locations of the walls are fixed and not part of the state;
#  you should do something else to represent the state. However, each Mazeworldproblem
#  might make use of a (single) maze object, modifying it as needed
#  in the process of checking for legal moves.

# Test code at the bottom of this file shows how to load in and display
#  a few maze data files (e.g., "maze1.maz", which you should find in
#  this directory.)

#  the order in a tuple is (x, y) starting with zero at the bottom left

# Maze file format:
#    # is a wall
#    . is a floor
# the command \robot x y adds a robot at a location. The first robot added
# has index 0, and so forth.


class Maze:

    # internal structure:
    #   self.walls: set of tuples with wall locations
    #   self.width: number of columns
    #   self.rows

    # index in with (row, column), IN THAT ORDER. row starts with 0 at the
    # top. Column index starts at 0, left side.


    def __init__(self, mazefilename):

        self.robotloc = []
        self.num_states = 0
        self.state_dict = {}
        # read the maze file into a list of strings
        f = open(mazefilename)
        lines = []
        for line in f:
            line = line.strip()
            # ignore blank limes
            if len(line) == 0:
                pass
            elif line[0] == "\\":
                #print("command")
                # there's only one command, \robot, so assume it is that
                parms = line.split()
                x = int(parms[1])
                y = int(parms[2])
                self.robotloc.append(x)
                self.robotloc.append(y)
            else:
                lines.append(line)
                for position in line:
                    if position == "r" or position == "g" or position == "b" or position == "y":
                        self.num_states += 1
        self.position_dict = {}
        f.close()
        self.width = len(lines[0]) - len(lines[0])/2
        self.height = len(lines)
        self.map = list("".join(lines))
        self.probability_distribution = None 
        self.init_position_dict()
        self.init_state_dict()
        print("robot loc: " + str(self.robotloc))

    def index(self, x, y):
        """
        Return the index of the coordinate.
        @param: x: x-coordinate
        @param: y: y-coordinate
        """
        return (self.height - y - 1) * self.width + x
    
    def init_state_dict(self):
        """
        Map every non-walled location to an index
        beginning from top left to bottom right
        """
        state_num = 0
        for y in range(self.height-1, -1, -1):
            for x in range(self.width):
                if self.get_cell_color(x,y) != "#":
                    self.state_dict[(x,y)] = state_num
                    state_num += 1

    def get_cell_color(self, x, y):
        """
        Return the color of the cell
        @param: x: x coordinate of the cell
        @param: y: y coordinate of the cell
        """
        return self.map[self.position_dict[self.index(x,y)]]

    def valid_coord(self,x,y):
        if x < 0 or x >= self.width:
            return False
        if y < 0 or y >= self.height:
            return False
        return True 

    # returns True if the location is a floor
    def is_floor(self, x, y):
        if valid_cooord:
            return self.map[self.index(x, y)] != "#"
        return False


    def has_robot(self, x, y):
        if x < 0 or x >= self.width:
            return False
        if y < 0 or y >= self.height:
            return False

        for i in range(0, len(self.robotloc), 2):
            rx = self.robotloc[i]
            ry = self.robotloc[i + 1]
            if rx == x and ry == y:
                return True

        return False

    def init_position_dict(self):
        """
        Map every position (walls and non walls) into an index
        """
        map_list = list(self.map)
        matrix_cell = 0
        for i in range(len(map_list)):
            if map_list[i] != " ":
                self.position_dict[matrix_cell] = i
                matrix_cell += 1

    # function called only by __str__ that takes the map and the
    #  robot state, and generates a list of characters in order
    #  that they will need to be printed out in.
    def create_render_list(self, type=None):
        renderlist = list(self.map)
        robot_number = 0
        for index in range(0, len(self.robotloc), 2):

            x = self.robotloc[index]
            y = self.robotloc[index + 1]

            robot_index = self.index(x,y)
            renderlist[self.position_dict[robot_index]] = (renderlist[self.position_dict[robot_index]], "robot")
            #Create tuple with robot in it.
            #renderlist[self.index(x, y)] = (renderlist[self.index(x,y)],"robot")
            if(type == None):
                robot_number += 1
        return renderlist

    def find_neighbors(self, x, y):
        """
        Find the four valid neighbors in the cardinal 
        direction (north, south, east, west) of the location.
        @param: x: x-coordinate of the location
        @param: y: y-coordinate of the location
        """
        north_coord = (x, y + 1) if self.valid_coord(x, y + 1) else None 
        east_coord = (x + 1, y) if self.valid_coord(x + 1, y) else None
        south_coord = (x, y - 1) if self.valid_coord(x, y-1) else None
        west_coord = (x - 1, y) if self.valid_coord(x - 1, y) else None
        curr_coord = (x,y)

        coord_list = [north_coord, east_coord, south_coord, west_coord]
        coord_list = [coord for coord in coord_list if coord is not None and self.map[self.position_dict[self.index(coord[0], coord[1])]] is not "#"]

        return coord_list 

    def full_color(self, color_abbreviation):
        """
        Return the full word of a call given the abbreviation
        @paaram: color_abbreviation: first letter of the color
        """
        return{
            "r": "red",
            "b": "blue",
            "g": "green",
            "y": "yellow",
            "#": "#"
        }[color_abbreviation]          

    def __str__(self):
        renderlist = self.create_render_list()

        s = ""
        prev_val = ""
        index_list = []
        for i in range(len(renderlist)):
            if renderlist[i] != " ":
                index_list.append(i)


        start_index = 0
        end_index = len(index_list) 
        prob_distrib_index = 0
        while start_index < end_index:
            robot_start_index = start_index
            color_start_index = start_index
            prob_start_index = start_index
            sub_list_end_index = start_index + self.width 
            s += ("-" * 20) * self.width + "\n"
            s += "-                  -" * self.width + "\n"
            while color_start_index < sub_list_end_index:
                is_tuple = False
                curr_val = renderlist[self.position_dict[color_start_index]]
                if type(curr_val) == tuple:
                    is_tuple = True
                    num_color_spaces = 20 - len(self.full_color(curr_val[0])) + 1
                else:
                    num_color_spaces = 20 - len(self.full_color(str(curr_val))) + 1
                s += "-" + " " * (num_color_spaces/2-1)
                s += self.full_color(curr_val[0]) if is_tuple else self.full_color(str(curr_val))
                s += " " * (num_color_spaces - num_color_spaces/2-2) + "-"
                color_start_index += 1
            s += "\n"
            while robot_start_index < sub_list_end_index:
                curr_val = renderlist[self.position_dict[robot_start_index]]
                is_tuple = True if type(curr_val) == tuple else False
                if is_tuple:
                    num_robot_spaces = 20 - len(curr_val[1])
                    s += "-" + " " * (num_robot_spaces/2 - 1)
                    s += curr_val[1]
                    s += " " * (num_robot_spaces/2) + "-"
                else:
                    s += "-" + " " * 18 + "-"
                robot_start_index += 1
            s += "\n"
            if self.probability_distribution is not None:
                while prob_start_index < sub_list_end_index:
                    curr_val = renderlist[self.position_dict[prob_start_index]]
                    is_tuple = True if type(curr_val) == tuple else False
                    curr_val = curr_val[0] if is_tuple else curr_val
                    if curr_val == "#": 
                        s += "-" + " " * 18 + "-"
                    else:
                        num_prob_spaces = 14 #20 spaces - 6 (xx.xx%)
                        print("PROBABILITY: " + str(self.probability_distribution.matrix[prob_distrib_index][0] * 100))
                        s += "-" + " " * (num_prob_spaces/2-1)
                        s += "%.2f" % (self.probability_distribution.matrix[prob_distrib_index][0] * 100)     
                        s += "%" + " " * (num_prob_spaces/2) + "-"     
                        prob_distrib_index += 1
                    prob_start_index += 1
                s += "\n"             
            start_index = sub_list_end_index 
        s += "-" * 20 * self.width
        return s  

def robotchar(robot_number):
   return chr(ord("A") + robot_number)


# Some test code

if __name__ == "__main__":
#    test_maze1 = Maze("maze1.maz")
    test_maze2 = Maze("maze2.maz")
#    print(test_maze1.map)
#    print(test_maze1.create_render_list())
#    print(test_maze1)
    print(test_maze2)
    print(test_maze2.create_render_list())
    print(test_maze2.position_dict)

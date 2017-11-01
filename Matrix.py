#Author: Thomas Kim
#Date: 11/2/17

class Matrix():
    """
    Create a Matrix class to represent a 2D list as a matrix.
    """
    
    def __init__(self, matrix):
        """
        Matrix constructor
        @param: matrix: 2D list representation of a matrix.
        """
        self.matrix = matrix

    def transpose(self):
        """
        Transpose the matrix.
        """
        transpose_list = [[0 for i in range(len(self.matrix[0]))] for j in range(len(self.matrix))]
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                transpose_list[j][i] = self.matrix[i][j]
               
        print("TRANSPOSED LIST: " + str(transpose_list))
        self.matrix = transpose_list
 
    def multiply_matrix(self, matrix_multiplier):
        """
        Multiple the matrix by matrix_multiplier
        @param: matrix_multiplier: Matrix object to multiply the matrix by.
        """
        multiplied_matrix = [[0 for i in range(len(matrix_multiplier.matrix[0]))] for j in range(len(self.matrix))] 
        if len(self.matrix[0]) == len(matrix_multiplier.matrix):
            for i in range(len(self.matrix)):
                for j in range(len(matrix_multiplier.matrix[0])):
                    for k in range(len(matrix_multiplier.matrix)):
                        multiplied_matrix[i][j] += self.matrix[i][k] * matrix_multiplier.matrix[k][j]
        new_matrix = Matrix(multiplied_matrix)
        return new_matrix
                    
    def __str__(self):
        """
        Return a string representation of the matrix.
        """
        return_string = ""
        for i in range(len(self.matrix)):
            return_string += str(self.matrix[i]) + "\n"
        return return_string       
    
    def normalize(self):
        for col in range(len(self.matrix[0])): 
            check_sum = 0
            curr_sum = 0
            for row in range(len(self.matrix)): 
                curr_sum += self.matrix[row][col]   
            for row in range(len(self.matrix)): 
                self.matrix[row][col] = self.matrix[row][col]/float(curr_sum)
                check_sum += self.matrix[row][col]
            print("check sum: " + str(check_sum))
                
matrixA = [[1,2,3],[4,5,6],[7,8,9],[10,11,12]]
matrixB = [[2],[1],[0]] 
testA = Matrix(matrixA)
testB = Matrix(matrixB)
#print(testA.multiply_matrix(testB))
testB.normalize()
print(testB)

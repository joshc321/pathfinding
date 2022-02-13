from collections import deque
import numpy, random

class RandomPrim:
    
    #coord (x,y) (col, row) (width, height)  format (row, col)
    def __init__(self, win: 'pygcurse.PygcurseWindow', rows: int, cols: int, visualize: bool=False) -> None:
        self.win = win
        self.rows = rows
        self.cols = cols
        self.maze = numpy.ones([rows, cols])
        self.walls = set() #deque()

    def valid_wall(self,row: int, col: int) -> bool:
        '''
        Given a row and a col returns true if the values are in the grid
        and the value is a wall in the maze
        '''
        return (1 <= row < self.rows - 1) and (1 <= col < self.cols - 1) and self.maze[row][col] == 1

    def valid_path(self, row: int, col: int) -> bool:
        '''
        Given a row and a col returns true if the values are in the grid
        and the value is a path in the maze
        '''
        return (0 <= row < self.rows) and (0 <= col < self.cols) and (col < self.cols) and self.maze[row][col] == 0

    def get_walls(self, row: int, col: int) -> tuple:
        '''
        returns a tuple generator of tuples of valid walls
        around a grid value
        '''
        rows = [-1,0,0,1]
        cols = [0,-1,1,0]
        return ((row + rows[i], col + cols[i]) for i in range(len(rows)) if self.valid_wall(row + rows[i], col + cols[i]))

    def add_neighboring_walls(self, row, col):
        '''
        given a row, col adds the surrounding walls
        to the set of walls
        '''
        for coord in self.get_walls(row, col):
            self.walls.add(coord) # (col, row)

    def num_visited(self, row: int, col: int) -> int:
        '''
        given a row, col returns the number of visited
        grids around the cell
        '''
        return len(self.surrounding_paths(row, col))

    def surrounding_paths(self, row: int, col: int) -> list:
        '''
        given a row, col returns a list of paths surrounding
        the given cell
        '''
        rows = [-1,0,0,1]
        cols = [0,-1,1,0]
        return [(row + rows[i], col + cols[i]) for i in range(len(rows)) if self.valid_path(row + rows[i], col + cols[i])]

    def passage(self, row: int, col: int) -> tuple:
        '''
        returns a (col,row) tuple of the unvisited cell that the wall divides
        '''
        base_path = self.surrounding_paths(row, col)
        assert len(base_path) == 1, 'RandomePrim.passage: there should only be one path'
        base_path = base_path[0]
        dir = [base_path[0] - row, base_path[1] - col]
        new_passage = (row + -dir[0], col + -dir[1])
        return new_passage if self.valid_wall(*new_passage) else None

    def walls_set(self) -> set:
        '''
        returns a set of the current walls in the maze in 
        the form of tuples (col, row)
        '''
        return {(col, row) for row in range(self.rows) for col in range(self.cols) if self.maze[(row,col)] == 1}

    def prims(self) -> None:
        '''
        Performs a Randomized Prim's algorithm on the maze grid
        running until it has no more valid walls
        '''
        start_cell = (random.randint(1, self.rows-2), 0)
        self.maze[start_cell] = 0
        #self.win.write('O', *start_cell, fgcolor='blue')
        self.add_neighboring_walls(*start_cell)

        while self.walls:
            rand_wall = self.walls.pop()
            if self.num_visited(*rand_wall) == 1:
                if unvisited_cell := self.passage(*rand_wall):
                    self.maze[rand_wall] = 0
                    self.maze[unvisited_cell] = 0
                    #self.win.write('O', *rand_wall, fgcolor='blue')
                    #self.win.write('O', *unvisited_cell, fgcolor='blue')
                    self.add_neighboring_walls(*unvisited_cell)
            



if __name__ == '__main__':
    class test:
        def write(a,*b, fgcolor=''):
            pass
    prim = RandomPrim(test, 10,10)
    prim.prims()
    print(prim.maze)
    print(prim.walls)
    print(prim.walls_set())
    


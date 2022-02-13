#randomized depth first maze generation

from collections import deque
import random
from board import Board, BoardOptions
from settings import settings

class RandomDepthFirst:
    
    def __init__(self, board: Board, visual = None, multiplier = settings['multiplier']) -> None:
        self._board = board
        self.stack = deque()
        self._board.fill(BoardOptions().wall)
        self.visual = visual
        self.multiplier = multiplier

    def valid_wall(self,row: int, col: int) -> bool:
        '''
        Given a row and a col returns true if the values are in the grid
        and the value is a wall in the maze
        '''
        return self._board.is_valid_pos((row, col)) and self._board[row,col] == BoardOptions().wall

    def get_walls(self, row: int, col: int) -> tuple:
        '''
        returns a tuple generator of tuples of valid walls
        around a grid value
        '''
        rows = [-1,0,0,1]
        cols = [0,-1,1,0]
        return ((row + rows[i], col + cols[i]) for i in range(len(rows)) if self.valid_wall(row + rows[i], col + cols[i]))

    def get_random_neighbor(self, row: int, col: int) -> tuple:
        'returns a random valid neighboring cell'
        unvisited_neighbors = []
        for neighbor in self.get_walls(row, col):
            dir = (neighbor[0] - row, neighbor[1] - col)
            if self.available(dir, *neighbor):
                unvisited_neighbors.append(neighbor)
        random.shuffle(unvisited_neighbors)
        return unvisited_neighbors[0] if unvisited_neighbors else None

    def available(self, dir, row: int, col: int) -> bool:
        '''
        returns true if cell reached from direction dir is not touching
        any other paths
        '''
        #dirs = [(-1,0), (0,-1), (0,1), (1,0)]
        def ignore_vals(dir):
            row, col = dir
            if row != 0:
                return [(-row, col), (-row,row), (-row, -row)]
            else:
                return [(row, -col), (col, -col), (-col, -col)]

        rows = [-1,0,0,1,1,1,-1,-1]
        cols = [0,-1,1,0,1,-1,1,-1]

        return all(self._board[row + rows[i], col + cols[i]] == 1 for i in range(len(rows))
         if (rows[i], cols[i]) not in ignore_vals(dir) and self._board.is_valid_pos((row + rows[i], col + cols[i])))


    def depth(self) -> None:
        '''
        Performs a Randomized Depth First algorithm on the maze grid
        running until it has no more valid walls
        '''
        start_cell = (random.randint(1, self._board.size()[0]-2), 0)
        self._board[start_cell] = BoardOptions().path
        self.stack.append(start_cell)
        count = 0
        while self.stack:
            cell = self.stack.pop()
            if unvisited_cell := self.get_random_neighbor(*cell):
                self.stack.append(cell)
                self._board[unvisited_cell] = BoardOptions().path

                if count % self.multiplier == 0 and self.visual != None:
                    self.visual._handle_events()
                    self.visual._draw_frame()
                    count = 0
                count += 1
                self.stack.append(unvisited_cell)
            



if __name__ == '__main__':
    board = Board(10,10, True)
    rdf = RandomDepthFirst(board)
    #board[0,6] = 0
    rdf.depth()
    #print(board)
    #print(rdf.available((-1,0), 1,6))
    #board[1,6] = 0
    print(board)

'''
(r,c)

(-1,0)
Ignore: 
(1,0)   (-r, c)
(1,-1)  (-r,r)
(1,1)   (-r,-r)

(1,0)
Ignore: 
(-1,0)  (-r, c)
(-1,1)  (-r,r)
(-1,-1) (-r,-r)

(0,1)
Ignore:
(0,-1)  (r, -c)
(1,-1)  (c, -c)
(-1,-1) (-c,-c)

(0,-1)
Ignore:
(0,1)   (r, -c)
(-1,1)  (c, -c)
(1,1)   (-c, -c)
'''

import random
from board import Board, BoardOptions
from settings import settings

class RandomPrim:
    
    def __init__(self, board: Board, visual = None, multiplier = settings['multiplier']) -> None:
        self._board = board
        self.walls = [] # set() #deque()
        self._board.fill(BoardOptions().wall)
        self.visual = visual
        self.multiplier = multiplier

    def valid_wall(self,row: int, col: int) -> bool:
        '''
        Given a row and a col returns true if the values are in the grid
        and the value is a wall in the maze
        '''
        return self._board.is_valid_pos((row, col)) and self._board[row,col] == BoardOptions().wall

    def valid_path(self, row: int, col: int) -> bool:
        '''
        Given a row and a col returns true if the values are in the grid
        and the value is a path in the maze
        '''
        return self._board.is_valid_pos((row, col)) and self._board[row,col] == BoardOptions().path

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
            self.walls.append(coord) 

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


    def prims(self) -> None:
        '''
        Performs a Randomized Prim's algorithm on the maze grid
        running until it has no more valid walls
        '''
        start_cell = (random.randint(1, self._board.size()[0]-2), 0)
        self._board[start_cell] = BoardOptions().path
        self.add_neighboring_walls(*start_cell)

        count = 0

        while self.walls:
            rand_wall = self.walls.pop(random.randrange(len(self.walls)))
            if self.num_visited(*rand_wall) == 1:
                if unvisited_cell := self.passage(*rand_wall):
                    self._board[rand_wall] = BoardOptions().path
                    self._board[unvisited_cell] = BoardOptions().path
    
                    if count % self.multiplier == 0 and self.visual != None:
                        self.visual._handle_events()
                        self.visual._draw_frame()
                        count = 0
                    count += 1
                    self.add_neighboring_walls(*unvisited_cell)
            



if __name__ == '__main__':
    board = Board(10,10, True)
    prim = RandomPrim(board)
    prim.prims()
    print(prim._board)
    


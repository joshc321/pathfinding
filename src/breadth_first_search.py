from collections import deque
import numpy
from board import Board, BoardOptions

class PathNotFound(Exception):
    pass

class BFS: 

    def __init__(self, board: Board, start: tuple, goal: tuple) -> None:
        self._board = board
        self.start = start
        self.goal = goal
        self._visited = numpy.zeros(self._board.size())

    def reconstruct_path(self, cameFrom: dict, current: set) -> dict:
        '''
        Given a dictionary of paths and a current value returns a set
        of the reconstruced path from its origin
        '''
        total_path = {current}
        while current != self.start:
            current = cameFrom[current]
            total_path.add(current)
            self._board[current] = BoardOptions().route
        self._board[self.start] = BoardOptions().start_end
        return total_path

    def is_valid(self,row: int, col: int) -> bool:
        '''
        given a row and an int returns true if the position
        is valid for the current board and is a path and not
        visited
        '''
        return self._board.is_valid_pos((row, col)) and self._board[row,col] != BoardOptions().wall \
            and not self._visited[row, col]

    def neighbors(self,row: int, col: int) -> tuple:
        '''
        returns a tuple generator of tuples of the neighbors for
        the given int/row
        '''
        #rows = [-1,0,0,1,1,-1,1,-1]
        #cols = [0,-1,1,0,1,-1,-1,1]
        rows = [-1,0,0,1]
        cols = [0,-1,1,0]
        return ((row + rows[i], col + cols[i]) for i in range(len(rows)) if self.is_valid(row + rows[i], col + cols[i]))

    def bfs(self) -> None:
        '''
        Breadth first search pathfinding algorithm on the grid given,
        finds the optimal path
        '''
        s = deque()
        s.append(self.start)

        came_from = {}

        while s:
            v = s.popleft()
            if v == self.goal:
                return self.reconstruct_path(came_from, v)
            
            for neighbor in self.neighbors(*v):
                came_from[neighbor] = v
                self._visited[neighbor] = 1
                s.append(neighbor)

                        

        raise PathNotFound


if __name__ == '__main__':
    m = Board(10,10)
    m[9,0]=1
    m[8,1] = 1
    m[7,2] = 1
    print(m)
    BFS(m, (0,0), (8,8)).bfs()
    print(m)
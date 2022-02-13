from queue import PriorityQueue
from collections import defaultdict

from board import Board, BoardOptions

class PathNotFound(Exception):
    pass

class Astar: 

    def __init__(self, board: Board, start: tuple, goal: tuple) -> None:
        self._board = board
        self.start = start
        self.goal = goal

    def reconstruct_path(self, cameFrom: dict, current: set) -> dict:
        '''
        Given a dictionary of paths and a current value returns a set
        of the reconstruced path from its origin
        '''
        total_path = {current}
        while current in cameFrom:
            current = cameFrom[current]
            total_path.add(current)
            self._board[current] = BoardOptions().route
        self._board[self.start] = BoardOptions().start_end
        return total_path

    def is_valid(self,row: int, col: int) -> bool:
        '''
        given a row and an int returns true if the position
        is valid for the current board and is a path
        '''
        return self._board.is_valid_pos((row, col)) and self._board[row,col] != BoardOptions().wall

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

    def h(self,x1: int, y1: int, x2: int, y2: int) -> int:
        '''
        heuristic function (Manhattan distance)
        '''
        #return math.sqrt((x2-x1)**2 + (y2-y1)**2)
        return abs(x1 - x2) + abs(y1 - y2)

    def astar(self) -> None:
        '''
        Astar pathfinding algorithm on the grid given,
        finds the optimal path
        '''
        open_set = PriorityQueue()
        open_set.put((0, self.start))
        
        open_set_hash = {self.start}

        came_from = {}
        gScore = defaultdict(lambda: float('inf'))
        gScore[self.start] = 0

        fScore = defaultdict(lambda: float('inf'))
        fScore[self.start] = self.h(*self.start, *self.goal)

        while not open_set.empty():
            current = open_set.get()[1]
            
            if current == self.goal:
                return self.reconstruct_path(came_from, current)
            open_set_hash.remove(current)
            for neighbor in self.neighbors(*current):
                tentative_Gscore = gScore[current] + 1
                if tentative_Gscore < gScore[neighbor]:
                    came_from[neighbor] = current
                    gScore[neighbor] = tentative_Gscore
                    fScore[neighbor] = tentative_Gscore + self.h(*neighbor, *self.goal)
                    if neighbor not in open_set_hash:
                        open_set_hash.add(neighbor)
                        open_set.put((fScore[neighbor],neighbor))
                        

        raise PathNotFound
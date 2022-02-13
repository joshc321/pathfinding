from ast import Raise
from queue import PriorityQueue
import numpy
from collections import defaultdict
import multiprocessing

class PathNotFound(Exception):
    pass

class Astar: 

    def __init__(self, win: 'pygcurse.PygcurseWindow', start: tuple, goal: tuple, wall, rows: int, cols: int) -> None:
        self.win = win
        self.rows = rows
        self.cols = cols
        self.start = start
        self.goal = goal
        self._setup_walls(wall)
        
    
    def _setup_walls(self, wall) -> None:
        '''
        converts the inputted walls into 
        '''
        if type(wall) is set:
            self.walls = numpy.zeros([self.rows,self.cols])
            for i in wall:
                self.walls[i] = 1
        elif type(wall) is numpy.ndarray:
            self.walls = wall
        else:
            raise TypeError(f'Unsupported Type: \'{type(wall)}\'')

    def reconstruct_path(self, cameFrom: dict, current: set) -> dict:
        '''
        Given a dictionary of paths and a current value returns a set
        of the reconstruced path from its origin
        '''
        total_path = {current}
        while current in cameFrom:
            current = cameFrom[current]
            total_path.add(current)
            self.win.write('+', *current, fgcolor='red')
        return total_path

    def is_valid(self,row: int, col: int) -> bool:
        '''
        given a row and an int returns true if the position
        is valid for the current board and is a path
        '''
        return (row >= 0) and (row < self.rows) and (col >= 0) and (col < self.cols) and self.walls[row][col] == 0

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
                        #self.win.write('*', *neighbor, fgcolor='green')
                        

        raise PathNotFound
        
        


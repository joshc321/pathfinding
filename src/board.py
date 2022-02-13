# ./pathfinding/board.py
# Intial: 02-07-2022


import numpy
from dataclasses import dataclass

class Board:

    def _validate(self, rows: int, cols: int, border: bool):
        assert type(rows) is int, f"Board._validate: rows must be type int, unsupported type '{type(rows)}'"
        assert type(cols) is int, f"Board._validate: cols must be type int, unsupported type '{type(cols)}'"
        assert type(border) is bool, f"Board._validate: border must be type bool, unsupported type '{type(border)}'"

    def __init__(self, rows: int, cols: int, border: bool = False) -> None:
        self._validate(rows, cols, border)
        self.rows = rows
        self.cols = cols
        self._border = border
        self._border_size = 1
        self.board_setup()
    
    def board_setup(self) -> None:
        if self._border:
            self._board = numpy.ones([self.rows + 2 * self._border_size, self.cols + 2 * self._border_size], numpy.int8)
            self._board[self._border_size:-self._border_size, self._border_size: -self._border_size] = 0
        else:
            self._board = numpy.zeros([self.rows, self.cols], dtype=numpy.int8)
    
    def fill(self, val) -> None:
        if self._border:
            self._board[self._border_size:-self._border_size, self._border_size: -self._border_size] = val
        else:
            self._board.fill(val)

    def reset(self) -> None:
        self.board_setup()
    
    def replace(self, current: int, goal: int) -> None:
        self._board[self._board == current] = goal
    
    def size(self):
        '''
        Returns the size of the usable board
        '''
        return (self.rows, self.cols)
    
    def actual_size(self):
        '''
        Returns the size of the entire board space
        '''
        return self._board.shape
    
    def row(self, row: int):
        assert self.is_valid_row(row), f"Board.row: invalid row '{row}'"
        return self._board[row,:]
    
    def col(self, col: int):
        assert self.is_valid_col(col), f"Board.col: invalid row '{col}'"
        return self._board[:,col]

    def _normalize(self, val):
        assert type(val) in (int, tuple), f"Board._normalize: unsupported type '{type(val)}'"
        if self._border:
            if type(val) is int:
                return val + self._border_size
            elif type(val) is tuple:
                return tuple(self._normalize(i) for i in val)
        return val

    def is_valid_pos(self, pos: (int)) -> bool:
        '''
        Returns true if the given pos(row, col) is a valid board position
        '''
        return self.is_valid_row(pos[0]) and self.is_valid_col(pos[1])

    def is_valid_row(self, row: int) -> bool:
        assert type(row) is int, f"Board.valid_row: unsupported type '{type(row)}'"
        return row in range(self.rows)
    
    def is_valid_col(self, col: int) -> bool:
        assert type(col) is int, f"Board.valid_col: unsupported type '{type(col)}'"
        return col in range(self.cols)

    def __iter__(self):
        def grid_gen(values):
            yield from values
        return grid_gen((row, col, self[row,col]) for row in range(self.rows) \
        for col in range(self.cols))

    def __iterall__(self):
        def grid_gen(values):
            yield from values
        return grid_gen((row, col, self._board[row,col]) for row in range(self.actual_size()[0]) \
        for col in range(self.actual_size()[1]))

    def __getitem__(self, index):
        if type(index) is not tuple or len(index) != 2 or\
           type(index[0]) is not int or  type(index[1]) is not int\
           or not self.is_valid_row(index[0]) or \
           not self.is_valid_col(index[1]):
            raise TypeError(f'Board.__getitem___: illegal index {index}')
        return self._board[self._normalize(index)]

    def __setitem__(self, index, val):
        if type(index) is not tuple or len(index) != 2 or\
           type(index[0]) is not int or  type(index[1]) is not int\
           or not self.is_valid_row(index[0]) or \
           not self.is_valid_col(index[1]):
            raise TypeError(f'Board.__getitem___: illegal index {index}')
        if type(val) not in (int, float):
            raise TypeError(f'Board.__setitem___: illegal value {val}')
        self._board[self._normalize(index)] = val

    def __delitem__(self, index):
        if type(index) is not tuple or len(index) != 2 or\
           type(index[0]) is not int or  type(index[1]) is not int\
           or not self.is_valid_row(index[0]) or \
           not self.is_valid_col(index[1]):
            raise TypeError(f'Board.__getitem___: illegal index {index}')
        self._board[self._normalize(index)] = 0

    def __str__(self) -> str:
        return str(self._board)

    def __repr__(self) -> str:
        return f'Board({self.rows}, {self.cols})'
    
    def __call__(self, *args: any, **kwds: any) -> None:
        self.__init__(*args, **kwds)

@dataclass
class BoardOptions:
    path: int = 0
    wall: int = 1
    route: int = 2
    start_end: int = 3

if __name__ == '__main__':
    b = Board(10,10)
    print(b)
    b[1,2] = 3
    print(b)
    print(b.col(3))
    print(b.actual_size())
    b(5,5)
    print(b)
    try:
        Board(32.1, 4.2)
    except AssertionError:
        pass

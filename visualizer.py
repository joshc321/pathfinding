# ./pathfinding/visualizer.py

import pygame
from src import *
from settings import settings

_INITIAL_WIDTH, _INITIAL_HEIGHT = 420, 470

_BACKGROUND_COLOR = pygame.Color(255,255,255)
_WALL_COLOR = pygame.Color(255,255,255)
_PATH_COLOR = pygame.Color(0,0,0)
_ROUTE_COLOR = pygame.Color(195, 111, 111)
_START_END_COLOR = pygame.Color(55, 116, 144)
_WARNING_COLOR = pygame.Color(136, 39, 39)
_W_PATH_COLOR = pygame.Color(219, 193, 121)
_S_PATH_COLOR = pygame.Color(117, 32, 32)

BD = BoardOptions()

COLORS = {BD.path: _PATH_COLOR, BD.wall: _WALL_COLOR, BD.route: _ROUTE_COLOR, 
          BD.start_end: _START_END_COLOR, BD.w_path: _W_PATH_COLOR, 
          BD.s_path: _S_PATH_COLOR}

_FIELD_HEIGHT_PERCENT = 1
_FIELD_WIDTH_PERCENT = 1

_ROWS = settings['board']['rows']
_COLS = settings['board']['cols']



class Visualizer:
    def __init__(self) -> None:
        self._running = True
        self._board = Board(_ROWS, _COLS, True)
        self.is_pressed = False
        self._single_click = False

        self._selected_path = BD.wall

    def run(self) -> None:
        pygame.init()
        pygame.display.set_caption('Visualizer')

        try:

            self._create_surface((_INITIAL_WIDTH, _INITIAL_HEIGHT))
            self._redraw_game_window()
            while self._running:
                self._visualizer()

        finally:
            pygame.quit()

    def _create_surface(self, size: tuple[int, int]) -> None:
        self._surface = pygame.display.set_mode(size, pygame.RESIZABLE)
    
    def _handle_events(self) -> None:
        for event in pygame.event.get():
            self._handle_event(event)
    
    def _handle_key(self, event) -> None:
        assert event.type == pygame.KEYDOWN, 'Visualizer._handle_key: event must be a KEYDOWN event'
        mods = pygame.key.get_mods()

        if event.key ==pygame.K_ESCAPE:
            self._stop_game()
        if event.key == pygame.K_1 and not (mods & pygame.KMOD_LSHIFT):
            self._run_astar()
        if event.key == pygame.K_2 and not (mods & pygame.KMOD_LSHIFT):
            self._run_dfs()
        if event.key == pygame.K_3 and not (mods & pygame.KMOD_LSHIFT):
            self._run_bfs()
        if event.key == pygame.K_1 and (mods & pygame.KMOD_LSHIFT):
            self._run_prim()
        if event.key == pygame.K_2 and (mods & pygame.KMOD_LSHIFT):
            self._run_rdf()
        if event.key == pygame.K_c:
            self._board.reset()
        if event.key == pygame.K_f:
            self._board.fill(self._selected_path)
        if event.key == pygame.K_t:
            #testing block
            self._selected_path = next(BD.valid_paths)
    
    def _handle_event(self, event) -> None:
        if event.type == pygame.QUIT:
            self._stop_game()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.is_pressed = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.is_pressed = False
        elif event.type == pygame.MOUSEMOTION and self.is_pressed == True:   
            self._draw_wall()
        elif event.type == pygame.KEYDOWN:
            self._handle_key(event)
    
    def _visualizer(self):
        self._handle_events()
        self._draw_frame()
    
    def _run_rdf(self) -> None:
        self._board.reset()
        RandomDepthFirst(self._board, self._visualizer, multiplier=settings['multiplier']).depth()

    def _run_prim(self) -> None:
        self._board.reset()
        RandomPrim(self._board, self._visualizer, multiplier=settings['multiplier']).prims()

    def _run_astar(self) -> None:
        '''
        runs astar pathfinding algorithm on the current
        board state updating the board with the found
        route
        '''
        self._board.replace(BD.route, BD.path)
        self._board.replace(BD.start_end, BD.path)
        start, end = self._get_start_end()
        try:
            Astar(self._board, start, end).astar()
        except PathNotFound:
            self._path_not_found()

    def _run_dfs(self) -> None:
        '''
        runs depth first search pathfinding algorithm on the 
        current board state updating the baord with the found
        route
        '''
        self._board.replace(BD.route, BD.path)
        self._board.replace(BD.start_end, BD.path)
        start, end = self._get_start_end()
        try:
            DFS(self._board, start, end).dfs()
        except PathNotFound:
            self._path_not_found()
    
    def _run_bfs(self) -> None:
        '''
        runs breadth first search pathfinding algorithm on the 
        current board state updating the baord with the found
        route
        '''
        self._board.replace(BD.route, BD.path)
        self._board.replace(BD.start_end, BD.path)
        start, end = self._get_start_end()
        try:
            BFS(self._board, start, end).bfs()
        except PathNotFound:
            self._path_not_found()

    def _path_not_found(self) -> None:
        self._surface.fill(_WARNING_COLOR)
        pygame.display.update()

    def _get_start_end(self) -> list[tuple]:
        start_end = []
        while len(start_end) < 2:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN
                and event.key == pygame.K_ESCAPE):
                    self._stop_game()
                if event.type == pygame.MOUSEBUTTONUP:
                    coordinate = self._get_coordinates_at_pixel(event.pos)
                    if coordinate not in start_end and self._board.is_valid_pos(coordinate) \
                    and self._board[coordinate] != BD.wall:
                        self._board[coordinate] = BD.start_end
                        start_end.append(coordinate)
                        self._draw_frame()
        return start_end
        

    def _stop_game(self) -> None:
        self._running = False

    def _draw_frame(self) -> None:
        self._surface.fill(_BACKGROUND_COLOR)
        self._draw_grid()
        pygame.display.update()
    
    def _redraw_game_window(self) -> None:
        self._surface.fill(_BACKGROUND_COLOR)
        pygame.display.update()

    def _draw_grid(self) -> None:
        '''
        Draws the entire game board in grids
        '''
        iterator = self._board.__iterall__()
        for row, col, val in iterator:
            self._draw_box(row, col, COLORS[val])

    def _draw_box(self, row: int, col: int, color) -> pygame.Rect:
        '''
        Draws a pygame rect at the given row, col with given color, 
        returns the rect object
        '''
        left = self._grid_size()[1] * col
        top = self._grid_size()[0] * row
        rect = pygame.Rect(left, top, self._grid_size()[1], self._grid_size()[0])
        pygame.draw.rect(self._surface, color, rect)
        return rect
    
    def _draw_wall(self):
        '''
        turns the current mouse position into a wall
        '''
        pos = pygame.mouse.get_pos()
        coords = self._get_coordinates_at_pixel(pos)
        try:
            self._board[coords] = self._selected_path
        except TypeError:
            pass

    def _get_coordinates_at_pixel(self, pos):
        '''
        given a tuple of screen coordinates returns cooreponding row,col
        values
        '''
        col = int(pos[0] / self._grid_size()[1]) - 1
        row = int(pos[1] / self._grid_size()[0]) - 1
        return row, col

    def _grid_size(self) -> float:
        '''
        returns tuple with height of each grid and width of each grid
        '''
        return (self._field_height() / self._board.actual_size()[0], \
        self._field_width() / self._board.actual_size()[1])

    def _field_height(self) -> float:
        'returns the field height on screen adjusted for the screen size'
        return (int(self._display_height() * _FIELD_HEIGHT_PERCENT 
                             / (self._board.actual_size()[0])) 
                             * (self._board.actual_size()[0]))

    def _field_width(self) -> float:
        'returns the field width on screen adjusted for the screen size'
        return(int(self._display_width() * _FIELD_WIDTH_PERCENT 
                             / self._board.actual_size()[1]) 
                             * self._board.actual_size()[1])

    def _display_height(self) -> int:
        'returns the display height'
        return self._surface.get_height()

    def _display_width(self) -> int:
        'returns the display width'
        return self._surface.get_width()

if __name__ == '__main__':
    Visualizer().run()
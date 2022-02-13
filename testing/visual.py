from this import d
import pygame
import pygcurse
from astar import Astar
import time
from randomized_prim import RandomPrim
import numpy

class Screen:
    def __init__(self, width, height, fg_color='black', bg_color='white') -> None:
        self.width = width
        self.height = height
        self.rows = self.height - 1
        self.cols = self.width - 1
        self.fg_color = fg_color
        self.bg_color = bg_color
        self._running, self._drag = True, False
        self._start_end = []
        self._walls = set()
        self._maze = None
    
    def run(self):
        self._setup()
        self._get_start_end()
        self._screen_loop()
    
    def _screen_loop(self):
        while self._running:
            self._handle_events()
    
    def _get_start_end(self):
        self._start_end = []
        while len(self._start_end) < 2:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    self._quit()
                if event.type == pygame.MOUSEBUTTONUP:
                    coordinate = self.win.getcoordinatesatpixel(event.pos)
                    if coordinate not in self._start_end and coordinate not in self._walls:
                        self.win.write('O', *coordinate)
                        self._start_end.append(coordinate)

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._quit()
            elif event.type == pygame.KEYDOWN:
                self._handle_key_events(event.key)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._drag = True
            elif event.type == pygame.MOUSEBUTTONUP:
                self._drag = False
            elif event.type == pygame.MOUSEMOTION:
                if self._drag:
                    coordinate = self.win.getcoordinatesatpixel(event.pos)
                    if coordinate not in self._start_end:
                        self.win.write('X', *coordinate)
                        self._walls.add(coordinate)
    
    def _handle_key_events(self, key):
        if key == pygame.K_ESCAPE:
            self._quit()
        elif key == pygame.K_c:
            self._clear_screen()
            self._get_start_end()
            self._walls = set()
        elif key == pygame.K_p:
            self.win.write(str(numpy.ones([15,15])))
            print(self._walls)
        elif key == pygame.K_a:
            start = time.time()
            Astar(self.win, self._start_end[0], self._start_end[1], self._walls, self.cols, self.rows).astar()
            self.win.write('O', *self._start_end[0], fgcolor='black')
            self.win.write('O', *self._start_end[1], fgcolor='black')
            end = time.time()
            print(f'Total Time: {end - start}')
        elif key == pygame.K_m:
            self._clear_screen()
            prim = RandomPrim(self.win, self.rows, self.cols)
            prim.prims()
            self._maze = prim.maze
            self._walls = prim.walls_set()
            self._draw_walls()
            self._get_start_end()

    def _draw_walls(self):
        #for wall in self._walls:
        #    self.win.write('X', *wall, fgcolor='blue')
        #print(self._maze)
        a = '\n'.join(''.join('X' if i == 1 else ' ' for i in row) for row in self._maze)
        self.win.write(a, x=0, y=0)
        # print(a)
        # for idx, row in enumerate(self._maze):
        #     s = ''.join('X' if i == 1 else ' ' for i in row)
        #     print(s)
        #     self.win.write(s, x=0, y=idx)

    def _quit(self):
        pygame.quit()
        self._running = False

    def _setup(self):
        self.win = pygcurse.PygcurseWindow(self.width,self.height,fgcolor=self.fg_color)
        self._clear_screen()

    def _clear_screen(self):
        self.win.setscreencolors(None, self.bg_color, clear=True)
        self._start_end = []

if __name__ == '__main__':
    screen = Screen(90,55)
    screen.run()
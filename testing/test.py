came_from = {(0, 1): (0, 0), (1, 0): (0, 0), (0, 0): (1, 0), (1, 1): (1, 0), (2, 0): (1, 0), (2, 1): (2, 0), (3, 0): (2, 0), (3, 1): (3, 0), (4, 0): (3, 0), (4, 1): (4, 0), (5, 0): (4, 0), (5, 1): (5, 0), (6, 0): (5, 0), (6, 1): (6, 0), (7, 0): (6, 0), (7, 1): (7, 0), (8, 0): (7, 0), (8, 1): (8, 0), (9, 0): (8, 0), (9, 1): (9, 0), (9, 2): (9, 1), (8, 2): (9, 2), (9, 3): (9, 2), (8, 3): (9, 3), (9, 4): (9, 3), (8, 4): (9, 4), (9, 5): (9, 4), (8, 5): (9, 5), (9, 6): (9, 5), (8, 6): (9, 6), (9, 7): (9, 6), (8, 7): (9, 7), (9, 8): (9, 7), (8, 8): (9, 8), (9, 9): (9, 8), (8, 9): (9, 9), (7, 9): (8, 9), (6, 9): (7, 9), (7, 8): (7, 9), (6, 8): (7, 8), (7, 7): (7, 8), (6, 7): (7, 7), (7, 6): (7, 7), (6, 6): (7, 6), (7, 5): (7, 6), (6, 5): (7, 5), (7, 4): (7, 5), (6, 4): (7, 4), (7, 3): (7, 4), (6, 3): (7, 3), (7, 2): (7, 3), (6, 2): (7, 2), (5, 2): (6, 2), (4, 2): (5, 2), (5, 3): (5, 2), (4, 3): (5, 3), (5, 4): (5, 3), (4, 4): (5, 4), (5, 5): (5, 4), (4, 5): (5, 5), (5, 6): (5, 5), (4, 6): (5, 6), (5, 7): (5, 6), (4, 7): (5, 7), (5, 8): (5, 7), (4, 8): (5, 8), (5, 9): (5, 8), (4, 9): (5, 9), (3, 9): (4, 9), (2, 9): (3, 9), (3, 8): (3, 9), (2, 8): (3, 8), (3, 7): (3, 8), (2, 7): (3, 7), (3, 6): (3, 7), (2, 6): (3, 6), (3, 5): (3, 6), (2, 5): (3, 5), (3, 4): (3, 5), (2, 4): (3, 4), (3, 3): (3, 4), (2, 3): (3, 3), (3, 2): (3, 3), (2, 2): (3, 2), (1, 2): (2, 2), (0, 2): (1, 2), (1, 3): (1, 2), (0, 3): (1, 3), (1, 4): (1, 3), (0, 4): (1, 4), (1, 5): (1, 4), (0, 5): (1, 5), (1, 6): (1, 5), (0, 6): (1, 6), (1, 7): (1, 6), (0, 7): (1, 7), (1, 8): (1, 7), (0, 8): (1, 8), (1, 9): (1, 8), (0, 9): (1, 9)}
current = (8,8)
print(came_from[current])




# import pygame
# import pygcurse

# def test():
#     win = pygcurse.PygcurseWindow(50,50,fgcolor='black')
#     win.setscreencolors(None, 'white', clear=True)

#     drag, run = False, True
#     while run:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
#                 pygame.quit()
#                 run = False
#             elif event.type == pygame.KEYDOWN and event.key == pygame.K_c:
#                 win.setscreencolors(None, 'white', clear=True)
#             elif event.type == pygame.MOUSEBUTTONDOWN:
#                 drag = True
#             elif event.type == pygame.MOUSEBUTTONUP:
#                 drag = False
#             elif event.type == pygame.MOUSEMOTION:
#                 if drag:
#                     coordinate = win.getcoordinatesatpixel(event.pos)
#                     win.write('#', *coordinate)

# if __name__ == '__main__':
#     test()
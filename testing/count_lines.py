
file_paths = ['astar_main.py', 'rand_prim.py', 'visualizer.py', 'board.py']

total = 0
for path in file_paths:
    with open(path, 'r') as file:
        total += sum(1 for _ in file)

print(total)
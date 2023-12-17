import math

input: list[str] = [
    '...#......',
    '.......#..',
    '#.........',
    '..........',
    '......#...',
    '.#........',
    '.........#',
    '..........',
    '.......#..',
    '#...#.....',
]

input_file = open('input.txt', 'r')
input = list(filter(lambda s: s != '', input_file.read().split('\n')))

def draw_map(input: list[str]):
    for line in input:
        print(line)

def add_empty_row(input: list[str], y: int):
    input.insert(y, ''.ljust(len(input[0]), '.'))

def add_empty_column(input: list[str], x: int):
    for y in range(len(input)):
        input[y] = input[y][:x] + '.' + input[y][x:]

def is_empty_row(input: list[str], y: int) -> bool:
    return '#' not in input[y]

def is_empty_column(input: list[str], x: int) -> bool:
    for row in input:
        if row[x] == '#':
            return False
    return True

def dijkstra(input: list[str], all_nodes: list[tuple[int, int]], current_node_coordinates: tuple[int, int]) -> dict[tuple[int, int], int]:
    distance_map: list[list] = [[math.inf for _ in line] for line in input]

    n_x, n_y = current_node_coordinates
    distance_map[n_y][n_x] = 0

    queue: list[tuple[tuple, int]] = []
    for d_x, d_y in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
        c_x: int = n_x + d_x
        c_y: int = n_y + d_y

        if 0 <= c_x < len(distance_map[0]) and 0 <= c_y < len(distance_map):
            queue.append(((c_x, c_y), 1))

    while queue:
        x, y = queue[0][0]
        distance: int = queue[0][1]
        queue = queue[1:]

        if (distance_map[y][x] == math.inf) or distance < int(distance_map[y][x]):
            distance_map[y][x] = distance
            for d_x, d_y in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
                c_x: int = x + d_x
                c_y: int = y + d_y

                if 0 <= c_x < len(distance_map[0]) and 0 <= c_y < len(distance_map):
                    queue.append(((c_x, c_y), distance + 1))
            continue

    distances: dict[tuple[int, int], int] = {}
    for d_x, d_y in all_nodes:
        distances[(d_x, d_y)] = distance_map[d_y][d_x]

    return distances

expanded_map: list[str] = []
for line in input:
    expanded_map.append(line)

for y in range(len(input) - 1, -1, -1):
    if is_empty_row(expanded_map, y):
        add_empty_row(expanded_map, y)

for x in range(len(input[0]) - 1, -1, -1):
    if is_empty_column(expanded_map, x):
        add_empty_column(expanded_map, x)

# get nodes
nodes: list[tuple[int, int]] = []

for y in range(len(expanded_map)):
    for x in range(len(expanded_map[y])):
        if expanded_map[y][x] == '#':
            nodes.append((x, y))

pairs: list[tuple] = []
overall_map: dict[tuple, dict] = {}

for current in nodes:
    overall_map[current] = dijkstra(expanded_map, nodes, current)

def already_in_pairs(src: tuple, dst: tuple, pair_list: list[tuple]) -> bool:
    for pair in pair_list:
        if (src, dst) == pair or (dst, src) == pair:
            return True
    return False

total: int = 0
for src_key in overall_map.keys():
    for dst_key in overall_map[src_key].keys():
        if not already_in_pairs(src_key, dst_key, pairs):
            total += overall_map[src_key][dst_key]
            pairs.append((src_key, dst_key))

print(total)

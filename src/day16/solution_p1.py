from enum import Enum

class Direction(Enum):
    UP = (0, -1)
    RIGHT = (1, 0)
    DOWN = (0, 1)
    LEFT = (-1, 0)

    @staticmethod
    def value_of(value: tuple):
        if value == Direction.UP.value:
            return Direction.UP
        if value == Direction.RIGHT.value:
            return Direction.RIGHT
        if value == Direction.DOWN.value:
            return Direction.DOWN
        if value == Direction.LEFT.value:
            return Direction.LEFT


input: list[str] = [
    '.|...\\....',
    '|.-.\\.....',
    '.....|-...',
    '........|.',
    '..........',
    '.........\\',
    '..../.\\\\..',
    '.-.-/..|..',
    '.|....-|.\\',
    '..//.|....',
]

input_file = open('input.txt', 'r')
input = list(filter(lambda s: s != '', input_file.read().split('\n')))

def get_next_direction(direction: Direction, character: str) -> list[Direction]:
    if character == '/':
        cx, cy = direction.value
        return [Direction.value_of((-cy, -cx))]

    if character == '\\':
        cx, cy = direction.value
        return [Direction.value_of((cy, cx))]

    if character == '-':
        if direction == Direction.LEFT or direction == Direction.RIGHT:
            return [direction]
        return [Direction.LEFT, Direction.RIGHT]

    if character == '|':
        if direction == Direction.UP or direction == Direction.DOWN:
            return [direction]
        return [Direction.UP, Direction.DOWN]

    return [direction]

def is_used_mirror(used_mirrors: list[tuple[tuple, list[Direction]]], coordinates: tuple, direction: Direction) -> bool:
    for mirror_coordinates, directions in used_mirrors:
        if mirror_coordinates != coordinates:
            continue

        if direction in directions:
            return True

        # coord found but direction not found - add to used list
        directions.append(direction)
        return False

    # not found - add to used list
    used_mirrors.append((coordinates, [direction]))
    return False


visit_map: list[str] = ['.'.ljust(len(line), '.') for line in input]

iterators: list[tuple] = [(0, 0)]
directions: list[Direction] = [Direction.RIGHT]
used_splitters: list[tuple] = []
used_mirrors: list[tuple[tuple, list[Direction]]] = []

while iterators:
    for i in range(len(iterators) - 1, -1, -1):
        x, y = iterators[i]
        direction = directions[i]

        if not 0 <= x < len(input[0]) or not 0 <= y < len(input):
            iterators.pop(i)
            directions.pop(i)
            continue

        if visit_map[y][x] != '#':
            visit_map[y] = visit_map[y][:x] + '#' + visit_map[y][x + 1:]

        if input[y][x] in '=|' and (x, y) in used_splitters:
            iterators.pop(i)
            directions.pop(i)
            continue

        if input[y][x] in '/\\' and is_used_mirror(used_mirrors, iterators[i], direction):
            iterators.pop(i)
            directions.pop(i)
            continue

        next_directions: list[Direction] = get_next_direction(direction, input[y][x])
        if input[y][x] in '=|':
            used_splitters.append((x, y))

        if len(next_directions) == 2:
            first_direction, second_direction = next_directions
            fx, fy = first_direction.value
            iterators[i] = (x + fx, y + fy)
            directions[i] = first_direction

            sx, sy = second_direction.value
            iterators.append((x + sx, y + sy))
            directions.append(second_direction)

            continue

        nx, ny = next_directions[0].value
        iterators[i] = (x + nx, y + ny)
        directions[i] = next_directions[0]

total: int = 0
for line in visit_map:
    for char in line:
        if char == '#':
            total += 1
print(total)

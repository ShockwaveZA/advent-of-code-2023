
from enum import Enum

class Direction(Enum):
    UP = (0, -1)
    RIGHT = (1, 0)
    DOWN = (0, 1)
    LEFT = (-1, 0)

    def opposite_direction(self):
        opposite_tuple = (-self.value[0], -self.value[1])
        for direction in Direction:
            if direction.value == opposite_tuple:
                return direction

input: list[str] = [
    '..F7.',
    '.FJ|.',
    'SJ.L7',
    '|F--J',
    'LJ...',
]

input_file = open('input.txt', 'r')
input = list(filter(lambda s: s != '', input_file.read().split('\n')))

def get_pipe_directions(input: list[str], coordinates: tuple[int, int]) -> list[Direction]:
    x, y = coordinates
    try:
        pipe_letter: str = input[y][x]
    except IndexError:
        return []

    if pipe_letter == '|':
        return [Direction.UP, Direction.DOWN]
    elif pipe_letter == '-':
        return [Direction.LEFT, Direction.RIGHT]
    elif pipe_letter == 'L':
        return [Direction.UP, Direction.RIGHT]
    elif pipe_letter == 'J':
        return [Direction.UP, Direction.LEFT]
    elif pipe_letter == '7':
        return [Direction.DOWN, Direction.LEFT]
    elif pipe_letter == 'F':
        return [Direction.DOWN, Direction.RIGHT]

    return []


def is_connecting_pipe(input: list[str], source: tuple[int, int], destination: tuple[int, int]) -> bool:
    s_x, s_y = source
    d_x, d_y = destination
    change_x, change_y = d_x - s_x, d_y - s_y

    if change_x == 0 and change_y == -1:
        # going UP
        return Direction.DOWN in get_pipe_directions(input, destination)
    elif change_x == 1 and change_y == 0:
        # going RIGHT
        return Direction.LEFT in get_pipe_directions(input, destination)
    elif change_x == 0 and change_y == 1:
        # going DOWN
        return Direction.UP in get_pipe_directions(input, destination)
    elif change_x == -1 and change_y == 0:
        # going LEFT
        return Direction.RIGHT in get_pipe_directions(input, destination)

    return False

def get_letter_from_directions(directions: list[Direction]) -> str:
    if len(directions) != 2:
        raise Exception('Invalid directions received')

    if Direction.UP in directions and Direction.DOWN in directions:
        return '|'
    elif Direction.LEFT in directions and Direction.RIGHT in directions:
        return '-'
    elif Direction.UP in directions and Direction.RIGHT in directions:
        return 'L'
    elif Direction.UP in directions and Direction.LEFT in directions:
        return 'J'
    elif Direction.DOWN in directions and Direction.LEFT in directions:
        return '7'
    elif Direction.DOWN in directions and Direction.RIGHT in directions:
        return 'F'

def get_next_coordinate(coordinates: tuple[int, int], direction: Direction) -> tuple[int, int]:
    x, y = coordinates
    change_x, change_y = direction.value
    return x + change_x, y + change_y

def determine_letter(input: list[str], coordinates: tuple[int, int]) -> str:
    possible_directions: list[Direction] = []
    x, y = coordinates

    # try UP
    if y > 0:
        if is_connecting_pipe(input, coordinates, get_next_coordinate(coordinates, Direction.UP)):
            possible_directions.append(Direction.UP)

    # try RIGHT
    if x < len(input[0]) - 1:
        if is_connecting_pipe(input, coordinates, get_next_coordinate(coordinates, Direction.RIGHT)):
            possible_directions.append(Direction.RIGHT)

    # try DOWN
    if y < len(input) - 1:
        if is_connecting_pipe(input, coordinates, get_next_coordinate(coordinates, Direction.DOWN)):
            possible_directions.append(Direction.DOWN)

    # try LEFT
    if x > 0:
        if is_connecting_pipe(input, coordinates, get_next_coordinate(coordinates, Direction.LEFT)):
            possible_directions.append(Direction.LEFT)

    return get_letter_from_directions(possible_directions)

def get_continuing_direction(input: list[str], direction: Direction, coordinates: tuple[int, int]) -> Direction:
    continuing_direction, *rest = list(filter(lambda d: d != direction.opposite_direction(), get_pipe_directions(input, coordinates)))
    return continuing_direction

def find_s(input: list[str]) -> tuple[int, int]:
    for y in range(len(input)):
        for x in range(len(input[y])):
            if input[y][x] == 'S':
                return (x, y)

start_coordinates: tuple[int, int] = find_s(input)
s_x, s_y = start_coordinates

input[s_y] = input[s_y][:s_x] + determine_letter(input, start_coordinates) + input[s_y][s_x + 1:]
directions: list[Direction] = get_pipe_directions(input, start_coordinates)

direction_a, direction_b = directions
iterator_a, iterator_b = get_next_coordinate(start_coordinates, direction_a), get_next_coordinate(start_coordinates, direction_b)
direction_a = get_continuing_direction(input, direction_a, iterator_a)
direction_b = get_continuing_direction(input, direction_b, iterator_b)
steps_a, steps_b = 1, 1

while iterator_a != iterator_b:
    iterator_a = get_next_coordinate(iterator_a, direction_a)
    direction_a = get_continuing_direction(input, direction_a, iterator_a)
    steps_a += 1

    iterator_b = get_next_coordinate(iterator_b, direction_b)
    direction_b = get_continuing_direction(input, direction_b, iterator_b)
    steps_b += 1

print(steps_a)






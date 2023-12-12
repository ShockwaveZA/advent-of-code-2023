from dataclasses import dataclass

input: list[str] = [
    '467..114..',
    '...*......',
    '..35..633.',
    '......#...',
    '617*......',
    '.....+.58.',
    '..592.....',
    '......755.',
    '...$.*....',
    '.664.598..',
]

@dataclass
class Neighbour:
    number: int
    x: int
    y: int

def get_number(input: list[str], x: int, y: int) -> int:
    string: str = ''
    i: int = x
    while i - 1 >= 0 and input[y][i - 1].isdigit():
        i -= 1

    while i < len(input[y]) and input[y][i].isdigit():
        string += input[y][i]
        i += 1
    return int(string)

def get_start_coords_of_number(input: list[str], x: int, y: int) -> tuple[int, int]:
    i: int = x
    while i - 1 >= 0 and input[y][i - 1].isdigit():
        i -= 1
    return (i, y)


def get_gear_ratio(input: list[str], x: int, y: int) -> int:
    if input[y][x] != '*':
        return 0

    def get_neighbouring_numbers(input: list[str], x: int, y: int) -> list[int]:
        neighbours: list[Neighbour] = []
        for i in range(y - 1, y + 2):
            if i < 0 or i >= len(input):
                continue

            for j in range(x - 1, x + 2):
                if j < 0 or j >= len(input[i]):
                    continue

                if y == i and x == j:
                    continue

                if input[i][j].isdigit():
                    number: int = get_number(input, j, i)

                    exists_in_array: bool = False
                    for neighbour in neighbours:
                        if get_start_coords_of_number(input, j, i) == get_start_coords_of_number(input, neighbour.x, neighbour.y):
                            exists_in_array = True
                            break

                    if not exists_in_array:
                        neighbours.append(Neighbour(number, j, i))

        return list(map(lambda n: n.number, neighbours))

    neighbouring_numbers: list[int] = get_neighbouring_numbers(input, x, y)
    if len(neighbouring_numbers) == 2:
        n1, n2 = neighbouring_numbers
        return n1 * n2
    return 0


text_file = open('input.txt', 'r')
input = text_file.read().split('\n')

total: int = 0
y: int = 0
while y < len(input):
    x: int = 0
    while x < len(input[y]):
        if input[y][x] == '*':
            total += get_gear_ratio(input, x, y)
        x += 1
    y += 1

print(total)
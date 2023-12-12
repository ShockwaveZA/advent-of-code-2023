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

def number_length(input: list[str], x: int, y: int) -> int:
    i: int = x
    while i < len(input[y]) and input[y][i].isdigit():
        i += 1
    return i - x

def get_number(input: list[str], x: int, y: int) -> int:
    string: str = ''
    i: int = x
    while i < len(input[y]) and input[y][i].isdigit():
        string += input[y][i]
        i += 1
    return int(string)

def is_part_number(input: list[str], x: int, y: int) -> bool:
    def has_adjacent_part(input: list[str], x: int, y: int) -> bool:
        def get_neighbours(input: list[str], x: int, y: int) -> str:
            neighbours: list[str] = []
            for i in range(y - 1, y + 2):
                if i < 0 or i >= len(input):
                    continue

                line: str = ''
                for j in range(x - 1, x + 2):
                    if j < 0 or j >= len(input[i]):
                        continue

                    if y == i and x == j:
                        continue

                    line += input[i][j]
                neighbours.append(line)
            return ''.join(neighbours)

        return any(char not in '0123456789.' for char in get_neighbours(input, x, y))

    i: int = x
    while i < len(input[y]) and input[y][i].isdigit():
        if has_adjacent_part(input, i, y):
            return True
        i += 1
    return False

text_file = open('input.txt', 'r')
input = text_file.read().split('\n')

total: int = 0
y: int = 0
while y < len(input):
    x: int = 0
    while x < len(input[y]):
        if input[y][x].isdigit():
            length: int = number_length(input, x, y)
            if is_part_number(input, x, y):
                total += get_number(input, x, y)
            x += length
            continue
        x += 1
    y += 1

print(total)
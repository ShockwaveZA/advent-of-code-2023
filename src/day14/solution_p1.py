


input: list[str] = [
    'O....#....',
    'O.OO#....#',
    '.....##...',
    'OO.#O....O',
    '.O.....O#.',
    'O.#..O.#.#',
    '..O..#O..O',
    '.......O..',
    '#....###..',
    '#OO..#....',
]

input_file = open('input.txt', 'r')
input = list(filter(lambda s: s != '', input_file.read().split('\n')))

def calculate_load(input: list[str]) -> int:
    total: int = 0
    length: int = len(input)

    for x in range(len(input[0])):
        boundary: int = -1

        for y in range(length):
            if input[y][x] == '#':
                boundary = y
                continue

            if input[y][x] == 'O':
                if y == boundary + 1:
                    boundary = y
                    total += length - y
                    continue

                boundary += 1
                input[boundary] = input[boundary][:x] + 'O' + input[boundary][x + 1:]
                input[y] = input[y][:x] + '.' + input[y][x + 1:]
                total += length - boundary

    return total

print(calculate_load(input))

NUMBER_MAP = {
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9,
}

input = [
    'two1nine',
    'eightwothree',
    'abcone2threexyz',
    'xtwone3four',
    '4nineeightseven2',
    'zoneight234',
    '7pqrstsixteen',
]

text_file = open('input.txt', 'r')
input: list[str] = list(filter(lambda s: s != '', text_file.read().split('\n')))

def extract_calibration_value(line: str) -> int:
    number_string: str = ''
    for i in range(len(line)):
        char: str = line[i]
        if char.isdigit():
            number_string += char
        else:
            for key in NUMBER_MAP.keys():
                if key[0] != char:
                    continue

                length: int = len(key)
                if line[i:i + length] == key:
                    number_string += str(NUMBER_MAP[key])
                    break

    return int(number_string[0] + number_string[-1])

total: int = 0
for line in input:
    total += extract_calibration_value(line)
print(total)
input = [
    '1abc2',
    'pqr3stu8vwx',
    'a1b2c3d4e5f',
    'treb7uchet',
]

text_file = open('input.txt', 'r')
input: list[str] = list(filter(lambda s: s != '', text_file.read().split('\n')))

def extract_calibration_value(line: str) -> int:
    number_string: str = ''
    for char in line:
        if char.isdigit():
            number_string += char
    return int(number_string[0] + number_string[-1])

total: int = 0
for line in input:
    total += extract_calibration_value(line)
print(total)

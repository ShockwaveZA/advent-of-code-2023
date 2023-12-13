

input: list[str] = [
    '???.### 1,1,3',
    '.??..??...?##. 1,1,3',
    '?#?#?#?#?#?#?#? 1,3,1,6',
    '????.#...#... 4,1,1',
    '????.######..#####. 1,6,5',
    '?###???????? 3,2,1',
]

input_file = open('input.txt', 'r')
input = list(filter(lambda s: s != '', input_file.read().split('\n')))

def get_combinations(line: str) -> int:

    def get_check_format(springs: str) -> str:
        return ','.join(map(str, map(len, filter(lambda i: i != '', springs.split('.')))))

    def generate_combinations(springs: str, check: str) -> int:
        try:
            index: int = springs.index('?')

            combinations: int = 0
            for char in ['.', '#']:
                substituted_springs = springs[:index] + char + springs[index + 1:]
                combinations += generate_combinations(substituted_springs, check)

            return combinations
        except ValueError:
            return 1 if check == get_check_format(springs) else 0


    springs, check = line.split(' ')

    return generate_combinations(springs, check)


total: int = 0
for line in input:
    total += get_combinations(line)
print(total)

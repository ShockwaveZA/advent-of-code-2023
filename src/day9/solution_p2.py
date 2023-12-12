

input: list[str] = [
    '0 3 6 9 12 15',
    '1 3 6 10 15 21',
    '10 13 16 21 30 45',
]

input_file = open('input.txt', 'r')
input = list(filter(lambda s: s != '', input_file.read().split('\n')))

def get_next_sequence_value(sequence: list[int]) -> int:
    def is_sequence_all_zero(sequence: list[int]) -> bool:
        for i in sequence:
            if i != 0:
                return False
        return True

    difference_sequences: list[list[int]] = []
    while len(difference_sequences) == 0 or not is_sequence_all_zero(difference_sequences[-1]):
        previous_sequence: list[int] = sequence
        if len(difference_sequences) > 0:
            previous_sequence = difference_sequences[-1]

        next_difference_sequence: list[int] = []
        for i in range(len(previous_sequence) - 1):
            next_difference_sequence.append(previous_sequence[i + 1] - previous_sequence[i])

        difference_sequences.append(next_difference_sequence)

    difference_sequences[-1].insert(0, 0)
    for i in range(len(difference_sequences) - 2, -1, -1):
        difference_sequences[i].insert(0, difference_sequences[i][0] - difference_sequences[i + 1][0])

    return sequence[0] - difference_sequences[0][0]

total: int = 0
for line in input:
    sequence: list[int] = list(map(int, line.split(' ')))
    total += get_next_sequence_value(sequence)

print(total)

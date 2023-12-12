input: list[str] = [
    'Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53',
    'Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19',
    'Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1',
    'Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83',
    'Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36',
    'Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11',
]

def get_card_score(card: str) -> int:
    name, values = card.split(': ')
    win_str, choice_str = values.split(' | ')
    winning_numbers: list[int] = list(map(int, filter(lambda i: i != '', str(win_str).split(' '))))
    chosen_numbers: list[int] = list(map(int, filter(lambda i: i != '', str(choice_str).split(' '))))

    matching_numbers: int = 0
    for number in chosen_numbers:
        matching_numbers = matching_numbers + 1 if number in winning_numbers else matching_numbers

    if matching_numbers == 0:
        return 0
    return 2 ** (matching_numbers - 1)


text_file = open('input.txt', 'r')
input = list(filter(lambda s: s != '', text_file.read().split('\n')))

total: int = 0
for line in input:
    total += get_card_score(line)

print(total)
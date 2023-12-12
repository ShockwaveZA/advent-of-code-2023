from dataclasses import dataclass

input = [
    'Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53',
    'Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19',
    'Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1',
    'Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83',
    'Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36',
    'Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11',
]

@dataclass
class Card:
    line: str
    count: int

def map_to_card(line: str) -> Card:
    return Card(line, 1)

def get_matching_numbers(card: str) -> int:
    win_str, choice_str = card.split(': ')[1].split(' | ')
    winning_numbers: list[int] = list(map(int, filter(lambda i: i != '', str(win_str).split(' '))))
    chosen_numbers: list[int] = list(map(int, filter(lambda i: i != '', str(choice_str).split(' '))))

    matching_numbers: int = 0
    for number in chosen_numbers:
        matching_numbers = matching_numbers + 1 if number in winning_numbers else matching_numbers

    return matching_numbers


text_file = open('input.txt', 'r')
input = list(filter(lambda s: s != '', text_file.read().split('\n')))

cards: list[Card] = list(map(map_to_card, input))

for i in range(len(cards)):
    card, count = cards[i].line, cards[i].count
    matching_numbers: int = get_matching_numbers(card)
    for j in range(i + 1, i + 1 + matching_numbers):
        if j >= len(cards):
            break
        cards[j].count += count

total: int = 0
for card in cards:
    total += card.count
print(total)

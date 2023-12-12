from dataclasses import dataclass

input = [
    'Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green',
    'Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue',
    'Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red',
    'Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red',
    'Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green',
]

TOTAL_CUBE = {
    'red': 12,
    'green': 13,
    'blue': 14,
}

@dataclass
class Game:
    id: int
    sets: list[dict[str, int]]

# text_file = open('input.txt', 'r')
# input: list[str] = list(filter(lambda s: s != '', text_file.read().split('\n')))

def get_game_info(line: str) -> Game:
    def map_subsets(set: str) -> dict[str, int]:
        subset = {}
        for roll in set.split(', '):
            count, colour = roll.split(' ')
            subset[colour] = int(count)
        return subset

    parts = line.split(': ')
    game_number: int = int(parts[0].split(' ')[-1])
    sets: list[str] = parts[1].split('; ')
    subsets: list[dict[str, int]] = list(map(map_subsets, sets))

    return Game(game_number, subsets)

def is_game_possible(game: Game) -> bool:
    for subset in game.sets:
        for colour in subset.keys():
            if subset[colour] > TOTAL_CUBE[colour]:
                return False
    return True

total: int = 0
for line in input:
    game: Game = get_game_info(line)
    if is_game_possible(game):
        total += game.id

print(total)

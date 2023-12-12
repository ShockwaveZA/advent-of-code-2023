from dataclasses import dataclass

input = [
    'Time:      7  15   30',
    'Distance:  9  40  200',
]

text_file = open('input.txt', 'r')
input = list(filter(lambda s: s != '', text_file.read().split('\n')))

@dataclass
class Race:
    time: int
    distance: int

def process_input(input: list[str]) -> list[Race]:
    times: list[int] = list(map(int, filter(lambda s: s != '', input[0].split(': ')[1].split(' '))))
    distances: list[int] = list(map(int, filter(lambda s: s != '', input[1].split(': ')[1].split(' '))))

    races: list[Race] = []
    for i in range(len(times)):
        races.append(Race(times[i], distances[i]))
    return races

def calculate_win_possibilities(race: Race) -> int:
    count: int = 0
    for i in range(race.distance // race.time, race.time):
        distance_by_finish: int = i + (race.time - i - 1) * i
        if distance_by_finish > race.distance:
            count += 1
    return count

races: list[Race] = process_input(input)
product: int = 1
for race in races:
    product *= calculate_win_possibilities(race)
print(product)
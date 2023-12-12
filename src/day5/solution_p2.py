import math
from enum import Enum
from dataclasses import dataclass

class Map(Enum):
    SED_TO_SOI = 'seed-to-soil'
    SOI_TO_FRT = 'soil-to-fertilizer'
    FRT_TO_WTR = 'fertilizer-to-water'
    WTR_TO_LGT = 'water-to-light'
    LGT_TO_TMP = 'light-to-temperature'
    TMP_TO_HUM = 'temperature-to-humidity'
    HUM_TO_LOC = 'humidity-to-location'

input: list[str] = [
    'seeds: 79 14 55 13',
    'seed-to-soil map:',
    '50 98 2',
    '52 50 48',
    'soil-to-fertilizer map:',
    '0 15 37',
    '37 52 2',
    '39 0 15',
    'fertilizer-to-water map:',
    '49 53 8',
    '0 11 42',
    '42 0 7',
    '57 7 4',
    'water-to-light map:',
    '88 18 7',
    '18 25 70',
    'light-to-temperature map:',
    '45 77 23',
    '81 45 19',
    '68 64 13',
    'temperature-to-humidity map:',
    '0 69 1',
    '1 0 69',
    'humidity-to-location map:',
    '60 56 37',
    '56 93 4',
]

@dataclass
class InputRange:
    start_value: int
    range: int

@dataclass
class ConversionMap:
    start_from_value: int
    start_to_value: int
    range: int

text_file = open('input.txt', 'r')
input = list(filter(lambda s: s != '', text_file.read().split('\n')))

def process_almanac(input: list[str]) -> dict:
    almanac_input: dict = {}
    seed_list: list[int] = list(map(int, str(input[0]).split(': ')[-1].split(' ')))
    seeds: list[InputRange] = []
    i: int = 0
    while i < len(seed_list):
        seeds.append(InputRange(seed_list[i], seed_list[i + 1]))
        i += 2

    almanac_input['seeds'] = seeds

    i = 1
    while i < len(input):
        if not input[i][0].isdigit():
            section_dict: dict = {}
            map_name: str = input[i].split(' ')[0]
            i += 1
            while i < len(input) and input[i][0].isdigit():
                dst, src, rng = map(int, input[i].split(' '))
                section_dict[src] = ConversionMap(src, dst, rng)
                i += 1

            sorted_keys: list[str] = sorted(section_dict.keys())
            sorted_section_dict: dict = {key: section_dict[key] for key in sorted_keys}

            almanac_input[map_name] = sorted_section_dict

    return almanac_input

def get_smallest_location_by_seed(seed: InputRange, almanac: dict) -> int:
    def map_that_contains_seed(seed: InputRange, conversion_key_map: dict) -> ConversionMap or None:
        for key in conversion_key_map.keys():
            range: int = conversion_key_map[key].range
            if int(key) <= seed.start_value < int(key) + range or int(key) <= seed.start_value + seed.range < int(key) + range:
                return conversion_key_map[key]
        return None

    def get_destination_value(value: int, c_map: ConversionMap) -> int:
        if c_map.start_from_value <= value < c_map.start_from_value + c_map.range:
            offset: int = value - c_map.start_from_value
            return c_map.start_to_value + offset
        return value

    def calculate_value(seed: InputRange, almanac: dict, maps: list[Map]) -> int:
        if len(maps) == 0:
            return seed.start_value

        current_map, *other_maps = maps
        calculated_values: list[int] = []

        keys: list[str] = list(almanac[current_map.value].keys())
        if seed.start_value < almanac[current_map.value][keys[0]].start_from_value:
            difference: int = almanac[current_map.value][keys[0]].start_from_value - seed.start_value
            calculated_values.append(calculate_value(InputRange(seed.start_value, difference), almanac, other_maps))
            seed.start_value += difference
            seed.range -= difference

        containing_map: ConversionMap = map_that_contains_seed(seed, almanac[current_map.value])
        while containing_map:
            if seed.start_value + seed.range > containing_map.start_from_value + containing_map.range:
                calculated_value: int = get_destination_value(seed.start_value, containing_map)
                calculated_range: int  = containing_map.start_from_value + containing_map.range - seed.start_value
                calculated_values.append(calculate_value(InputRange(calculated_value, calculated_range), almanac, other_maps))
                seed.range = (seed.start_value + seed.range) - (containing_map.start_from_value + containing_map.range)
                seed.start_value = containing_map.start_from_value + containing_map.range
            else:
                destination_value: int = get_destination_value(seed.start_value, containing_map)
                calculated_values.append(calculate_value(InputRange(destination_value, seed.range), almanac, other_maps))
                seed.range = 0
                break

            containing_map = map_that_contains_seed(seed, almanac[current_map.value])

        if seed.range > 0:
            calculated_values.append(calculate_value(InputRange(seed.start_value, seed.range), almanac, other_maps))

        return sorted(calculated_values)[0]

    return calculate_value(seed, almanac, [
        Map.SED_TO_SOI,
        Map.SOI_TO_FRT,
        Map.FRT_TO_WTR,
        Map.WTR_TO_LGT,
        Map.LGT_TO_TMP,
        Map.TMP_TO_HUM,
        Map.HUM_TO_LOC,
    ])

almanac: dict = process_almanac(input)

lowest = math.inf

for seed in almanac['seeds']:
    location_number = get_smallest_location_by_seed(seed, almanac)
    lowest = location_number if location_number < lowest else lowest
print(lowest)
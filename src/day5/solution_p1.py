import math
from enum import Enum

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

text_file = open('input.txt', 'r')
input = list(filter(lambda s: s != '', text_file.read().split('\n')))

def process_almanac(input: list[str]) -> dict:
    almanac_input = {}
    almanac_input['seeds'] = list(map(int, input[0].split(': ')[-1].split(' ')))

    i: int = 1
    while i < len(input):
        if not input[i][0].isdigit():
            section_dict: dict = {}
            map_name = input[i].split(' ')[0]
            i += 1
            while i < len(input) and input[i][0].isdigit():
                dst, src, rng = map(int, input[i].split(' '))
                section_dict[src] = { 'start': dst, 'range': rng }
                i += 1
            almanac_input[map_name] = section_dict

    return almanac_input

def get_location_by_seed(seed_number: int, almanac: dict) -> int:
    def get_destination_value(source: int, conversion_map: dict) -> int:
        for key in conversion_map.keys():
            dest, range = conversion_map[key]['start'], conversion_map[key]['range']

            if int(key) <= source <= int(key) + range:
                offset: int = source - int(key)
                return dest + offset
        return source

    soil_number: int = get_destination_value(seed_number, almanac[Map.SED_TO_SOI.value])
    fertilizer_number: int = get_destination_value(soil_number, almanac[Map.SOI_TO_FRT.value])
    water_number: int = get_destination_value(fertilizer_number, almanac[Map.FRT_TO_WTR.value])
    light_number: int = get_destination_value(water_number, almanac[Map.WTR_TO_LGT.value])
    temperature_number: int = get_destination_value(light_number, almanac[Map.LGT_TO_TMP.value])
    humidity_number: int = get_destination_value(temperature_number, almanac[Map.TMP_TO_HUM.value])
    location_number: int = get_destination_value(humidity_number, almanac[Map.HUM_TO_LOC.value])

    return location_number



almanac: dict = process_almanac(input)

lowest = math.inf
for seed in almanac['seeds']:
    location_number = get_location_by_seed(seed, almanac)
    lowest = location_number if location_number < lowest else lowest

print(lowest)
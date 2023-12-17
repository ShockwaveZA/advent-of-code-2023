

input: str = 'rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7'

file = open('input.txt', 'r')
input = file.read().split('\n')[0]

def hash(string: str) -> int:
    value: int = 0
    for char in string:
        value += ord(char)
        value *= 17
        value %= 256
    return value

def process_step(boxes: dict[int, list[tuple]], word: str):
    if word.__contains__('='):
        label, focal_length = word.split('=')
        box_number: int = hash(label)

        if boxes.__contains__(box_number):
            found: bool = False
            for i in range(len(boxes[box_number])):
                if boxes[box_number][i][0] == label:
                    boxes[box_number][i] = (label, focal_length)
                    found = True
                    break
            if not found:
               boxes[box_number].append((label, focal_length))
        else:
            boxes[box_number] = [(label, focal_length)]

    if word.__contains__('-'):
        label = word[:-1]
        box_number: int = hash(label)
        if boxes.__contains__(box_number):
            for i in range(len(boxes[box_number])):
                if boxes[box_number][i][0] == label:
                    boxes[box_number].pop(i)
                    if len(boxes[box_number]) == 0:
                        del boxes[box_number]
                    break

    # print(f'After "{word}"')
    # for key in boxes.keys():
    #     print(f'Box {key}: {' '.join(map(lambda s: f'[{s}]', map(lambda t: f'{t[0]} {t[1]}', boxes[key])))}')
    # print()

def calculate_focusing_power(boxes: dict[int, list[tuple]]) -> int:
    total: int = 0
    for key in boxes.keys():
        for i in range(len(boxes[key])):
            label, focus_value = boxes[key][i]
            value: int = (key + 1) * (i + 1) * int(focus_value)

            # print(f'{label}: {key + 1} * {i + 1} * {focus_value} = {value}')
            total += value
    return total

all_boxes: dict[int, list[tuple]] = {}
for word in input.split(','):
    process_step(all_boxes, word)

print(calculate_focusing_power(all_boxes))

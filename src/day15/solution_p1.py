

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

total: int = 0
for word in input.split(','):
    value = hash(word)
    total += value

print(total)

from dataclasses import dataclass

input: list[str] = [
    'LLR',
    'AAA = (BBB, BBB)',
    'BBB = (AAA, ZZZ)',
    'ZZZ = (ZZZ, ZZZ)',
]

@dataclass
class Node:
    left: str
    right: str

input_file = open('input.txt', 'r')
input = list(filter(lambda s: s != '', input_file.read().split('\n')))

def initialize_map(input: list[str]) -> dict[str, Node]:
    trie: dict[str, Node] = {}

    for line in input:
        name, tupl = line.split(' = ')
        left, right = tupl[1:-1].split(', ')

        node: Node = Node(left, right)
        trie[name] = node
    return trie

directions, *nodes = input
trie: dict[str, Node] = initialize_map(nodes)

node: Node = trie['AAA']
is_end: bool = False
i: int = 0
steps: int = 1
while not is_end:
    for i in range(len(directions)):
        if directions[i] == 'L':
            if node.left == 'ZZZ':
                is_end = True
                break
            node = trie[node.left]
        else:
            if node.right == 'ZZZ':
                is_end = True
                break
            node = trie[node.right]
        steps += 1
        i = (i + 1) % len(directions)

print(steps)









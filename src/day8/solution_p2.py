from dataclasses import dataclass

input: list[str] = [
    'LR',
    '11A = (11B, XXX)',
    '11B = (XXX, 11Z)',
    '11Z = (11B, XXX)',
    '22A = (22B, XXX)',
    '22B = (22C, 22C)',
    '22C = (22Z, 22Z)',
    '22Z = (22B, 22B)',
    'XXX = (XXX, XXX)',
]

@dataclass
class Node:
    label: str
    left: str
    right: str

input_file = open('input.txt', 'r')
input = list(filter(lambda s: s != '', input_file.read().split('\n')))

def initialize_map(input: list[str]) -> dict[str, Node]:
    trie: dict[str, Node] = {}

    for line in input:
        name, tupl = line.split(' = ')
        left, right = tupl[1:-1].split(', ')

        node: Node = Node(name, left, right)
        trie[name] = node
    return trie

def is_all_nodes_at_end(steps: list[int]) -> bool:
    for i in steps:
        if i == -1:
            return False
    return True


def lcm_of_list(numbers: list[int]):
    def lcm(a: int, b: int):
        def gcd(a: int, b: int):
            while b:
                a, b = b, a % b
            return a

        return a * b // gcd(a, b)

    result: int = 1
    for number in numbers:
        result = lcm(result, number)
    return result

directions, *nodes = input
trie: dict[str, Node] = initialize_map(nodes)

iterating_nodes: list[Node] = list(map(lambda s: trie[s], filter(lambda s: s[-1] == 'A', trie.keys())))
steps_list: list[int] = list(map(lambda n: -1, iterating_nodes))
is_end: bool = False
i: int = 0
steps: int = 1
while not is_end:
    for i in range(len(directions)):
        if directions[i] == 'L':
            for k in range(len(iterating_nodes)):
                iterating_nodes[k] = trie[iterating_nodes[k].left]
                if iterating_nodes[k].label[-1] == 'Z':
                    steps_list[k] = steps

            if is_all_nodes_at_end(steps_list):
                is_end = True
                break
        else:
            for k in range(len(iterating_nodes)):
                iterating_nodes[k] = trie[iterating_nodes[k].right]
                if iterating_nodes[k].label[-1] == 'Z':
                    steps_list[k] = steps

            if is_all_nodes_at_end(steps_list):
                is_end = True
                break
        steps += 1
        i = (i + 1) % len(directions)

print(lcm_of_list(steps_list))

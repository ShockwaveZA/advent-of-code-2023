from dataclasses import dataclass

input: list[str] = [
	'32T3K 765',
	'T55J5 684',
	'KK677 28',
	'KTJJT 220',
	'QQQJA 483',
]

CARD_VALUES: dict[str, int] = {
	'A': 12,
	'K': 11,
	'Q': 10,
	'J': 9,
	'T': 8,
	'9': 7,
	'8': 6,
	'7': 5,
	'6': 4,
	'5': 3,
	'4': 2,
	'3': 1,
	'2': 0,
}

input_file = open('input.txt', 'r')
input = list(filter(lambda s: s != '', input_file.read().split('\n')))

@dataclass
class Entry:
	hand: str
	bid: int

def process_input(input: list[str]) -> list[Entry]:
	def map_entry(line: str) -> Entry:
		hand, bid = line.split(' ')
		return Entry(hand, int(bid))
	
	return list(map(map_entry, input))

def sort_entries(entries: list[Entry]) -> list[Entry]:
	def rank_hand(hand: str) -> int:
		def count_occurrences(hand: str) -> list[int]:
			counted_cards: dict[str, int] = {}
			for card in hand:
				if card in counted_cards.keys():
					continue

				counted_cards[card] = hand.count(card)
			counts = []
			for card in counted_cards.keys():
				counts.append(counted_cards[card])
			return sorted(counts)

		counts = count_occurrences(hand)

		# 5 of a kind
		if counts == [5]:
			return 6

		# 4 of a kind
		if counts == [1, 4]:
			return 5

		# Full house
		if counts == [2, 3]:
			return 4

		# 3 of a kind
		if counts == [1, 1, 3]:
			return 3

		# 2 pair
		if counts == [1, 2, 2]:
			return 2

		# 1 pair
		if counts == [1, 1, 1, 2]:
			return 1

		# High card
		return 0

	def compare_hands(hand1: str, hand2: str) -> int:
		rank1, rank2 = rank_hand(hand1), rank_hand(hand2)

		if rank1 == rank2:
			for i in range(len(hand1)):
				value1, value2 = CARD_VALUES[hand1[i]], CARD_VALUES[hand2[i]]

				if value1 == value2:
					continue

				return 1 if value1 < value2 else -1
			return 0

		return 1 if rank1 < rank2 else -1

	sorted_entries: list[Entry] = []
	for entry in entries:
		sorted_entries.append(entry)

	for i in range(len(sorted_entries) - 1):
		for j in range(i + 1, len(sorted_entries)):
			if compare_hands(sorted_entries[i].hand, sorted_entries[j].hand) == 1:
				temp = sorted_entries[i]
				sorted_entries[i] = sorted_entries[j]
				sorted_entries[j] = temp

	return sorted_entries

sorted_entries: list[Entry] = sort_entries(process_input(input))
total: int = 0
for i in range(len(sorted_entries)):
	rank = len(sorted_entries) - i
	total += rank * sorted_entries[i].bid

print(total)

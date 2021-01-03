def parse(filename):
	t1, t2 = open(filename).read().strip().split("\n\n")
	return tuple(map(lambda x: list(map(int, x.split("\n")[1:])), [t1, t2]))

def score(deck):
	res = 0
	for i in range(len(deck)):
		res += deck[i] * (len(deck)-i)
	return res

def solution1(deck1, deck2):
	while len(deck1) > 0 and len(deck2) > 0:
		p1, p2 = deck1[0], deck2[0]
		if p1 > p2:
			deck1 = deck1[1:] + [p1, p2]
			deck2 = deck2[1:]
		else:
			deck1 = deck1[1:]
			deck2 = deck2[1:] + [p2, p1]
	if len(deck1) > 0:
		return score(deck1)
	return score(deck2)

def can_recurse(deck1, deck2):
	p1, p2 = deck1[0], deck2[0]
	return p1 <= len(deck1) - 1 and p2 <= len(deck2) - 1

def combat(deck1, deck2):
	db = set()
	while len(deck1) > 0 and len(deck2) > 0:
		key = (tuple(deck1), tuple(deck2))
		if key in db:
			return "p1", score(deck1)
		db.add(key)

		p1, p2 = deck1[0], deck2[0]

		if can_recurse(deck1, deck2):
			winner, _ = combat(deck1[1:p1+1], deck2[1:p2+1])
		else:
			winner = "p1" if p1 > p2 else "p2"

		if winner == "p1":
			deck1 = deck1[1:] + [p1, p2]
			deck2 = deck2[1:]
		else:
			deck1 = deck1[1:]
			deck2 = deck2[1:] + [p2, p1]

	if len(deck1) > 0:
		return "p1", score(deck1)
	return "p2", score(deck2)

def solution2(deck1, deck2):
	return combat(deck1, deck2)[1]

def main():
	print(solution1(*parse("sample.txt")))
	print(solution1(*parse("input.txt")))

	print(solution2(*parse("sample.txt")))
	print(solution2(*parse("input.txt")))

if __name__ == "__main__":
	main()

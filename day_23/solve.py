def slice(cups, start):
	res = []
	for i in range(start, start+3):
		index = i % len(cups)
		res.append(cups[index])
	return res, [x for x in cups if x not in res]

def destination(cups, current, limit=9):
	def next(label):
		if label == 1:
			return limit
		return label - 1
	while next(current) not in cups:
		current = next(current)
	return cups.index(next(current))

def place(cups, dest, place):
	return cups[:dest+1] + place + cups[dest+1:]

def pretty_cups(cups, current):
	res = []
	for cup in cups:
		if cup == current:
			res.append(f"({cup})")
		else:
			res.append(str(cup))
	return " ".join(res)

def solution1(cups):
	picked_up = []
	current = cups[0]
	for z in range(100):
		# print(f"-- move {z+1} --")
		# print(f"cups: {pretty_cups(cups, current)}")
		# pick up 3 cups
		picked_up, cups = slice(cups, cups.index(current)+1)
		# print(f"pick up: {', '.join(list(map(str, picked_up)))}")

		# pick destination
		dest = destination(cups, current)
		# print(f"destination: {cups[dest]}")

		# place picked up cups at destination
		cups = place(cups, dest, picked_up)

		current = cups[(cups.index(current) + 1) % len(cups)]

	start = cups.index(1)
	res = ""
	for i in range(start+1, start+len(cups)):
		res = res + str(cups[i % len(cups)])
	return res

class Node(object):
	def __init__(self, number):
		self.number = number
		self.left = None
		self.right = None

class LinkedList(object):
	def __init__(self, nodes):
		self.db = {}
		prev = nodes[-1]
		for node in nodes:
			self.db[node.number] = node
			node.left = prev
			prev.right = node
			prev = node
	
	def slice(self, start, size=3):
		res = [start.right]
		for i in range(size-1):
			res.append(res[-1].right)
		start.right = res[-1].right
		res[-1].right.left = start

		for node in res:
			del self.db[node.number]
		return res

	def insert(self, start, nodes):
		nodes[-1].right = self.db[start].right
		nodes[-1].right.left = nodes[-1]
		self.db[start].right = nodes[0]
		nodes[0].left = self.db[start]
		for node in nodes:
			self.db[node.number] = node

	def destination(self, number):
		def next(num):
			if num == 1:
				return 1000000
			return num - 1
		while next(number) not in self.db:
			number = next(number)
		return next(number)

	def get(self, num):
		return self.db[num]

	def pretty(self, start):
		res = [f"({start.number})"] 
		curr = start.right
		while curr != start:
			res.append(str(curr.number))
			curr = curr.right
		return " ".join(res)
		

def solution2(cups):
	begin = cups[0]
	cups = LinkedList(list(map(Node, cups + list(range(max(cups)+1, 1000001)))))
	# cups = LinkedList(list(map(Node, cups)))

	current = cups.get(begin)
	for z in range(10000000):
		# print(f"-- move {z+1} --")
		# print(f"cups: {cups.pretty(current)}")
		# pick up 3 cups
		picked_up = cups.slice(current)
		# print(f"pick up: {', '.join(list(map(lambda x: str(x.number), picked_up)))}")

		# pick destination
		dest = cups.destination(current.number)
		# print(f"destination: {dest}")

		# place picked up cups at destination
		cups.insert(dest, picked_up)

		current = current.right

	start = cups.get(1)
	c1, c2 = start.right.number, start.right.right.number
	return c1, c2, c1 * c2

def main():
	# print(solution1(list(map(int, "389125467"))))
	print(solution2(list(map(int, "389125467"))))
	print(solution2(list(map(int, "942387615"))))

if __name__ == "__main__":
	main()
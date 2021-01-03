class Bag(object):

	def __init__(self, color):
		self.color = color
		self.children = []
		self.parents = []

	def add_child(self, child, count):
		self.children.append((child, count))
		child.parents.append((self, count))

	def add_parent(self, parent, count):
		self.parents.append((parent, count))
		parent.children.append((self, count))

class BagDatabase(object):

	def __init__(self):
		self.db = {}

	def get_bag(self, color):
		if color not in self.db:
			self.db[color] = Bag(color)
		return self.db[color]

def parse(rules):
	database = BagDatabase()
	for rule in rules:
		bag_color = rule.split("contain")[0].strip()[:-5]
		bag = database.get_bag(bag_color)
		if rule.split("contain")[1].strip(" .") == "no other bags":
			continue
		for child_rule in rule.split("contain")[1].strip().split(","):
			count = int(child_rule.split()[0])
			color = " ".join(child_rule.split()[1:-1])
			bag.add_child(database.get_bag(color), count)
	return database

def find_ancestors(database, color):
	visited = set()
	queue = list(map(lambda x: x[0], database.get_bag(color).parents))
	while queue:
		bag = queue[0]
		visited.add(bag)
		for parent in bag.parents:
			if parent[0] not in visited:
				queue.append(parent[0])
		del queue[0]
	return visited

def find_descendants(bag):
	if len(bag.children) == 0:
		return 0
	counter = 0
	for child, count in bag.children:
		# print(f"count: {count}, child: {child.color}, counter: {counter}")
		counter = counter + count + (count * find_descendants(child))
	return counter
	

def solution1(rules):
	database = parse(rules)
	return len(find_ancestors(database, "shiny gold"))

def solution2(rules):
	database = parse(rules)
	# for color in database.db.keys():
	# 	print(f"Descendants for {color}: {find_descendants(database.get_bag(color))}")
	return find_descendants(database.get_bag("shiny gold"))

print(solution1(open("sample.txt").read().strip().split("\n")))
print(solution1(open("input.txt").read().strip().split("\n")))

print(solution2(open("sample.txt").read().strip().split("\n")))
print(solution2(open("sample2.txt").read().strip().split("\n")))
print(solution2(open("input.txt").read().strip().split("\n")))
from itertools import combinations

def _binify(number):
	return ("0",)*(36-len(bin(number)[2:])) + tuple(bin(number)[2:])

def parse(filename):
	instructions = []
	for line in open(filename).read().strip().split("\n"):
		lhs, rhs = line.split(" = ")
		if lhs == "mask":
			yield ("mask", rhs)
		else:
			addr = _binify(int(lhs.split("[")[1][:-1]))
			val = _binify(int(line.split(" = ")[1]))
			yield (addr, val)

def mask_value(mask, value):
	result = []
	for i in range(1, len(mask)+1):
		if mask[-i] == "X":
			result.append(value[-i])
		else:
			result.append(mask[-i])
	return int("".join(tuple(reversed(result))), 2)

def solution1(instructions):
	db = {}
	mask = None
	for lhs, rhs in instructions:
		if lhs == "mask":
			mask = rhs
		else:
			db[lhs] = mask_value(mask, rhs)
	return sum(db.values())

def mask_addr(mask, addr):
	result = []
	for i in range(1, len(mask)+1):
		if mask[-i] == "0":
			result.append(addr[-i])
		else:
			result.append(mask[-i])
	return tuple(reversed(result))

def intersect(addr1, addr2):
	result = []
	for i in range(36):
		if addr1[i] == "X":
			result.append(addr2[i])
		elif addr2[i] == "X":
			result.append(addr1[i])
		elif addr1[i] == addr2[i]:
			result.append(addr1[i])
		else:
			return None
	return tuple(result)

def exclude(addr1, addr2):
	lookup = {"1": "0", "0": "1"}
	excluded = []
	singleXs = []
	for i in range(36):
		a, b = addr1[i], addr2[i]
		if a == "X" and b == "X":
			excluded.append("X")
		elif a == "X":
			singleXs.append(i)
			excluded.append(b)
		elif b == "X":
			singleXs.append(i)
			excluded.append(a)
		elif a == b:
			excluded.append(a)
		else:
			raise Exception("Invalid input")
	for r in range(len(singleXs)):
		for xs in combinations(singleXs, r+1):
			temp = excluded.copy()
			for i in xs:
				temp[i] = lookup[temp[i]]
			yield tuple(temp)

def update(old_db, addr, value):
	db = {}
	for prev_addr in old_db.keys():
		if prev_addr == addr:
			continue
		common_addr = intersect(addr, prev_addr)
		if not common_addr:
			db[prev_addr] = old_db[prev_addr]
			continue
		new_addrs = exclude(prev_addr, common_addr)
		for new_addr in new_addrs:
			db[new_addr] = old_db[prev_addr]
	db[addr] = value
	return db

def solution2(instructions):
	db = {}
	mask = None
	for lhs, rhs in instructions:
		if lhs == "mask":
			mask = rhs
			continue
		db = update(db, mask_addr(mask, lhs), int("".join(rhs), 2))
	return sum([(2 ** key.count("X")) * db[key] for key in db])

print(solution1(parse("sample.txt")))
print(solution1(parse("input.txt")))

print(solution2(parse("sample2.txt")))
print(solution2(parse("input.txt")))
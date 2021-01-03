import operator

def parse(filename):
	for line in open(filename).read().strip().split():
		yield (line[0], int(line[1:]))

def _turn(facing, direction, degree):
	offset = {90: 1, 180: 2, 270: 3, "R": 1, "L": -1}
	cardinals = ["E", "S", "W", "N"]
	return cardinals[(cardinals.index(facing) + offset[direction] * offset[degree]) % 4]
	
def _execute(x, y, facing, code, arg):
	dirs = {"N": (0, 1), "S": (0, -1), "E": (1, 0), "W": (-1, 0)}
	if code in dirs.keys():
		x += dirs[code][0] * arg
		y += dirs[code][1] * arg
	elif code in ("L", "R"):
		facing = _turn(facing, code, arg)
	elif code == "F":
		x += dirs[facing][0] * arg
		y += dirs[facing][1] * arg
	return x, y, facing

def solution1(instructions):
	facing = "E"
	x ,y = 0, 0
	for instruction in instructions:
		x, y, facing = _execute(x, y, facing, *instruction)
	return abs(x) + abs(y)

def _execute2(ship, waypoint, code, arg):
	dirs = {"N": (0, 1), "S": (0, -1), "E": (1, 0), "W": (-1, 0)}
	print(f"ship: {ship}, waypoint: {waypoint}. Applying {code} {arg}")
	if code in dirs.keys():
		waypoint = tuple(map(operator.add, waypoint, (dirs[code][0] * arg, dirs[code][1] * arg)))
	elif code in ("L", "R"):
		dir1 = "E" if waypoint[0] > 0 else "W"
		dir2 = "N" if waypoint[1] > 0 else "S"
		comp1 = tuple([abs(waypoint[0]) * x for x in dirs[_turn(dir1, code, arg)]])
		comp2 = tuple([abs(waypoint[1]) * x for x in dirs[_turn(dir2, code, arg)]])
		# print(f"dir1: {dir1}, comp1: {comp1}, dir2: {dir2}, comp2: {comp2}")
		waypoint = tuple(map(operator.add, comp1, comp2))
	elif code == "F":
		ship = tuple(map(operator.add, ship, tuple(map(lambda x: x*arg, waypoint))))
	return ship, waypoint

def solution2(instructions):
	waypoint= (10, 1)
	ship= (0, 0)
	for instruction in instructions:
		ship, waypoint= _execute2(ship, waypoint, *instruction)
	print(f"Final ship position: {ship}")
	return sum(map(abs, ship))

print(solution2(parse("sample.txt")))
print(solution2(parse("input.txt")))
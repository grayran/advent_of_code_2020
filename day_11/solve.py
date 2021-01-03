import itertools

def parse(filename):
	return list(map(list, open(filename).read().strip().split("\n")))

def _exists(grid, x, y):
	return 0 <= x < len(grid[0]) and 0 <= y < len(grid)

def _neighbors(grid, x, y):
	adjacents = {".": 0, "L": 0, "#": 0}
	for i in range(-1, 2):
		for j in range(-1, 2):
			if i == 0 and j == 0:
				continue
			if _exists(grid, x+i, y+j):
				adjacents[grid[y+j][x+i]] += 1
	return adjacents

def _next1(grid):
	new_grid = []
	for y in range(len(grid)):
		new_row = []
		for x in range(len(grid[0])):
			adjacents = _neighbors(grid, x, y)
			seat = grid[y][x]
			if seat == "L" and adjacents["#"] == 0:
				new_row.append("#")
			elif seat == "#" and adjacents["#"] >= 4:
				new_row.append("L")
			else:
				new_row.append(seat)
		new_grid.append(new_row)
	return new_grid

def _grid_stats(grid):
	stats = {".": 0, "L": 0, "#": 0}
	for row in grid:
		for seat in row:
			stats[seat] += 1
	return stats

def _visible_seats(grid, col, row):
	stats = {".": 0, "L": 0, "#": 0}
	slopes = list(itertools.product([-1, 0, 1], [-1, 0, 1]))
	slopes.remove((0, 0))
	for i, j in slopes:
		x, y = col, row
		while _exists(grid, x+i, y+j):
			x += i
			y += j
			seat = grid[y][x]
			if seat != ".":
				stats[grid[y][x]] += 1
				break
	return stats	

def _next2(grid):
	new_grid = []
	for y in range(len(grid)):
		new_row = []
		for x in range(len(grid[0])):
			visible_seats = _visible_seats(grid, x, y)
			seat = grid[y][x]
			if seat == "L" and visible_seats["#"] == 0:
				new_row.append("#")
			elif seat == "#" and visible_seats["#"] >= 5:
				new_row.append("L")
			else:
				new_row.append(seat)
		new_grid.append(new_row)
	return new_grid
			

def solution1(grid):
	next_grid = _next1(grid)
	while next_grid != grid:
		grid = next_grid
		next_grid = _next1(next_grid)
	return _grid_stats(grid)["#"]

def solution2(grid):
	next_grid = _next2(grid)
	while next_grid != grid:
		grid = next_grid
		next_grid = _next2(next_grid)
	return _grid_stats(grid)["#"]

print(solution2(parse("sample.txt")))
print(solution2(parse("input.txt")))
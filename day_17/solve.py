def parse(filename):
	grid = {}
	row = 0
	for line in open(filename).read().strip().split("\n"):
		col = 0
		for c in line:
			grid[(row, col, 0)] = c
			col += 1
		row += 1
	return grid

def parse2(filename):
	grid = {}
	row = 0
	for line in open(filename).read().strip().split("\n"):
		col = 0
		for c in line:
			grid[(row, col, 0, 0)] = c
			col += 1
		row += 1
	return grid

def adjacents1(w, x, y):
	for i in [-1, 0, 1]:
		for j in [-1, 0, 1]:
			for k in [-1, 0, 1]:
				if i != 0 or j != 0 or k != 0:
					yield (x+i, y+j, z+k)

def adjacents2(w, x, y, z):
	for i in [-1, 0, 1]:
		for j in [-1, 0, 1]:
			for k in [-1, 0, 1]:
				for l in [-1, 0, 1]:
					if i != 0 or j != 0 or k != 0 or l != 0:
						yield (w+i, x+j, y+k, z+l)

def _execute(grid):
	new_grid = {}
	cells = list(grid.keys())
	for k in grid.keys():
		cells.extend(list(adjacents(*k)))
	for coords in cells:
		active_adjs = 0
		inactive_adjs = 0
		for adj in adjacents(*coords):
			if adj not in grid or grid[adj] == ".":
				inactive_adjs += 1
			else:
				active_adjs += 1
		if coords not in grid:
			grid[coords] = "."
		if grid[coords] == "#" and active_adjs not in (2, 3):
			new_grid[coords] = "."
		elif grid[coords] == "." and active_adjs == 3:
			new_grid[coords] = "#"
		else:
			new_grid[coords] = grid[coords]
	return new_grid

def _execute2(grid):
	new_grid = {}
	cells = list(grid.keys())
	for k in grid.keys():
		cells.extend(list(adjacents2(*k)))
	for coords in cells:
		active_adjs = 0
		inactive_adjs = 0
		for adj in adjacents2(*coords):
			if adj not in grid or grid[adj] == ".":
				inactive_adjs += 1
			else:
				active_adjs += 1
		if coords not in grid:
			cell = "."
		else:
			cell = grid[coords]
		if cell == "#" and active_adjs not in (2, 3):
			# new_grid[coords] = "."
			pass
		elif cell == "." and active_adjs == 3:
			new_grid[coords] = "#"
		else:
			new_grid[coords] = cell
	return new_grid
	
	
def solution2(grid):
	for i in range(6):
		print(f"Iteration #{i+1}")
		grid = _execute2(grid)
	return list(grid.values()).count("#")
	
def solution1(grid):
	for i in range(6):
		grid = _execute(grid)
	return list(grid.values()).count("#")

print(solution2(parse2("sample.txt")))
print(solution2(parse2("input.txt")))
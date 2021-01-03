from collections import namedtuple

Slope = namedtuple("Slope", ["x", "y"])

def solution1(grid, slope):
	x = 0
	counter = 0
	for y in range(slope.y, len(grid), slope.y):
		row = grid[y]
		x = (x + slope.x) % len(row)
		if row[x] == '#':
			counter += 1
	return counter

def solution2(grid, slopes):
	result = 1
	for slope in slopes:
		print(f"<--- Slope(x={slope.x}, y={slope.y}) result = {solution1(grid, slope)} --->")
		result *= solution1(grid, slope)
	return result

input_grid = open("input.txt").read().strip().split("\n")
sample_grid = open("sample.txt").read().strip().split("\n")

print(solution1(input_grid, Slope(x=3, y=1)))
print(solution1(sample_grid, Slope(x=3, y=1)))

slopes = [
	Slope(x=1, y=1),
	Slope(x=3, y=1),
	Slope(x=5, y=1),
	Slope(x=7, y=1),
	Slope(x=1, y=2),
]

print(solution2(input_grid, slopes))
print(solution2(sample_grid, slopes))
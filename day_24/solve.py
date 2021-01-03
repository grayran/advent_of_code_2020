def locate(directions):
	x, y = 0, 0
	for direction in directions:
		if direction == "e":
			x += 2
		elif direction == "w":
			x -= 2
		elif direction[1] == "e":
			x += 1
		elif direction[1] == "w":
			x -= 1
		
		if direction[0] == "n":
			y += 1
		elif direction[0] == "s":
			y -= 1
	return x, y

def parse(filename):
	tiles = {}
	for line in open(filename).read().strip().split():
		directions = []
		counter = 0
		while counter < len(line):
			if line[counter] in ("e", "w"):
				directions.append(line[counter])
				counter += 1
			elif line[counter] in ("n", "s"):
				directions.append(line[counter:counter+2])
				counter += 2
		coords = locate(directions)
		if coords in tiles:
			tiles[coords].is_black = not tiles[coords].is_black
		else:
			tiles[coords] = HexTile(coords[0], coords[1], True)
	return tiles


class HexTile(object):
	def __init__(self, x, y, is_black=True):
		self.is_black = is_black
		self.x = x
		self.y = y

	def _get_neighbor_coords(self, direction):
		if direction == "e":
			return self.x + 2, self.y
		elif direction == "w":
			return self.x - 2, self.y
		elif direction == "ne":
			return self.x + 1, self.y + 1
		elif direction == "nw":
			return self.x - 1, self.y + 1
		elif direction == "se":
			return self.x + 1, self.y - 1
		elif direction == "sw":
			return self.x - 1, self.y - 1
		else:
			raise Exception(f"Invalid direction {direction}")

	def is_neighbor_black(self, direction, tile_db):
		coords = self._get_neighbor_coords(direction)
		if coords in tile_db:
			return tile_db[coords].is_black
		return False

	def next_tile(self, tile_db):
		adj_colors = {True: 0, False: 0}
		for d in ("e", "w", "ne", "nw", "se", "sw"):
			adj_colors[self.is_neighbor_black(d, tile_db)] += 1
		if self.is_black and adj_colors[True] == 0 or adj_colors[True] > 2:
			return HexTile(self.x, self.y, False)
		elif not self.is_black and adj_colors[True] == 2:
			return HexTile(self.x, self.y, True)
		return HexTile(self.x, self.y, self.is_black)


def solution2(tile_db):
	for z in range(100):
		new_tile_db = {}
		for coords in tile_db:
			next = tile_db[coords].next_tile(tile_db)
			if next.is_black:
				new_tile_db[coords] = next
			for d in ("e", "w", "ne", "nw", "se", "sw"):
				neighbor_coords = tile_db[coords]._get_neighbor_coords(d)
				if neighbor_coords in tile_db:
					continue
				neighbor_tile = HexTile(*neighbor_coords, False)
				neighbor_next = neighbor_tile.next_tile(tile_db)
				if neighbor_next.is_black:
					new_tile_db[neighbor_coords] = neighbor_next

		tile_db = new_tile_db
	return sum([1 for tile in tile_db.values() if tile.is_black])

def solution1(tile_db):
	return sum([1 for tile in tile_db.values() if tile.is_black])

def main():
	print(solution1(parse("sample.txt")))
	print(solution1(parse("input.txt")))
	print(solution2(parse("sample.txt")))
	print(solution2(parse("input.txt")))

if __name__ == "__main__":
	main()
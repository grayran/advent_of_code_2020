from functools import cached_property
from typing import List

from models import Tile

TILE_SIZE = 8

class TileDB(object):
    def __init__(self):
        self._db = {}

    def size(self):
        return len(self._db)

    def add(self, tile: Tile):
        self._db[tile.number] = tile

    def get(self, tile_number) -> Tile:
        return self._db[tile_number]

    def numbers(self) -> List[int]:
        return list(self._db.keys())

    def tiles(self) -> List[Tile]:
        return list(self._db.values())

    @cached_property
    def all_edges(self):
        all_edges = {}
        for tile in self.tiles():
            for edge in tile.all_possible_edges:
                if edge not in all_edges:
                    all_edges[edge] = set()
                all_edges[edge].add(tile.number)
        return all_edges


class Grid(object):
    def __init__(self, tile_db: TileDB, grid_width: int):
        self.tile_db = tile_db
        self.grid_width = grid_width
        self.grid = []
        for i in range(grid_width):
            self.grid.append([])
            for j in range(grid_width):
                self.grid[-1].append(None)

    def get(self, x: int, y: int) -> str:
        tile_row = x // TILE_SIZE
        tile_col = y // TILE_SIZE
        tile_offset_x = x % TILE_SIZE
        tile_offset_y = y % TILE_SIZE
        return self.tile_db.get(self.get_tile(tile_row, tile_col)).body[tile_offset_x][tile_offset_y]

    def as_list(self):
        grid = []
        for i in range(TILE_SIZE * self.grid_width):
            grid.append([])
            for j in range(TILE_SIZE * self.grid_width):
                grid[-1].append(self.get(i, j))
        return grid

    def in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < TILE_SIZE * self.grid_width and 0 <= y < TILE_SIZE * self.grid_width

    def get_tile(self, x: int, y: int) -> int:
        return self.grid[x][y]

    def put_tile(self, x: int, y: int, tile_number: int):
        self.grid[x][y] = tile_number

    def pretty(self):
        out = []
        for row in self.grid:
            line = []
            for cell in row:
                line.append(str(cell))
            out.append(" ".join(line))
        return "\n".join(["GRID:"] + out)


class Image(object):
    def __init__(self, grid_width):
        self.grid_width = grid_width
        self.grid = []
        for i in range(grid_width):
            self.grid.append([])
            for j in range(grid_width):
                self.grid[-1].append(None)

    def flip(self):
        new_grid = []
        for i in range(self.grid_width):
            new_grid.append([])
            for j in range(self.grid_width):
                new_grid[-1].append(self.grid[self.grid_width-1-i][j])
        self.grid = new_grid

    def rotate(self):
        new_grid = []
        for i in range(self.grid_width):
            new_grid.append([])
            for j in range(self.grid_width):
                new_grid[-1].append(self.grid[self.grid_width-1-j][i])
        self.grid = new_grid

    def in_bounds(self, x: int, y: int) -> str:
        return 0 <= x < self.grid_width and 0 <= y < self.grid_width

    def get(self, x: int, y: int) -> str:
        return self.grid[x][y]

    def put(self, x: int, y: int, c: str):
        self.grid[x][y] = c

    def copy(self):
        image = Image(self.grid_width)
        for i in range(self.grid_width):
            for j in range(self.grid_width):
                image.put(i, j, self.grid[i][j])
        return image

    @staticmethod
    def from_grid(grid: Grid):
        print(f"Image dimensions: {grid.grid_width * TILE_SIZE}x{grid.grid_width * TILE_SIZE}")
        image = Image(grid.grid_width * TILE_SIZE)
        for i in range(TILE_SIZE * grid.grid_width):
            for j in range(TILE_SIZE * grid.grid_width):
                image.put(i, j, grid.get(i, j))
        return image

    def pretty(self):
        out = []
        for row in self.grid:
            line = []
            for cell in row:
                line.append(str(cell))
            out.append(" ".join(line))
        return "\n".join(["IMAGE:"] + out)

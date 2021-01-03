from datastore import TileDB, Grid, Image
from models import Tile, Edge


DRAGON = [[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#', ' '],
['#', ' ', ' ', ' ', ' ', '#', '#', ' ', ' ', ' ', ' ', '#', '#', ' ', ' ', ' ', ' ', '#', '#', '#'],
[' ', '#', ' ', ' ', '#', ' ', ' ', '#', ' ', ' ', '#', ' ', ' ', '#', ' ', ' ', '#', ' ', ' ', ' ']]


def parse(filename: str) -> TileDB:
    tile_defs = open(filename).read().strip().split("\n\n")
    tiles = TileDB()
    for tile_def in tile_defs:
        tile_def = tile_def.split("\n")
        tile_id = int(tile_def[0].strip().split()[1][:-1])
        tile_def = tuple(map(tuple, tile_def[1:]))
        tiles.add(Tile(tile_id, tile_def))
    return tiles


def partition_tiles(tile_db: TileDB):
    corners = list(set([tile.number for tile in tile_db.tiles() if tile.lone_edge_count(tile_db) == 2]))
    sides = list(set([tile.number for tile in tile_db.tiles() if tile.lone_edge_count(tile_db) == 1]))
    middle = list(set([tile.number for tile in tile_db.tiles() if tile.lone_edge_count(tile_db) == 0]))
    return corners, sides, middle


def _arrange_top_left_corner_tile(tile_db: TileDB, corner: Tile):
    lone_edges = corner.lone_edges(tile_db)
    times = 0
    while lone_edges not in [(Edge.U, Edge.L), (Edge.L, Edge.U)]:
        times += 1
        lone_edges = tuple([Edge((edge.value + 1) % 4) for edge in lone_edges])
    corner.rotate(times=times)


def _place_side_tile(grid: Grid, tile_db: TileDB, x: int, y: int, side: Edge):
    if x == 0 and y == 0:
        return grid.get_tile(0, 0)

    # print(f"Placing tile ({x}, {y}) on edge: {side.name}")

    if side in (Edge.U, Edge.D):
        previous = tile_db.get(grid.get_tile(x, y - 1))
        connecting_side = Edge.L
        matching_edge = tuple(reversed(previous.get_edge(Edge.R)))
    elif side in (Edge.L, Edge.R):
        previous = tile_db.get(grid.get_tile(x - 1, y))
        connecting_side = Edge.U
        matching_edge = tuple(reversed(previous.get_edge(Edge.D)))
    else:
        raise Exception("Illegal side value: ", side)

    neighbor_candidates = [x for x in tile_db.all_edges[matching_edge] if x != previous.number]

    if len(neighbor_candidates) != 1:
        raise Exception(f"Can't work with {len(neighbor_candidates)} neighbors: {neighbor_candidates}")

    tile = tile_db.get(neighbor_candidates[0])

    if matching_edge not in tile.edges:
        # print(f"Flipping tile {tile.number}")
        tile.flip()
    if matching_edge not in tile.edges:
        print(tile.pretty())
        raise Exception(f"Can't find edge {''.join(matching_edge)} even after flipping {tile.number}")

    count = 0
    while tile.get_edge(connecting_side) != matching_edge:
        tile.rotate()
        if count > 4:
            print(tile.pretty())
            raise Exception(f"Can't find edge {''.join(matching_edge)} even after rotating {tile.number}")

    grid.put_tile(x, y, tile.number)
    return tile.number


def assemble_grid(tile_db: TileDB):
    grid_width = int(tile_db.size() ** 0.5)
    grid = Grid(tile_db, grid_width)
    if grid_width == 1:
        # print("Found a 1-grid")
        grid.put_tile(0, 0, tile_db.numbers()[0])
        return grid

    corners, sides, middle = partition_tiles(tile_db)

    _arrange_top_left_corner_tile(tile_db, tile_db.get(corners[0]))
    grid.put_tile(0, 0, corners[0])

    placed_tiles = set()

    for offset in range(grid_width//2+1):
        # print("Placing top row and left column.")
        for i in range(offset, grid_width-offset):
            placed_tiles.add(_place_side_tile(grid, tile_db, offset, i, Edge.U))
            placed_tiles.add(_place_side_tile(grid, tile_db, i, offset, Edge.L))
            # print("\n".join(["UPDATED_GRID:", grid.pretty()]))

        # print("Placing bottom row and right column.")
        for i in range(1+offset, grid_width-offset):
            placed_tiles.add(_place_side_tile(grid, tile_db, grid_width-offset-1, i, Edge.D))
            placed_tiles.add(_place_side_tile(grid, tile_db, i, grid_width-offset-1, Edge.R))
            # print("\n".join(["UPDATED_GRID:", grid.pretty()]))

    return grid


def check_dragon(image: Image, x: int, y: int):
    for i in range(len(DRAGON)):
        for j in range(len(DRAGON[i])):
            if not image.in_bounds(x + i, y + j):
                return False
            if DRAGON[i][j] == "#" and image.get(x+i, y+j) != "#":
                return False
    return True


def locate_dragons(image: Image):
    indices = []
    for x in range(8 * image.grid_width):
        for y in range(8 * image.grid_width):
            if check_dragon(image, x, y):
                indices.append((x, y))
    return indices


def fill_dragons(image: Image, indices):
    image = image.copy()
    for x, y in indices:
        for i in range(len(DRAGON)):
            for j in range(len(DRAGON[i])):
                if not image.in_bounds(x + i, y + j):
                    print(f"error: x={x}, y={y}, i: {i}, j: {j}")
                    raise Exception("Unexpected out of bounds while filling")
                if DRAGON[i][j] == "#":
                    if image.get(x + i, y + j) not in ("#", "O"):
                        print(f"error: x={x}, y={y}, i: {i}, j: {j}")
                        raise Exception("Unexpected mismatch while filling")
                    image.put(x+i, y+j, "O")
    return image


def calculate_roughness(image: Image):
    return sum([row.count("#") for row in image.grid])


def find_dragon(image: Image):
    indices = locate_dragons(image)
    for i in range(4):
        if len(indices) != 0:
            print(f"Breaking because indices = {indices}")
            break
        print(f"Rotating {i+1} times")
        image.rotate()
        indices = locate_dragons(image)

    if len(indices) == 0:
        print(f"Flipping the image")
        image.flip()
        indices = locate_dragons(image)
        for i in range(4):
            if len(indices) != 0:
                print(f"Breaking because indices = {indices}")
                break
            print(f"Rotating again {i + 1} times")
            image.rotate()
            indices = locate_dragons(image)

    filled_image = fill_dragons(image, indices)
    print(image.pretty())

    return calculate_roughness(filled_image)


def main():
    tile_db = parse("input.txt")
    grid = assemble_grid(tile_db)
    print(grid.pretty())

    for tile in tile_db.tiles():
        tile.shed()

    image = Image.from_grid(grid)
    print(image.pretty())
    print("DRAGON_COUNT:", find_dragon(image))

if __name__ == "__main__":
    main()
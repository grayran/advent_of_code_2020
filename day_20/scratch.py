from functools import reduce
import operator


class Tile(object):
    def __init__(self, tile_id, tile_def):
        self.tile_id = tile_id
        self.tile_def = tile_def
        self.edges = (tile_def[0], tuple(reversed(tile_def[-1])), tuple(reversed([x[0] for x in tile_def])),
                      tuple([x[-1] for x in tile_def]))
        self.adjacents = [None] * 4

    def get_edges(self):
        return self.edges

    def merge(self, tile_id, merging_edge):
        for i in range(4):
            if self.edges[i] == merging_edge:
                self.adjacents[i] = tile_id
                return
        raise Exception("Can't merge")

    def is_connected(self, tile_id):
        return tile_id in self.adjacents


class EdgeDB(object):
    def __init__(self):
        self.db = {}

    def add(self, edge, tile_id):
        if edge not in self.db:
            self.db[edge] = []
        self.db[edge].append(tile_id)

    def ref_count(self, edge):
        if edge not in self.db:
            return 0
        return len(self.db[edge])

    def edges(self):
        return self.db.keys()


def parse(filename):
    tile_defs = open(filename).read().strip().split("\n\n")
    tiles = {}
    for tile_def in tile_defs:
        tile_def = tile_def.split("\n")
        tile_id = int(tile_def[0].strip().split()[1][:-1])
        tile_def = tuple(map(tuple, tile_def[1:]))
        tiles[tile_id] = Tile(tile_id, tile_def)
    return tiles


def original_edge_db(tiles):
    edge_db = EdgeDB()
    for tile_id in tiles:
        for edge in tiles[tile_id].get_edges():
            edge_db.add(edge, tile_id)
    return edge_db


def all_edge_db(tiles):
    edge_db = EdgeDB()
    for tile_id in tiles:
        for edge in tiles[tile_id].get_edges():
            edge_db.add(edge, tile_id)
            edge_db.add(tuple(reversed(edge)), tile_id)
    return edge_db


def divide_tiles(tile_db, all_edges):
    edge_count_db = {}
    for tile_id in tile_db:
        edges = tile_db[tile_id].edges
        lone_edge_count = 0
        for edge in edges:
            if len(all_edges._db[edge]) == 1:
                lone_edge_count += 1
        if lone_edge_count not in edge_count_db:
            edge_count_db[lone_edge_count] = []
        edge_count_db[lone_edge_count].append(tile_id)

    return edge_count_db[2], edge_count_db[1], edge_count_db[0]


def rotate_tile(tile, tile_db, all_edges, target_edges):
    if any([e not in tile.edges for _, e in target_edges]):
        print("\n".join(map(lambda x: "".join(x), tile.edges)))
        print("target_edges: ")
        print("\n".join(map(lambda x: "".join(x[1]), target_edges)))
        raise Exception("CAN'T ROTATE TILE")

    new_tile = tile
    for x in range(4):
        all_match = False
        # print(f"Rotating {x}")
        # print(f"old_tile_edges:")
        # print("\n".join(list(map(lambda x: "".join(x), tile.edges))))
        # print(f"new_tile_edges:")
        # print("\n".join(list(map(lambda x: "".join(x), new_tile.edges))))
        for target_index, target_edge in target_edges:
            if new_tile.edges[target_index] != target_edge:
                all_match = False
                break
            else:
                tile_db[tile.tile_id] = new_tile
                all_match = True
        if all_match:
            return new_tile

        new_tile_def = []
        # print(f"old_tile_def:")
        # print("\n".join(list(map(lambda x: "".join(x), new_tile.tile_def))))
        for i in range(10):
            row = []
            for j in range(10):
                row.append(new_tile.tile_def[9 - j][i])
            new_tile_def.append(tuple(row))
        new_tile = Tile(new_tile.tile_id, tuple(new_tile_def))
    # print(f"new_tile_def:")
    # print("\n".join(list(map(lambda x: "".join(x), new_tile_def))))

    raise Exception("Can't satisfy requirements by rotating")


def flip_tile(tile, want_edge, tile_db):
    if want_edge in tile.edges:
        return tile

    new_tile_def = []
    for i in range(10):
        row = []
        for j in range(10):
            row.append(tile.body[9 - i][j])
        new_tile_def.append(tuple(row))
    tile_db[tile.tile_id] = Tile(tile.tile_id, tuple(new_tile_def))

    if want_edge not in tile_db[tile.tile_id].edges:
        raise Exception(f"Even flipping {tile_id} didn't yield {''.join(want_edge)}")

    return tile_db[tile.tile_id]


def merge_edge_tiles(prev, tile_db, all_edges, edge_index):
    lookup = {0: 1, 1: 0, 2: 3, 3: 2}
    print(f"Merging tile: {prev.tile_id} on edge {edge_index}")
    edge = prev.edges[edge_index]
    neighbors = [x for x in all_edges._db[edge] if x != prev.tile_id]

    if len(neighbors) < 1:
        raise Exception(f"Can't find any neighbors for edge: {edge}")
    elif len(neighbors) > 1:
        print(f"Found multiple candidates: {neighbor}")
        raise Exception(f"Can't find any neighbors for edge: {edge}")

    neighbor_id = neighbors[0]

    print(f"Found neighbor: {neighbor_id}")
    neighbor = tile_db[neighbor_id]

    if edge not in neighbor.edges:
        print(f"Flipping neighbor: {neighbor_id}")
        neighbor = flip_tile(neighbor, edge, tile_db)

    if edge not in neighbor.edges:
        print(f"Edge not found even after flipping tile {neighbor_id}: {''.join(edge)}")
        print("\n".join(map(lambda x: ''.join(x), neighbor.edges)))
        print("^^^^^^^")

    neighbor = rotate_tile(neighbor, tile_db, all_edges, [(lookup[edge_index], edge)])
    prev.merge(neighbor, edge)

    # tile_db[neighbor].merge(prev, edge)
    return neighbor


def assemble_grid(tile_db):
    grid_width = int(len(tile_db) ** 0.5)
    if grid_width == 1:
        return [[tile_db[list(tile_db.keys())[0]].tile_id]]

    corners, sides, middles = divide_tiles(tile_db, all_edge_db(tile_db))
    print(f"Corner tiles: {corners}")
    all_edges = all_edge_db(tile_db)
    original_edges = original_edge_db(tile_db)

    edge_tiles = set(corners + sides)
    placed_tiles = set()

    grid = []
    for i in range(grid_width):
        grid.append([])
        for j in range(grid_width):
            grid[-1].append(None)

    top_left_tile = tile_db[corners[0]]
    lone_corner_indices = tuple([i for i in range(4) if len(all_edges.db[top_left_tile.edges[i]]) == 1])
    target_indices = (0, 2)
    if lone_corner_indices in [(0, 3), (3, 1), (1, 2)]:
        target_indices = (2, 0)

    corner_lone_edges = [e for e in top_left_tile.edges if len(all_edges.db[e]) == 1]
    print(f"Corner lone edges: {[''.join(x) for x in corner_lone_edges]}")
    print(f"Target indices: {target_indices}")
    print(f"Arg: {list(zip(target_indices, [''.join(x) for x in corner_lone_edges]))}")
    tile_db[corners[0]] = rotate_tile(top_left_tile, tile_db, all_edges, list(zip(target_indices, corner_lone_edges)))

    lone_corner_indices = tuple([i for i in range(4) if len(all_edges.db[tile_db[corners[0]].edges[i]]) == 1])
    print(f"After rotating {corners[0]}: {lone_corner_indices}")

    grid[0][0] = corners[0]
    placed_tiles.add(grid[0][0])

    print("BORDER_GRID:")
    print("\n".join(list(map(lambda x: " ".join(list(map(str, x))), grid))))

    # top row & left col
    for i in range(1, grid_width):
        is_last = (i == grid_width - 1)
        print(f"Placing tile ({0}, {i})")
        grid[0][i] = merge_edge_tiles(tile_db[grid[0][i - 1]], tile_db, all_edges, 1).tile_id
        if grid[0][i] in placed_tiles:
            print(f"ALREADY placed tile??: {grid[0][i]}")
        placed_tiles.add(grid[0][i])

        print("BORDER_GRID:")
        print("\n".join(list(map(lambda x: " ".join(list(map(str, x))), grid))))

        print(f"Placing tile ({i}, {0})")
        grid[i][0] = merge_edge_tiles(tile_db[grid[i - 1][0]], tile_db, all_edges, 3).tile_id
        if grid[i][0] in placed_tiles:
            print(f"ALREADY placed tile??: {grid[i][0]}")
        placed_tiles.add(grid[i][0])

        print("BORDER_GRID:")
        print("\n".join(list(map(lambda x: " ".join(list(map(str, x))), grid))))

    # bottom row & right col
    print("PLACING BOTTOM ROW AND RIGHT COL")
    for i in range(1, grid_width):
        is_last = (i == grid_width - 1)
        print(f"Placing tile ({grid_width - 1}, {i})")
        grid[grid_width - 1][i] = merge_edge_tiles(tile_db[grid[grid_width - 1][i - 1]], tile_db, all_edges, 1).tile_id
        if grid[grid_width - 1][i] in placed_tiles:
            print(f"ALREADY placed tile??: {grid[grid_width - 1][i]}")
        placed_tiles.add(grid[grid_width - 1][i])

        print("BORDER_GRID:")
        print("\n".join(list(map(lambda x: " ".join(list(map(str, x))), grid))))

        if not is_last:
            print(f"Placing tile ({i}, {grid_width - 1})")
            grid[i][grid_width - 1] = merge_edge_tiles(tile_db[grid[i - 1][grid_width - 1]], tile_db, all_edges,
                                                       3).tile_id
            if grid[i][grid_width - 1] in placed_tiles:
                print(f"ALREADY placed tile??: {grid[i][grid_width - 1]}")
            placed_tiles.add(grid[i][grid_width - 1])

            print("BORDER_GRID:")
            print("\n".join(list(map(lambda x: " ".join(list(map(str, x))), grid))))

    if edge_tiles != placed_tiles:
        print(f"EDGE WRONG: edge_tiles: {edge_tiles}")
        print(f"PLAC WRONG: placed_tiles: {placed_tiles}")
        raise Exception(":(")

    if not middles:
        print("NO MIDDLES")
        return grid

    middle_tile_db = {middle_tile: tile_db[middle_tile] for middle_tile in middles}
    inner_grid = assemble_grid(middle_tile_db)

    print("INNER_GRID:")
    print("\n".join(list(map(lambda x: " ".join(list(map(str, x))), inner_grid))))

    for i in range(1, grid_width - 1):
        for j in range(1, grid_width - 1):
            grid[i][j] = inner_grid[i - 1][j - 1]

    print("OUTER_GRID:")
    print("\n".join(list(map(lambda x: " ".join(list(map(str, x))), grid))))

    return grid


def solution1(tiles):
    grid_width = int(len(tiles) ** 0.5)
    min_joined_edges = (len(tiles) * 4 - grid_width * 4)
    print(f"Num tiles: {len(tiles)}, grid_width: {grid_width}, min_joined_edges: {min_joined_edges}")
    corner_tiles, edge_tiles, middle_tiles = divide_tiles(tiles, all_edge_db(tiles))
    return reduce(operator.mul, corner_tiles)


# solution1(parse("sample.txt"))
# print("RESULT: ",solution1(parse("sample.txt")))
# print("RESULT: ",solution1(parse("input.txt")))

print("RESULT:")
assemble_grid(parse("input.txt"))
# print("\n".join(list(map(lambda x: " ".join(list(map(lambda y: str(y.tile_id), x))), assemble_grid(parse("sample.txt"))))))

import enum
from typing import Tuple
from functools import cached_property

TILE_SIZE = 10


def _get_tile_edges(body: Tuple):
    return (tuple(body[0]),  # up
            tuple([x[-1] for x in body]),  # right
            tuple(reversed(body[-1])),  # down
            tuple(reversed([x[0] for x in body])))  # left


class Edge(enum.IntEnum):
    U = 0
    R = 1
    D = 2
    L = 3


class Tile(object):
    def __init__(self, number, body):
        self.number = number
        self.body = body
        self.edges = _get_tile_edges(body)
        self.neighbors = [None] * 4

    def merge(self, number, merging_edge):
        for i in range(4):
            if self.edges[i] == merging_edge:
                self.neighbors[i] = number
                return
        raise Exception("Can't merge")

    def is_connected(self, number):
        return number in self.neighbors

    def get_edge(self, side: Edge):
        return self.edges[side.value]

    def flip(self):
        if not all([neighbor is None for neighbor in self.neighbors]):
            raise Exception("Cannot flip a tile with neighbors")

        new_body = []
        for i in range(TILE_SIZE):
            new_row = []
            for j in range(TILE_SIZE):
                new_row.append(self.body[TILE_SIZE-1-i][j])
            new_body.append(tuple(new_row))
        new_body = tuple(new_body)
        self.edges = _get_tile_edges(new_body)
        self.body = new_body

    def rotate(self, times=1):
        if not all([neighbor is None for neighbor in self.neighbors]):
            raise Exception("Cannot rotate a tile with neighbors")

        body = [list(x) for x in self.body]
        new_body = list(self.body)
        for t in range(times):
            new_body = []
            for i in range(TILE_SIZE):
                row = []
                for j in range(TILE_SIZE):
                    row.append(body[TILE_SIZE - 1 - j][i])
                new_body.append(tuple(row))
            body = new_body
        self.body = tuple(new_body)
        self.edges = _get_tile_edges(self.body)

    def shed(self):
        new_body = []
        for i in range(1, TILE_SIZE-1):
            new_body.append(tuple(self.body[i][1:-1]))
        self.body = tuple(new_body)

    @cached_property
    def all_possible_edges(self):
        return self.edges + tuple(map(lambda x: tuple(reversed(x)), self.edges))

    def lone_edges(self, tile_db) -> Tuple:
        return tuple([Edge(i) for i in range(4) if len(tile_db.all_edges[self.edges[i]]) == 1])

    def lone_edge_count(self, tile_db):
        return sum([1 for edge in self.edges if len(tile_db.all_edges[edge]) == 1])

    def pretty_edges(self):
        out = [f"Tile {self.number} edges:"]
        for i in range(4):
            out.append(f"{Edge(i).name}: {''.join(self.edges[i])}")
        return "\n".join(out)

    def pretty(self):
        out = [f"Tile {self.number}:"]
        for row in self.body:
            out.append("".join(row))
        return "\n".join(out)



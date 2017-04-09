from Utilities import *
import numpy as np


class Cell:
    Backbone, Void, Wall, Wireless, Router, ConnectedRouter, Cable = range(-2, 5)


def read_dataset(fpath):
    with open(fpath, 'r') as reader:
        # size of grid
        H, W, R = [int(i) for i in reader.readline().split(" ")]
        # cost and budget
        Pb, Pr, B = [int(i) for i in reader.readline().split(" ")]
        # backbone position
        tmp = reader.readline().split(" ")
        backbone = (int(tmp[0]), int(tmp[1]))
        # read the matrix
        matrix = np.zeros((H, W), dtype=np.int8)

        for line in range(H):
            tmp = reader.readline()
            for col in range(W):
                if tmp[col] == '-':
                    matrix[line, col] = Cell.Void
                elif tmp[col] == '#':
                    matrix[line, col] = Cell.Wall
                else:
                    matrix[line, col] = Cell.Wireless

        return {
            'height': H,
            'width': W,
            'radius': R,
            'price_backbone': Pb,
            'price_router': Pr,
            'budget': B,
            'backbone': backbone,
            'graph': matrix
        }


def write_solution(fpath, D):
    # look for cables and routers, find positions and write that stuff
    cables = []
    routers = []

    graph = D['graph']
    for x, row in enumerate(graph):
        for y, val in enumerate(row):
            if val == Cell.Cable:
                cables.append((x, y))
            elif val == Cell.ConnectedRouter:
                routers.append((x, y))
                cables.append((x, y))

    with open(fpath, 'w') as writer:
        writer.write("%d\n" % len(cables))
        for cable in cables:
            writer.write("%d %d\n" % (cable[0], cable[1]))

        writer.write("%d\n" % len(routers))
        for router in routers:
            writer.write("%d %d\n" % (router[0], router[1]))

        writer.close()


if __name__ == '__main__':
    import sys

    fpath = sys.argv[1]
    D = read_dataset(fpath)
    bb = D['backbone']
    D['graph'][bb[0] - 1, bb[1]] = Cell.Cable
    write_solution(sys.argv[2], D)

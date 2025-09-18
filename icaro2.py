import math
import random
from functools import lru_cache

N = 16
M = 12
lmb = 0.2

def zero(n,m):
    return [
        [
            [0, 0]
            for j in range(M+1)
        ]
        for i in range(N+1)
    ]


def init(n,m):
    z=zero(n,m)
    # init
    for i in range(n):
        z[i][0][0] = 1
        z[i][m][0] = 1
    for j in range(m):
        z[0][j][1] = 1
        z[n][j][1] = 1
    return z


def draw(l):
    n=len(l) - 1
    m=len(l[0]) - 1
    for j in range(m,-1,-1):
        for i in range(n + 1):
            if l[i][j][1]:
                print("|", end="")
            else:
                print(" ", end="")
            if l[i][j][0]:
                print("_", end="")
            else:
                print(" ", end="")
        print("\n", end="")


def candidate_pos(n,m):
    for j in range(m):
        for i in range(1, n):
            yield (i,j,1)
    for i in range(n):
        for j in range(1, m):
            yield (i,j,0)


def saturate(l):
    n=len(l) - 1
    m=len(l[0]) - 1
    for i,j,z in candidate_pos(n,m):
        assert l[i][j][z]==0
        l[i][j][z] = 1


def has_walls(i, j, l):
    # is the corner at i, j touched by some walls? 
    full = l[i][j][0] + l[i][j][1] + l[i-1][j][0] + l[i][j-1][1]
    return full > 0


def eligible_wall_pos(pos, l):
    i,j,z=pos
    # must be empty
    if l[i][j][z] == 1:
        return False
    # one end must bear wall, the other no
    end0 = (i, j)
    end1 = (i + (1 - z), j + z)
    has_walls0 = has_walls(*end0, l)
    has_walls1 = has_walls(*end1, l)
    return has_walls0 ^ has_walls1


@lru_cache
def wall_weight(i, j, hn, hm, lmb):
    return math.exp(-lmb*(math.fabs(i-hn) + math.fabs(j-hm)))

def choose_wall(cand_walls, l):
    # uniform
    # return cand_walls[random.randint(0, len(cand_walls)-1)]

    # prefer central
    hn=0.5 * (len(l) - 1)
    hm=0.5 * (len(l[0]) - 1)
    weights = [
        wall_weight(i, j, hn, hm, lmb)
        for i, j, _ in cand_walls
    ]
    cumw = [
        sum(weights[0:p+1])
        for p in range(len(weights))
    ]
    rnd = random.random() * cumw[-1]
    return [
        cwall
        for cwall, cumw in zip(cand_walls, cumw)
        if cumw > rnd
    ][0]


def add_one(l):
    n=len(l) - 1
    m=len(l[0]) - 1
    cand_wallpos = [
        cand_pos
        for cand_pos in candidate_pos(n,m)
        if eligible_wall_pos(cand_pos, l)
    ]
    if cand_wallpos == []:
        return False

    wall_pos = choose_wall(cand_wallpos, l)
    i,j,z=wall_pos
    l[i][j][z]=1
    return True

if __name__ == "__main__":
    labi = init(N,M)
    # draw(labi)
    saturate(labi)
    # draw(labi)

    labi = init(N,M)
    for w in range((N-1) * (M-1) + 1):
        # print("ITE", w)
        # draw(labi)
        if not add_one(labi):
            # print("Exiting")
            break

    draw(labi)
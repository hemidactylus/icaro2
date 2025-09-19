import math
import random
from functools import lru_cache

N = 24
M = 18
lmb = 0.2
lmb2 = 0.6
lmb3 = 2.5

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


def survey_walls(i, j, l):
    # count walls entering either ends of this proposed wall
    vs = l[i][j][1] + l[i][j-1][1]
    hs = l[i][j][0] + l[i-1][j][0]
    return (hs, vs)


def eligible_wall_pos(pos, l):
    # return bool, (edge counts h/v)
    i,j,z=pos
    # must be empty
    if l[i][j][z] == 1:
        return False, (0,0)
    # one end must bear wall, the other no
    end0 = (i, j)
    end1 = (i + (1 - z), j + z)
    ws0 = survey_walls(*end0, l)
    ws1 = survey_walls(*end1, l)
    return (ws0[0]+ws0[1] > 0) ^ (ws1[0]+ws1[1] > 0), (ws0[0]+ws1[0], ws0[1]+ws1[1])


@lru_cache
def wall_weight(i, j, n, m, lmb, z, wshs):
    # prefer central (lmb)
    # prefer corners over straight long segments (lmb2)
    # prefer walls not starting off boundaries (lmb3)
    isborder = 1 if i==0 or j==0 or i==n-1 or j==m-1 else 0
    hn= 0.5 * n
    hm= 0.5 * m
    return math.exp(-lmb*(math.fabs(i-hn) + math.fabs(j-hm)) -lmb2*(wshs[z]-wshs[1-z]) - lmb3*isborder)

def choose_wall(cand_walls, l):
    n=len(l) - 1
    m=len(l[0]) - 1

    weights = [
        wall_weight(i, j, n, m, lmb, z, wshs)
        for (i, j, z), (elib, wshs) in cand_walls
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
        (cand_pos, eli)
        for cand_pos in candidate_pos(n,m)
        if (eli := eligible_wall_pos(cand_pos, l))[0]
    ]
    if cand_wallpos == []:
        return False

    wall_pos = choose_wall(cand_wallpos, l)
    i,j,z=wall_pos[0]
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

from dataclasses import dataclass

CellType = tuple[int, int]
LineState = int
LinePos = tuple[int, int, int]

IMP_WHITE = 0
IMP_WALL = 1
CAND_WALL = 10


@dataclass
class CandidateState:
    growable: bool
    weight: float
    meta: dict[str, int]


def calc_impositions(
    n: int, m: int, dcells: set[CellType], dimps: dict[LinePos, int]
) -> dict[LinePos, LineState]:
    imposed: dict[LinePos, LineState] = {}
    for x in range(n + 1):
        for y in range(m + 1):
            is_dead = (x, y) in dcells
            if y < m:
                # vert line before cell
                vl = (x, y, 1)
                if x == 0:
                    imposed[vl] = IMP_WHITE if is_dead else IMP_WALL
                elif x == n:
                    imposed[vl] = IMP_WHITE if (x - 1, y) in dcells else IMP_WALL
                else:
                    # on the inside, impose if on interface only
                    if is_dead ^ ((x - 1, y) in dcells):
                        imposed[vl] = IMP_WALL
                    elif is_dead:
                        # within the dead zone entirely
                        imposed[vl] = IMP_WHITE
            if x < n:
                # horiz line below cell
                hl = (x, y, 0)
                if y == 0:
                    imposed[hl] = IMP_WHITE if is_dead else IMP_WALL
                elif y == m:
                    imposed[hl] = IMP_WHITE if (x, y - 1) in dcells else IMP_WALL
                else:
                    # on the inside, check for interface
                    if is_dead ^ ((x, y - 1) in dcells):
                        imposed[hl] = IMP_WALL
                    elif is_dead:
                        # within the dead zone entirely
                        imposed[hl] = IMP_WHITE
    # direct impositions if any
    for line, imposed_state in dimps.items():
        imposed[line] = IMP_WALL if imposed_state else IMP_WHITE
    return imposed


def calc_candidates_TEMP(
    n: int, m: int, impositions: dict[LinePos, LineState]
) -> dict[LinePos, LineState]:
    cands: set[LinePos] = set()
    for x in range(n + 1):
        for y in range(m + 1):
            if y < m:
                # vert line before cell
                if (x, y, 1) not in impositions:
                    cands.add((x, y, 1))
            if x < n:
                # horiz line below cell
                if (x, y, 0) not in impositions:
                    cands.add((x, y, 0))
    # TEMP build a 'candidate-only' maze for tests
    return {lp: CAND_WALL for lp in cands}


def recolor(msg: str) -> str:
    return f"\033[96m{msg}\033[0m"


def maze_display(N, M, maze, default=" ") -> str:
    buffer = ""
    for j in range(M, -1, -1):
        for i in range(N + 1):
            vl = (i, j, 1)
            hl = (i, j, 0)
            vstate = maze.get(vl)
            if vstate == IMP_WHITE:
                buffer += "'"
            elif vstate == IMP_WALL:
                buffer += "|"
            elif vstate == CAND_WALL:
                buffer += recolor("|")
            elif vstate is None:
                buffer += default
            else:
                raise ValueError
            hstate = maze.get(hl)
            if hstate == IMP_WHITE:
                buffer += "."
            elif hstate == IMP_WALL:
                buffer += "_"
            elif hstate == CAND_WALL:
                buffer += recolor("_")
            elif hstate is None:
                buffer += default
            else:
                raise ValueError
        if j > 0:
            buffer += "\n"
    return buffer


if __name__ == "__main__":
    # test setup
    N = 4
    M = 5
    dead_cells: set[CellType] = {(0, 2), (0, 3), (1, 3), (0, 4), (3, 0), (3, 1)}
    direct_impositions: dict[LinePos, int] = {(1, 0, 1): 1, (1, 1, 0): 1, (3, 3, 0): 0}
    impositions = calc_impositions(N, M, dead_cells, direct_impositions)
    #
    temp_cand_maze = calc_candidates_TEMP(N, M, impositions)
    #
    #
    assert temp_cand_maze.keys() & impositions.keys() == set()
    tcm_repr = maze_display(N, M, {**temp_cand_maze, **impositions})
    print("with candidates:")
    print(tcm_repr)

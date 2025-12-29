# Icaro 2 - reboot

Maze is contained within a `(N,M)` grid ("size").

"Line" is a `(x,y,t)` triple (a `LinePos`) with t = 0 for horizontal, 1 for vertical (growbound from corner).
A line can be made either 'wall' or 'white'.

A fictitious layer on the top and right, used only for horiz-lines and vert-lines resp., is added.

## Imposition

Dead cells are `(x,y)`, a set.

Dead cells induce imposed:

- walls, between dead and alive
- walls, between alive and boundary
- whites, between dead and dead
- whites, between dead and boundary

There may be (white/wall) impositions as direct requests on top of it. These act as overrides.

impositions is a map `LinePos -> line state (int)`

## Candidates

All lines that could be walls (i.e. not imposed) are 'candidates'.

A map `(x,y,t) -> CandidateState`

CandidateState has attributes:
- growable (bool)
- weight (float) <-- depends on strategy

## Maze

The maze is a fixed-size NxMx2 (modulo offsets) array, where
- <= 0 means white (-1 if imposed, 0 if from candidate)
- nonzero means wall (1 = imposed, 2 = from candidate)

## Flow

### Init

deadcells, size, forced-impositions --> imposed

fullgrid, imposed --> candidates

fullgrid, imposed , candidates --> maze

For all candidate lines: calculate is_growable; refresh list of growables

### Update

While list of growables is ! []:

- pick one line (use weights from strategy)
- turn on wall: (a) on maze, (b) mark ungrowable, (c) recalc growable of up to 6 neighbours

### Growable

A line is growable if (it is candidate, AND) it is not a wall AND exactly one of the two ends is touching at least one wall. (must retain all info on the walls for the weight strategy: number, orientation)

## Testing setup

N, M = 4, 5

Dead cells:

```
Xooo
XXoo
Xooo
oooX
oooX
```

That is:

```
{(0,2), (0,3), (1,3), (0,4), (3,0), (3,1)}
```

Additional direct-imposed walls(1)/whites(0):

```
{(1,0,1): 1, (1,1,0): 1, (3,3,0): 0}
```

expected impositions (walls; wites are `.` and `'`):

```
 . _ _ _  
'.|_    | 
'.'_|  .| 
'_|    _| 
|  _  |.' 
|_|_ _|.' 
```

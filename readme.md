# Icaro 2

cells are [x,y] and each has |_  _=0, |=1

origin is lower left, so (note a fictitious layer):

```
[*0,M]                          [*N,M]
[0,M-1]               [N-1,M-1]
...
[0.2]
[0,1]
[0,0] [1,0] [2,0] ... [N-1,0]   [*N,0]
```

Init for NxM is:

- has `|` iff (x==0 or x==N) and y < M
- has `_` iff (y==0 or y==M) and x < N

Total walls to build are:


e.g. N=3,M=2. Init:

```
 _ _ _ ,
|. . .|,
|_ _ _|,
```

might become (i.e. +2:

```
 _ _ _ ,
|. .|.|,
|_|_ _|,
```

it seems (N-1) * (M-1) must be attached.

candidate wall positions are:

- `|` for all (x = 1...N-1 and y = 0...M-1)
- `_` for all (y = 1...M-1 and x = 0...N-1)

 
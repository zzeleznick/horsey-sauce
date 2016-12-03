## Hard Inputs

Divergent Results (lo, hi)
307: 2364323, 12348875 (65)
416: 5873665, 11751500 (1)
556: 6385483, 12249408 (49)
396: 2010492, 7155918 (10)
130: USE DFS 7132304 < 9159450

DFS > Sets
003, 130, 396


Long Runtimes
- 70.in (* 112K edge, slowasf) [SOLVED]
    vertices go 1..50, edges are i+50...
    path 0 50 100 150 200 250 300 350 400 450; ... 49, 99 .. 499
    50 paths each length 10, average of 25 per v
    10**2*25*50: 125000
- 229.in
- 230.in [9 minutes]
- 231.in [9 minutes]
- 271.in [15 minutes]
- 272.in [7 minutes]
- 273.in [13 minutes]
- 336.in
- 356.in
- 406.in
- 407.in
- 408.in
- 462.in
- 581.in (* 84K edge)
- 582.in (* 73K edge)
- 590.in (* 245K edges)

Ours
- 448.in
    5,420,063 (14)
- 449.in
    Note that our best is right now 3,495,378 (10) | 4,837,785 (224)
    But, weston got 10,035,223
- 450.in
    3,876,251 (14) | 5,572,087 (269)

## Todos
- compare dfs with sets for select inputs
- ensure we take the best output (dfs/sets)
- check for dags => dag longest path
- check alternate algs ?

## Timing
33 minutes for 1-500.in

## Notes

Path Length ~= (Score/50)**.5

Note:
500**2*50 = 12,500,000
480**2*50 = 11,520,000

If ranking is based on sum(scores)
the biggest differentiators will be on graphs
with scores with large multiplicative differences

e.g. graph with optimal path length of 420 vs 380, 380 vs 310
420**2*50: 8,820,000
380**2*50: 7,220,000
340**2*50: 5,780,000
260**2*50: 3,380,000
180**2*50: 1,620,000
120**2*50: 720,000

a path length increase of x =>
    p = (s/50)**.5;
    s2 = (p+x)**2*50;
    maximize (s2-s)

def pdelta(p,x):
    s = (p)**2*50
    s2 = (p+x)**2*50
    return s2-s

In [100]: pdelta(460, 40)
Out[100]: 1920000

In [98]: pdelta(420, 40)
Out[98]: 1760000

In [66]: pdelta(380, 40)
Out[66]: 1600000

In [67]: pdelta(300, 40)
Out[67]: 1280000

In [68]: pdelta(100, 40)
Out[68]: 480000

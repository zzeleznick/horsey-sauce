## Hard Inputs

Long Runtimes
- 70.in
- 229.in
- 230.in
- 231.in
- 271.in
- 272.in
- 273.in
- 336.in
- 356.in
- 406.in
- 407.in
- 408.in
- 461.in

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

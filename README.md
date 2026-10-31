# Traveling Salesman — Farthest Insertion Heuristic

[![CI](https://github.com/BernardoFerrazG/Heur-stica-Caixeiro-Viajante/actions/workflows/ci.yml/badge.svg)](https://github.com/BernardoFerrazG/Heur-stica-Caixeiro-Viajante/actions/workflows/ci.yml)

A constructive heuristic for the **Traveling Salesman Problem** (*Problema do Caixeiro Viajante*): **farthest insertion**. An optional **2-opt** local search can then improve the tour. Code and CLI messages are in Portuguese; this README is in English.

## How it works

**Farthest insertion** (`insercao_mais_distante`):

1. Start with a cycle made of the two cities that are farthest apart.
2. Choose the city outside the cycle whose distance to its *nearest* city in the cycle is the largest.
3. Insert it between the pair of consecutive cities `(a, b)` that minimises the cost increase `d(a,x) + d(x,b) − d(a,b)`.
4. Repeat until every city is in the cycle.

Inserting the far-away cities first fixes the "outline" of the tour early. This usually gives better results than nearest-neighbour or nearest-insertion construction. The implementation keeps every city's distance to the current cycle up to date incrementally, so each insertion costs `O(n)` and the whole construction `O(n²)`.

**2-opt** (`dois_opt`, enabled with `--2opt`): repeatedly takes two edges `(a,b)` and `(c,d)`, replaces them with `(a,c)` and `(b,d)` by reversing the segment between them, and stops when no such exchange shortens the tour.

## Results on the bundled instance

The instance in [`distancias.txt`](distancias.txt) has 15 cities; its exact optimum is **291**, computed with a Held-Karp dynamic program.

| Method | Tour length | Gap to optimum |
| --- | --- | --- |
| Farthest insertion | 315 | +8.2% |
| Farthest insertion + 2-opt | 315 | +8.2% (already 2-opt optimal) |

For comparison, the [Ant Colony Optimization solver](https://github.com/BernardoFerrazG/TSP_ant_colony) reaches the optimum of 291 on the same instance, at a much higher computational cost.

## Usage

```bash
pip install -r requirements.txt
python pcv.py                     # farthest insertion, opens the plot
python pcv.py --2opt              # + 2-opt improvement
python pcv.py --sem-grafico       # text output only
python pcv.py -m outra_matriz.txt
```

Example output:

```
Inserção do mais distante: custo 315
Ciclo: 0 -> 10 -> 3 -> 5 -> 13 -> 11 -> 7 -> 9 -> 2 -> 6 -> 4 -> 8 -> 14 -> 1 -> 12 -> 0
```

## Tests

```bash
pip install pytest
pytest
```

The tests check that tours are valid, that 2-opt never makes a tour worse, and that on 15 random 8-city Euclidean instances the heuristic stays within 25% of the brute-force optimum. CI runs them on every push.

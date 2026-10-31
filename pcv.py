"""Heurísticas construtiva e de melhoria para o Problema do Caixeiro Viajante (PCV).

* Inserção do mais distante: começa pelo par de cidades mais distantes e, a cada
  passo, insere a cidade mais longe do ciclo atual na posição de menor custo.
* 2-opt (opcional): remove pares de arestas que se cruzam, invertendo o trecho
  entre elas, até não haver mais melhoria.
"""

from __future__ import annotations

import argparse
from pathlib import Path

Matriz = list[list[float]]

ARQUIVO_PADRAO = Path(__file__).resolve().parent / "distancias.txt"


def le_matriz(caminho: str | Path) -> Matriz:
    """Lê uma matriz de distâncias quadrada (valores separados por espaço, ``#`` = comentário)."""
    matriz = []
    with open(caminho, encoding="utf-8") as arquivo:
        for linha in arquivo:
            linha = linha.split("#", 1)[0].strip()
            if linha:
                matriz.append([float(valor) for valor in linha.split()])
    if any(len(linha) != len(matriz) for linha in matriz):
        raise ValueError("a matriz de distâncias precisa ser quadrada")
    return matriz


def custo_ciclo(caminho: list[int], matriz: Matriz) -> float:
    """Custo do ciclo que percorre ``caminho`` e volta à cidade inicial."""
    return sum(matriz[caminho[i]][caminho[(i + 1) % len(caminho)]] for i in range(len(caminho)))


def insercao_mais_distante(matriz: Matriz) -> list[int]:
    """Constrói um ciclo pela heurística de inserção do mais distante, em O(n²)."""
    n = len(matriz)
    if n < 3:
        return list(range(n))

    i, j = max(((i, j) for i in range(n) for j in range(i + 1, n)), key=lambda par: matriz[par[0]][par[1]])
    caminho = [i, j]
    nao_visitados = set(range(n)) - set(caminho)
    # Distância de cada cidade fora do ciclo até a cidade mais próxima dentro dele.
    dist_ao_ciclo = {v: min(matriz[v][i], matriz[v][j]) for v in nao_visitados}

    while nao_visitados:
        vertice = max(nao_visitados, key=lambda v: (dist_ao_ciclo[v], -v))

        def custo_insercao(pos: int) -> float:
            a, b = caminho[pos], caminho[(pos + 1) % len(caminho)]
            return matriz[a][vertice] + matriz[vertice][b] - matriz[a][b]

        melhor_pos = min(range(len(caminho)), key=custo_insercao)
        caminho.insert(melhor_pos + 1, vertice)
        nao_visitados.remove(vertice)
        for v in nao_visitados:
            dist_ao_ciclo[v] = min(dist_ao_ciclo[v], matriz[v][vertice])

    return caminho


def dois_opt(caminho: list[int], matriz: Matriz) -> list[int]:
    """Melhora o ciclo com movimentos 2-opt até atingir um ótimo local (matriz simétrica)."""
    caminho = caminho[:]
    n = len(caminho)
    melhorou = True
    while melhorou:
        melhorou = False
        for i in range(n - 1):
            for j in range(i + 2, n if i > 0 else n - 1):
                a, b = caminho[i], caminho[i + 1]
                c, d = caminho[j], caminho[(j + 1) % n]
                ganho = matriz[a][b] + matriz[c][d] - matriz[a][c] - matriz[b][d]
                if ganho > 1e-9:
                    caminho[i + 1 : j + 1] = reversed(caminho[i + 1 : j + 1])
                    melhorou = True
    return caminho


def comeca_em(caminho: list[int], cidade: int = 0) -> list[int]:
    k = caminho.index(cidade)
    return caminho[k:] + caminho[:k]


def desenha(caminho: list[int], matriz: Matriz, custo: float) -> None:
    import matplotlib.pyplot as plt
    import networkx as nx

    grafo = nx.DiGraph()
    grafo.add_nodes_from(range(len(matriz)))
    for k in range(len(caminho)):
        a, b = caminho[k], caminho[(k + 1) % len(caminho)]
        grafo.add_edge(a, b, weight=f"{matriz[a][b]:g}")

    pos = nx.circular_layout(caminho)
    nx.draw(grafo, pos, with_labels=True, node_color="lightblue", node_size=600, font_size=10, edge_color="tab:red")
    nx.draw_networkx_edge_labels(grafo, pos, edge_labels=nx.get_edge_attributes(grafo, "weight"), font_size=9)
    plt.title(f"Ciclo encontrado — custo {custo:g}")
    plt.show()


def main() -> None:
    parser = argparse.ArgumentParser(description="PCV: inserção do mais distante (+ 2-opt opcional).")
    parser.add_argument("-m", "--matriz", default=ARQUIVO_PADRAO, help="arquivo com a matriz de distâncias")
    parser.add_argument("--2opt", dest="dois_opt", action="store_true", help="aplica a melhoria 2-opt ao ciclo")
    parser.add_argument("--sem-grafico", action="store_true", help="não abre a janela com o desenho")
    args = parser.parse_args()

    matriz = le_matriz(args.matriz)
    caminho = insercao_mais_distante(matriz)
    print(f"Inserção do mais distante: custo {custo_ciclo(caminho, matriz):g}")

    if args.dois_opt:
        caminho = dois_opt(caminho, matriz)
        print(f"Após 2-opt:                custo {custo_ciclo(caminho, matriz):g}")

    caminho = comeca_em(caminho)
    custo = custo_ciclo(caminho, matriz)
    print("Ciclo:", " -> ".join(map(str, caminho + [caminho[0]])))

    if not args.sem_grafico:
        desenha(caminho, matriz, custo)


if __name__ == "__main__":
    main()

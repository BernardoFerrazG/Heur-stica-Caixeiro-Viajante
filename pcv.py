import networkx as nx
import matplotlib.pyplot as plt


def insercao_mais_distante(matriz):
    n = len(matriz)
    maior_distancia = -1
    par = (0, 1)
    for i in range(n):
        for j in range(n):
            if matriz[i][j] > maior_distancia:
                maior_distancia = matriz[i][j]
                par = (i, j)

    caminho = list(par)  
    nao_visitados = set(range(n)) - set(caminho)
    
    while nao_visitados:

        vertice_distante = max(
            nao_visitados, 
            key=lambda i: min(matriz[i][j] for j in caminho)
        )
        
        custos_insercao = []
        for i in range(len(caminho)):
            prox = (i + 1) % len(caminho)
            custo = (
                matriz[caminho[i]][vertice_distante] +
                matriz[vertice_distante][caminho[prox]] -
                matriz[caminho[i]][caminho[prox]]
            )
            custos_insercao.append(custo)
        
        melhor_pos = custos_insercao.index(min(custos_insercao))
        
        caminho.insert(melhor_pos + 1, vertice_distante)
        nao_visitados.remove(vertice_distante)

    return caminho


matriz = [
    [0, 29, 82, 46, 68, 52, 72, 42, 51, 55, 29, 74, 23, 72, 46],
    [29, 0, 55, 46, 42, 43, 43, 23, 23, 31, 41, 51, 11, 52, 21],
    [82, 55, 0, 68, 46, 55, 23, 43, 41, 29, 79, 21, 64, 31, 51],
    [46, 46, 68, 0, 82, 15, 72, 31, 62, 42, 21, 51, 51, 43, 64],
    [68, 42, 46, 82, 0, 74, 23, 52, 21, 46, 82, 58, 46, 65, 23],
    [52, 43, 55, 15, 74, 0, 61, 23, 55, 31, 33, 37, 51, 29, 59],
    [72, 43, 23, 72, 23, 61, 0, 42, 23, 31, 77, 37, 51, 46, 33],
    [42, 23, 43, 31, 52, 23, 42, 0, 33, 15, 37, 33, 33, 31, 37],
    [51, 23, 41, 62, 21, 55, 23, 33, 0, 29, 62, 46, 29, 51, 11],
    [55, 31, 29, 42, 46, 31, 31, 15, 29, 0, 51, 21, 41, 23, 37],
    [29, 41, 79, 21, 82, 33, 77, 37, 62, 51, 0, 65, 42, 59, 61],
    [74, 51, 21, 51, 58, 37, 37, 33, 46, 21, 65, 0, 61, 11, 55],
    [23, 11, 64, 51, 46, 51, 51, 33, 29, 41, 42, 61, 0, 62, 23],
    [72, 52, 31, 43, 65, 29, 46, 31, 51, 23, 59, 11, 62, 0, 59],
    [46, 21, 51, 64, 23, 59, 33, 37, 11, 37, 61, 55, 23, 59, 0]
]


caminho = insercao_mais_distante(matriz)

custo_total = sum(
    matriz[caminho[i]][caminho[(i+1) % len(caminho)]] 
    for i in range(len(caminho))
)   

G = nx.DiGraph()
G.add_nodes_from(range(len(matriz)))

for i in range(len(caminho)):
    G.add_edge(caminho[i], caminho[(i+1) % len(caminho)], weight=matriz[caminho[i]][caminho[(i+1) % len(caminho)]])

pos = nx.spring_layout(G, seed=42)
nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=500, font_size=10)
edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10)

print("caminho:", caminho)
print("Custo Total:", custo_total)

plt.show()




import itertools
import random

import pytest

from pcv import ARQUIVO_PADRAO, comeca_em, custo_ciclo, dois_opt, insercao_mais_distante, le_matriz

OTIMO_15_CIDADES = 291  # ótimo exato de distancias.txt (Held-Karp)


def forca_bruta(matriz):
    n = len(matriz)
    return min(custo_ciclo([0, *perm], matriz) for perm in itertools.permutations(range(1, n)))


def matriz_euclidiana(n, seed):
    rng = random.Random(seed)
    pontos = [(rng.random(), rng.random()) for _ in range(n)]
    return [[((xa - xb) ** 2 + (ya - yb) ** 2) ** 0.5 for xb, yb in pontos] for xa, ya in pontos]


def test_ciclo_visita_todas_as_cidades():
    matriz = le_matriz(ARQUIVO_PADRAO)
    caminho = insercao_mais_distante(matriz)
    assert sorted(caminho) == list(range(len(matriz)))


def test_resultado_na_instancia_de_exemplo():
    matriz = le_matriz(ARQUIVO_PADRAO)
    construtivo = insercao_mais_distante(matriz)
    melhorado = dois_opt(construtivo, matriz)
    assert custo_ciclo(construtivo, matriz) >= OTIMO_15_CIDADES
    assert custo_ciclo(melhorado, matriz) <= custo_ciclo(construtivo, matriz)
    assert sorted(melhorado) == list(range(len(matriz)))


@pytest.mark.parametrize("seed", range(15))
def test_qualidade_em_instancias_euclidianas(seed):
    matriz = matriz_euclidiana(8, seed)
    otimo = forca_bruta(matriz)
    construtivo = insercao_mais_distante(matriz)
    melhorado = dois_opt(construtivo, matriz)
    # Inserção do mais distante tem garantia de razão logarítmica; na prática fica bem perto do ótimo.
    assert custo_ciclo(construtivo, matriz) <= otimo * 1.25
    assert otimo - 1e-9 <= custo_ciclo(melhorado, matriz) <= custo_ciclo(construtivo, matriz) + 1e-9


def test_comeca_em():
    assert comeca_em([2, 0, 1]) == [0, 1, 2]


def test_matriz_nao_quadrada(tmp_path):
    arquivo = tmp_path / "m.txt"
    arquivo.write_text("0 1\n1 0 3\n")
    with pytest.raises(ValueError):
        le_matriz(arquivo)

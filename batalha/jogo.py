TAMANHO = 10
AGUA, NAVIO, ACERTO, ERRO = "~", "N", "X", "O"
FROTA = [5, 4, 3, 3, 2]


def criar_tabuleiro():
    return [[AGUA for _ in range(TAMANHO)] for _ in range(TAMANHO)]


def posicionar_navio(tab, linha, coluna, tamanho, orientacao):
    casas = []
    for i in range(tamanho):
        l = linha + i if orientacao == "V" else linha
        c = coluna + i if orientacao == "H" else coluna
        if not (0 <= l < TAMANHO and 0 <= c < TAMANHO):
            raise ValueError("Navio sai do tabuleiro")
        if tab[l][c] != AGUA:
            raise ValueError("Navio sobreposto")
        casas.append((l, c))
    for l, c in casas:
        tab[l][c] = NAVIO


def atirar(tab, linha, coluna):
    if not (0 <= linha < TAMANHO and 0 <= coluna < TAMANHO):
        raise ValueError("Tiro fora do tabuleiro")
    if tab[linha][coluna] in (ACERTO, ERRO):
        raise ValueError("Casa já atingida")
    if tab[linha][coluna] == NAVIO:
        tab[linha][coluna] = ACERTO
        return "acerto"
    tab[linha][coluna] = ERRO
    return "agua"


def perdeu(tab):
    return all(NAVIO not in linha for linha in tab)


def visao_do_inimigo(tab):
    return [[AGUA if casa == NAVIO else casa for casa in linha] for linha in tab]
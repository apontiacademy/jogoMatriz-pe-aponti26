import random
from time import sleep
import requests

SERVIDOR = "http://127.0.0.1:8000"
SALA = "turma1"
TIME = "sparring"


def montar_frota(frota):
    return [
        {"linha": i * 2, "coluna": 0, "tamanho": tamanho, "orientacao": "H"}
        for i, tamanho in enumerate(frota)
    ]


def escolher_tiro(mar_inimigo):
    livres = [
        (l, c)
        for l, linha in enumerate(mar_inimigo)
        for c, casa in enumerate(linha)
        if casa == "~"
    ]
    return random.choice(livres)


def main():
    url = f"{SERVIDOR}/{SALA}"
    frota = requests.post(f"{url}/entrar/", json={"time": TIME}).json()["frota"]

    resposta = requests.post(f"{url}/posicionar/", json={"time": TIME, "navios": montar_frota(frota)}).json()
    if "erro" in resposta:
        print("Frota recusada:", resposta["erro"])
        return
    print("Frota posicionada! Aguardando adversário...")

    while True:
        estado = requests.get(f"{url}/estado/", params={"time": TIME}).json()
        if estado["vencedor"]:
            print("Fim de jogo! Vencedor:", estado["vencedor"])
            break
        if estado["sua_vez"]:
            linha, coluna = escolher_tiro(estado["inimigo"])
            print((linha, coluna), requests.post(
                f"{url}/atirar/", json={"time": TIME, "linha": linha, "coluna": coluna}
            ).json())
        sleep(0.5)


if __name__ == "__main__":
    main()




























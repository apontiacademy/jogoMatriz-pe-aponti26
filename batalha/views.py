import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from . import jogo

SALAS = {}


def _sala(codigo):
    return SALAS.setdefault(codigo, {
        "times": {}, "ordem": [], "vez": 0, "vencedor": None, "log": []
    })


def _dados(request):
    return json.loads(request.body or "{}")


def _inimigo(sala, time):
    return [t for t in sala["ordem"] if t != time][0]


def _erro(msg):
    return JsonResponse({"erro": msg}, status=400)


@csrf_exempt
def entrar(request, codigo):
    time = _dados(request)["time"]
    sala = _sala(codigo)
    if time not in sala["times"] and len(sala["times"]) >= 2:
        return _erro("Sala cheia")
    sala["times"].setdefault(time, {"tabuleiro": jogo.criar_tabuleiro()})
    return JsonResponse({"ok": True, "frota": jogo.FROTA})


@csrf_exempt
def posicionar(request, codigo):
    dados = _dados(request)
    sala = _sala(codigo)
    if dados["time"] not in sala["times"]:
        return _erro("Time não entrou na sala")
    if sorted(n["tamanho"] for n in dados["navios"]) != sorted(jogo.FROTA):
        return _erro(f"A frota precisa ter os tamanhos {jogo.FROTA}")
    tab = jogo.criar_tabuleiro()
    try:
        for n in dados["navios"]:
            jogo.posicionar_navio(tab, n["linha"], n["coluna"], n["tamanho"], n["orientacao"])
    except ValueError as e:
        return _erro(str(e))
    sala["times"][dados["time"]]["tabuleiro"] = tab
    if dados["time"] not in sala["ordem"]:
        sala["ordem"].append(dados["time"])
    return JsonResponse({"ok": True})


def estado(request, codigo):
    sala = _sala(codigo)
    time = request.GET.get("time")
    pronta = len(sala["ordem"]) == 2
    resposta = {"pronta": pronta, "vencedor": sala["vencedor"], "sua_vez": False, "inimigo": None}
    if pronta and time in sala["ordem"]:
        inimigo = _inimigo(sala, time)
        resposta["sua_vez"] = sala["ordem"][sala["vez"]] == time and not sala["vencedor"]
        resposta["inimigo"] = jogo.visao_do_inimigo(sala["times"][inimigo]["tabuleiro"])
    return JsonResponse(resposta)


@csrf_exempt
def atirar(request, codigo):
    dados = _dados(request)
    sala = _sala(codigo)
    time = dados["time"]
    if len(sala["ordem"]) < 2 or sala["vencedor"]:
        return _erro("Partida não está em andamento")
    if sala["ordem"][sala["vez"]] != time:
        return _erro("Não é sua vez")
    alvo = sala["times"][_inimigo(sala, time)]["tabuleiro"]
    linha, coluna = dados["linha"], dados["coluna"]
    try:
        resultado = jogo.atirar(alvo, linha, coluna)
    except ValueError as e:
        sala["vez"] = 1 - sala["vez"]
        sala["log"].append(f"{time} errou a jogada: {e}")
        return _erro(str(e))
    sala["log"].append(f"{time} atirou em ({linha}, {coluna}): {resultado}")
    if jogo.perdeu(alvo):
        sala["vencedor"] = time
    elif resultado == "agua":
        sala["vez"] = 1 - sala["vez"]
    return JsonResponse({"resultado": resultado, "vencedor": sala["vencedor"]})


def painel(request, codigo):
    sala = _sala(codigo)
    tabuleiros = {nome: jogo.visao_do_inimigo(t["tabuleiro"]) for nome, t in sala["times"].items()}
    return render(request, "batalha/painel.html", {
        "codigo": codigo,
        "sala": sala,
        "tabuleiros": tabuleiros,
        "log": list(reversed(sala["log"][-10:])),
    })
# Batalha Naval: Coding Dojo em Python

Jogo de batalha naval em rede para Coding Dojo. Cada time programa um robô em Python que posiciona a frota e escolhe onde atirar. As partidas acontecem num servidor Django central e podem ser acompanhadas ao vivo pelo navegador.

O tabuleiro é uma matriz 10x10 (lista de listas), o que torna o jogo uma boa porta de entrada para trabalhar matrizes, laços, condicionais, funções e estratégia de resolução de problemas.

## Como funciona

O professor roda o servidor na máquina dele. Cada time recebe o arquivo `cliente_aluno.py`, que já cuida da comunicação com o servidor, e implementa duas funções:

- `montar_frota(frota)`: define onde ficam os navios.
- `escolher_tiro(mar_inimigo)`: decide a próxima casa a ser atacada.

O painel do navegador mostra os dois mares sendo atacados em tempo real, com os navios escondidos, então pode ser projetado para a turma inteira.

## Regras do jogo

- O mar tem 10 linhas por 10 colunas, numeradas de 0 a 9.
- A frota de cada time tem navios de tamanho 5, 4, 3, 3 e 2.
- Navios podem ficar na horizontal (`"H"`) ou na vertical (`"V"`), sem sair do mar e sem sobrepor outro navio.
- Quem acerta joga de novo. Quem acerta a água passa a vez.
- Tiro inválido (fora do mar ou em casa já atingida) faz o time perder a vez.
- Vence o time que afundar todos os navios do adversário primeiro.

No mar inimigo que o robô recebe, `"~"` é casa desconhecida, `"X"` é acerto e `"O"` é água.

## Estrutura do projeto

```
batalha_naval/
├── manage.py
├── sparring.py            robô de demonstração e treino
├── sparring2.py           cópia do sparring com outro nome de time
├── cliente_aluno.py       arquivo entregue aos times
├── arena/                 configuração do projeto Django
│   ├── settings.py
│   └── urls.py
└── batalha/               app do jogo
    ├── jogo.py            regras do jogo (só matriz, sem Django)
    ├── views.py           API e painel
    ├── urls.py            rotas do jogo
    └── templates/
        └── batalha/
            └── painel.html
```

## Instalação

### Linux (Ubuntu e derivados)

O Ubuntu bloqueia o `pip` fora de um ambiente virtual, então é preciso criar um dentro da pasta do projeto:

```
sudo apt install python3-venv python3-full
python3 -m venv .venv
source .venv/bin/activate
pip install django requests
```

Sempre que abrir um terminal novo, ative o ambiente antes de rodar qualquer coisa:

```
source .venv/bin/activate
```

### Windows

```
python -m venv .venv
.venv\Scripts\activate
pip install django requests
```

## Rodando uma partida de teste

São três terminais, todos dentro da pasta do projeto e com o ambiente ativado.

Terminal 1, o servidor:

```
python manage.py runserver
```

Terminal 2, o primeiro robô:

```
python sparring.py
```

Terminal 3, o segundo robô:

```
python sparring2.py
```

Depois, abra no navegador:

```
http://127.0.0.1:8000/turma1/
```

Os dois robôs precisam ter nomes de time diferentes (variável `TIME`), senão o servidor entende que são o mesmo time e a partida não começa.

## Jogando em rede na sala de aula

1. Rode o servidor aceitando conexões de outras máquinas:

```
   python manage.py runserver 0.0.0.0:8000
```

2. Descubra o IP da máquina do servidor com `ip a` (Linux) ou `ipconfig` (Windows), no campo IPv4.
3. No `cliente_aluno.py`, troque `IP_DO_PROFESSOR` por esse IP antes de distribuir aos times.
4. Cada dupla de times usa uma sala diferente, mudando a variável `SALA` (`turma1`, `turma2`, e assim por diante). Cada sala aceita dois times.
5. O painel de cada sala fica em `http://IP_DO_SERVIDOR:8000/NOME_DA_SALA/`.

Para treinar sem depender de outro time, uma equipe pode jogar contra o `sparring.py` numa sala própria, como `treino-azul`.

## API do servidor

Todas as rotas começam com o código da sala.

| Rota | Método | Corpo ou parâmetros | O que faz |
|------|--------|---------------------|-----------|
| `/<sala>/` | GET | | Painel da partida |
| `/<sala>/entrar/` | POST | `{"time": "nome"}` | Entra na sala e recebe a frota |
| `/<sala>/posicionar/` | POST | `{"time": "nome", "navios": [...]}` | Envia a posição dos navios |
| `/<sala>/estado/` | GET | `?time=nome` | Informa se é a sua vez e mostra o mar inimigo |
| `/<sala>/atirar/` | POST | `{"time": "nome", "linha": 0, "coluna": 0}` | Dispara um tiro |

Cada navio enviado em `navios` tem o formato:

```
{"linha": 0, "coluna": 0, "tamanho": 5, "orientacao": "H"}
```

## Níveis do dojo

- Rodada 1: implementar `escolher_tiro` devolvendo sempre uma casa ainda não atingida.
- Rodada 2: implementar `montar_frota` com posições e orientações sorteadas, respeitando os limites do mar e sem sobreposição.
- Rodada 3: melhorar `escolher_tiro` para, após um acerto, atacar as casas vizinhas em vez de atirar aleatoriamente.

## Problemas comuns

**`error: externally-managed-environment` ao usar o pip**
O ambiente virtual não foi criado ou não está ativado. Siga a seção de instalação.

**`ModuleNotFoundError: No module named 'django'` ou `'requests'`**
O terminal está sem o ambiente ativado. Rode `source .venv/bin/activate`.

**`ModuleNotFoundError: No module named 'batalha.urls'`**
Falta o arquivo `batalha/urls.py`. Existem dois `urls.py` no projeto: um em `arena` e outro em `batalha`, e os dois são necessários.

**`TemplateDoesNotExist: batalha/painel.html`**
O arquivo precisa estar em `batalha/templates/batalha/painel.html`, com a pasta `batalha` repetida dentro de `templates`.

**`Sala cheia`**
A sala já tem dois times de uma partida anterior. Reinicie o servidor (`Ctrl+C` e `runserver` de novo) ou use outro nome de sala. O jogo guarda tudo na memória, então reiniciar limpa todas as salas.

**Outras máquinas não conseguem conectar**
Confira se o servidor foi iniciado com `0.0.0.0:8000`, se o IP no cliente está correto e se o firewall permite conexões na porta 8000. Algumas redes Wi-Fi institucionais bloqueiam a comunicação entre computadores; nesse caso, teste com um roteador próprio ou com o roteador do celular.

**Aviso sobre "unapplied migrations" ao iniciar o servidor**
Pode ser ignorado, o jogo não usa banco de dados. Para remover o aviso, rode `python manage.py migrate` uma vez.

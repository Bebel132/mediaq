# Mediaq

Um *sequenciador/reprodutor* de mídia que opera exclusivamente em linha de comando. O programa carrega uma biblioteca de faixas a partir de um arquivo, monta playlists, simula a reprodução (sem áudio real, é claro!) e gerencia uma fila de reprodução imediata, um histórico de execução e um modo de embaralhamento inteligente. 

O foco do projeto está no uso adequado de quatro estruturas lineares distintas, cada uma cumprindo um papel funcional específico.

## Como executar
```bash
  git clone https://github.com/Bebel132/mediaq.git
  cd mediaq
  py main.py
```

## Exemplo de sessão
```bash
mediaq> library load library_exemplo.json 
Bibioteca carregada: 12 faixas
mediaq> playlist new minha
Playlist "minha" criada.
mediaq> playlist add 3
mediaq> playlist add 7
mediaq> playlist add 1
mediaq> playlist show
> 1. Azul — Zimbra (3:18)
2. Talvez Eu Esteja — Selvagens a Procura de Lei (3:27)
3. Verao — Zimbra (3:51)

mediaq> play     
>>> Tocando: "Azul" — Zimbra (3:18)
mediaq> enqueue 5
mediaq> next
>>> Tocando: "Destruicao" — Selvagens a Procura de Lei (3:30)
mediaq> next
>>> Tocando: "Talvez Eu Esteja" — Selvagens a Procura de Lei (3:27)
mediaq> next
>>> Tocando: "Verao" — Zimbra (3:51)
mediaq> next
Fim da playlist. Use 'playlist show' para ver as músicas ou 'enqueue <track_id>' para adicionar músicas à fila.
mediaq> history
1. Verao — Zimbra (3:51) - Tocada em [12:03:39]
2. Talvez Eu Esteja — Selvagens a Procura de Lei (3:27) - Tocada em [12:03:33]
3. Destruicao — Selvagens a Procura de Lei (3:30) - Tocada em [12:03:30]
4. Azul — Zimbra (3:18) - Tocada em [12:03:24]
mediaq> quit 
```

## Fórmula para o smart-shuffle

A função *smartShuffle(n)* recebe um número **n** de músicas da biblioteca, onde essas músicas são analisadas e ordenadas pela **avaliação** da música e, caso houver histórico, é calculado uma *"penalidade"* para as 5 últimas músicas que estão no histórico e nas selecionadas da biblioteca de acordo com a ordem em que foi reproduzida. Assim, a posição em que as músicas vão ser ordenadas é dada pela seguinte fórmula:

```
se a música estiver no historico:
    penalidade = 5 - posicao_no_historico
senão:
    penalidade = 0
# ou seja, a prioridade é maior para notas altas e diminui se a música foi tocada recentemente

chave = -(avaliacao * 10) + penalidade
# chave é o valor de prioridade da música para a nova playlist
```

Depois disso, é guardado em uma *tupla* a **chave** e a **música** em uma *PriorityQueue()*, é criado uma nova playlist e a lista será percorrida para adicionar as músicas ordenadas por prioridade na playlist

**Mas**, existe a possibilidade de não ter músicas no histórico, nesse caso, o calculo para obter a prioridade é a combinação da avaliação com um número aleatório

```
chave = (-(avaliacao * 10), random.random())
```
De resto, o funcionamento é o mesmo
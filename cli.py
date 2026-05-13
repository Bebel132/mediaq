import json
from pathlib import Path
from doubly_linked_list import DoublyLinkedList

# o dict é usado aqui ao invés do bool porque o bool não seria
# alterado dentro da função de sair, e sim só a cópia que é
# criada na função de sair, é como se a função de sair não
# conseguisse alcançar o valor do bool original
estado = {
    "rodando": True, 
    "musicas": [
        {
            "id": 1,
            "titulo": "Verao",
            "artista": "Zimbra",
            "duracao": 231,
            "avaliacao": 5,
            "data_adicao": "2026-05-11"
        },
        {
            "id": 2,
            "titulo": "O Que Era Certo",
            "artista": "Zimbra",
            "duracao": 214,
            "avaliacao": 4,
            "data_adicao": "2026-05-11"
        },
        {
            "id": 3,
            "titulo": "Azul",
            "artista": "Zimbra",
            "duracao": 198,
            "avaliacao": 4,
            "data_adicao": "2026-05-11"
        },
        {
            "id": 4,
            "titulo": "A Vida Passa",
            "artista": "Zimbra",
            "duracao": 245,
            "avaliacao": 5,
            "data_adicao": "2026-05-11"
        },
        {
            "id": 5,
            "titulo": "Destruicao",
            "artista": "Selvagens a Procura de Lei",
            "duracao": 210,
            "avaliacao": 4,
            "data_adicao": "2026-05-11"
        },
        {
            "id": 6,
            "titulo": "Mar Fechado",
            "artista": "Selvagens a Procura de Lei",
            "duracao": 223,
            "avaliacao": 5,
            "data_adicao": "2026-05-11"
        },
        {
            "id": 7,
            "titulo": "Talvez Eu Esteja",
            "artista": "Selvagens a Procura de Lei",
            "duracao": 207,
            "avaliacao": 3,
            "data_adicao": "2026-05-11"
        },
        {
            "id": 8,
            "titulo": "Sem Voce",
            "artista": "Selvagens a Procura de Lei",
            "duracao": 233,
            "avaliacao": 4,
            "data_adicao": "2026-05-11"
        },
        {
            "id": 9,
            "titulo": "Foco",
            "artista": "Menores Atos",
            "duracao": 201,
            "avaliacao": 4,
            "data_adicao": "2026-05-11"
        },
        {
            "id": 10,
            "titulo": "Luzes",
            "artista": "Menores Atos",
            "duracao": 219,
            "avaliacao": 5,
            "data_adicao": "2026-05-11"
        },
        {
            "id": 11,
            "titulo": "Vertigem",
            "artista": "Menores Atos",
            "duracao": 226,
            "avaliacao": 3,
            "data_adicao": "2026-05-11"
        },
        {
            "id": 12,
            "titulo": "Cores",
            "artista": "Menores Atos",
            "duracao": 212,
            "avaliacao": 4,
            "data_adicao": "2026-05-11"
        }
    ]
}

def rodar():
    while estado["rodando"]:
        entrada = input("mediaq> ").lower()
        entrada = entrada.split()

        # para lidar com comandos compostos como "library list" ou "playlist add"
        if len(entrada) == 2:
            entrada[0] = f"{entrada[0]} {entrada[1]}"
            entrada.pop()
        # para lidar com comandos compostos com argumentos, como "library load arquivo.json" ou "playlist add 3"
        if len(entrada) >= 3:
            entrada[0] = f"{entrada[0]} {entrada[1]}"
            entrada[1] = f"{' '.join(entrada[2:])}"
            del entrada[2:]

        aux = None
        for comando in comandos:
            if entrada[0] == comando["comando"]:
                aux = True
                # para verificar se o comando precisa de um argumento ou não, e chamar a função correspondente
                if len(entrada) == 1:
                    comando["funcao"]()
                if len(entrada) == 2:
                    comando["funcao"](entrada[1])
                if len(entrada) >= 3:
                    comando["funcao"](entrada[1:])
        if not aux:
            print("Comando não reconhecido. Digite 'help' para ver os comandos disponíveis.")


def funcaoQuit():
    estado["rodando"] = False


def funcaoBibliotecaCarregar(arquivo : str):
    if Path(arquivo).exists():
        print("-----------------------------------------")
        with open(arquivo, "r", encoding="utf-8") as f:
            estado["musicas"] = json.load(f)
        print(f"Bibioteca carregada: {len(estado['musicas'])} faixas")
        print("-----------------------------------------")
    else:
        print("Arquivo não encontrado.")


def funcaoBibliotecaListar(ordenacao : str | None = None):
    if ordenacao: ordenacao = ordenacao.split()[1]
    if not ordenacao: ordenacao = "id"

    if ordenacao not in ["rating", "title", "artist", "id"]:
        return print("Ordenação inválida. Use '--by rating', '--by title' ou '--by artist'.")
    

    if ordenacao == "rating":
        musicas_ordenadas = sorted(estado["musicas"], key=lambda musica: musica["avaliacao"])
    elif ordenacao == "title":
        musicas_ordenadas = sorted(estado["musicas"], key=lambda musica: musica["titulo"])
    elif ordenacao == "artist":
        musicas_ordenadas = sorted(estado["musicas"], key=lambda musica: musica["artista"])
    else:
        musicas_ordenadas = sorted(estado["musicas"], key=lambda musica: musica["id"])

    print("-----------------------------------------")
    for musica in musicas_ordenadas:
        # :02d adiciona um zero na esquerda se precisar
        print(f"{musica["titulo"]} — {musica["artista"]} ({musica["duracao"] // 60}:{musica["duracao"] % 60:02d})")
    print("-----------------------------------------")


def funcaoPlaylistNovo(nomePlaylist : str):
    playlist = DoublyLinkedList()
    estado["playlist"] = nomePlaylist
    estado["playlist_obj"] = playlist
    print(f'Playlist "{nomePlaylist}" criada.')


def funcaoPlaylistAdicionar(musica_id : str):
    if "playlist_obj" not in estado:
        return print("Nenhuma playlist criada. Use 'playlist new <nome>' para criar uma playlist.")
    
    id = int(musica_id)
    aux = None
    for musica in estado["musicas"]:
        if musica["id"] == id:
            aux = musica
            break
    
    if aux is None:
        print(f"Música com id {id} não encontrada na biblioteca.")
    else:
        estado["playlist_obj"].add(aux)


def funcaoPlaylistRemover(pos : str):
    if "playlist_obj" not in estado:
        return print("Nenhuma playlist criada. Use 'playlist new <nome>' para criar uma playlist.")

    estado["playlist_obj"].remove_at(int(pos) - 1)


def funcaoPlaylistMostrar():
    if "playlist_obj" not in estado:
        return print("Nenhuma playlist criada. Use 'playlist new <nome>' para criar uma playlist.")
    print(estado["playlist_obj"])


def funcaoTocar():
    if "playlist_obj" not in estado:
        return print("Nenhuma playlist criada. Use 'playlist new <nome>' para criar uma playlist.")
    musica = estado["playlist_obj"].current()
    return print(f'>>> Tocando: "{musica.get("titulo")}" — {musica.get("artista")} ({musica.get("duracao") // 60}:{musica.get("duracao") % 60:02d})')


def funcaoProximo():
    if "playlist_obj" not in estado:
        return print("Nenhuma playlist criada. Use 'playlist new <nome>' para criar uma playlist.")
    estado["playlist_obj"].move_next()
    return funcaoTocar()


def funcaoAnterior():
    if "playlist_obj" not in estado:
        return print("Nenhuma playlist criada. Use 'playlist new <nome>' para criar uma playlist.")
    estado["playlist_obj"].move_prev()
    return funcaoTocar()


def funcaoEnfileirar():
    return 


def funcaoMostrarFila():
    return 


def funcaoHistorico():
    return 


def funcaoSmartShuffle():
    return 


def funcaoSalvar():
    return


def funcaoCarregar():
    return


def funcaoAjuda():
    print("-----------------------------------------")
    for comando in comandos:
        if comando['opcao']:
            print(f"{comando['comando']} {comando['opcao']}")
        else:
            print(comando['comando'])
    print("-----------------------------------------")


comandos = [
    {'comando': 'library list', 'opcao': '[--by rating|title|artist]', 'funcao': funcaoBibliotecaListar},
    {'comando': 'library load', 'opcao': '<arquivo>', 'funcao': funcaoBibliotecaCarregar},
    {'comando': 'playlist new', 'opcao': '<nome>', 'funcao': funcaoPlaylistNovo},
    {'comando': 'playlist add', 'opcao': 'track_id', 'funcao': funcaoPlaylistAdicionar},
    {'comando': 'playlist remove', 'opcao': 'pos', 'funcao': funcaoPlaylistRemover},
    {'comando': 'playlist show', 'opcao': None, 'funcao': funcaoPlaylistMostrar},
    {'comando': 'play', 'opcao': None, 'funcao': funcaoTocar},
    {'comando': 'next', 'opcao': None, 'funcao': funcaoProximo},
    {'comando': 'prev', 'opcao': None, 'funcao': funcaoAnterior},
    {'comando': 'enqueue', 'opcao': '<track_id>', 'funcao': funcaoEnfileirar},
    {'comando': 'queue show', 'opcao': None, 'funcao': funcaoMostrarFila},
    {'comando': 'history', 'opcao': None, 'funcao': funcaoHistorico},
    {'comando': 'smart-shuffle', 'opcao': '<n>', 'funcao': funcaoSmartShuffle},
    {'comando': 'save', 'opcao': '<arquivo>', 'funcao': funcaoSalvar},
    {'comando': 'load', 'opcao': '<arquivo>', 'funcao': funcaoCarregar},
    {'comando': 'help', 'opcao': None, 'funcao': funcaoAjuda},
    {'comando': 'quit', 'opcao': None, 'funcao': funcaoQuit},
]
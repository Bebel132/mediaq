from player import Player


player = Player(musicas=[
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
    ])

def rodar():
    player.registrarComandos()
    while player.rodando:
        entrada = input("mediaq> ").lower()
        entrada = entrada.split()
        # para lidar com comandos compostos como "library list" ou "playlist add"
        if len(entrada) == 2 and entrada[0] != "enqueue": # excessão pro unico comando simples que tem um argumento
            entrada[0] = f"{entrada[0]} {entrada[1]}"
            entrada.pop()
        # para lidar com comandos compostos com argumentos, como "library load arquivo.json" ou "playlist add 3"
        if len(entrada) >= 3:
            entrada[0] = f"{entrada[0]} {entrada[1]}"
            entrada[1] = f"{' '.join(entrada[2:])}"
            del entrada[2:]
        
        aux = None
        for comando in player.comandos:
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
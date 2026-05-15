from player import Player


player = Player()

def rodar():
    player.registrarComandos()
    while player.rodando:
        entrada = input("mediaq> ").lower()
        entrada = entrada.split()
        # para lidar com comandos compostos como "library list" ou "playlist add"
        if len(entrada) == 2 and entrada[0] not in ["enqueue", "smart-shuffle", "save", "load"]: # excessão pro unico comando simples que tem um argumento
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
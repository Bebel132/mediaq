from player import MediaPlayer


player = MediaPlayer()

def run():
    player.registerCommands()
    while player.running:
        user_input = input("mediaq> ").lower()
        user_input = user_input.split()
        # para lidar com comandos compostos como "library list" ou "playlist add"
        if len(user_input) == 2 and user_input[0] not in ["enqueue", "smart-shuffle", "save", "load"]: # excessão pro unico comando simples que tem um argumento
            user_input[0] = f"{user_input[0]} {user_input[1]}"
            user_input.pop()
        # para lidar com comandos compostos com argumentos, como "library load arquivo.json" ou "playlist add 3"
        if len(user_input) >= 3:
            user_input[0] = f"{user_input[0]} {user_input[1]}"
            user_input[1] = f"{' '.join(user_input[2:])}"
            del user_input[2:]
        
        aux = None
        for command in player.commands:
            if user_input[0] == command["command"]:
                aux = True
                # para verificar se o comando precisa de um argumento ou não, e chamar a função correspondente
                if len(user_input) == 1:
                    command["function"]()
                
                if len(user_input) == 2:
                    if command["input_type"] == str:
                        command["function"](user_input[1])
                    elif command["input_type"] == int:
                        command["function"](int(user_input[1]))
                        
                if len(user_input) >= 3:
                    if command["input_type"] == str:
                        command["function"](user_input[1:])
                    elif command["input_type"] == int:
                        command["function"](int(user_input[1]))

        if not aux:
            print("Comando não reconhecido. Digite 'help' para ver os comandos disponíveis.")
from datetime import datetime
import json
from pathlib import Path
import random
from doubly_linked_list import DoublyLinkedList
from collections import deque
from queue import PriorityQueue

class Player:
    def __init__(
            self, 
            rodando : bool = True,
            comandos: list = [],
            musicas: list = [],
            playlist_obj: DoublyLinkedList | None = None,
            filaUpNext: deque = deque(),
        ):
        self.rodando = rodando;
        self.comandos = comandos;
        self.musicas = musicas;
        self.playlist_obj = playlist_obj;
        self.filaUpNext = filaUpNext;
        self.historicoLista = deque(maxlen=20)

    def quit(self):
        self.rodando = False


    def bibliotecaCarregar(self, arquivo : str):
        if Path(arquivo).exists():
            with open(arquivo, "r", encoding="utf-8") as f:
                self.musicas = json.load(f)
            print(f"Bibioteca carregada: {len(self.musicas)} faixas")
        else:
            print("Arquivo não encontrado.")


    def bibliotecaListar(self, ordenacao : str | None = None):
        if ordenacao: ordenacao = ordenacao.split()[1]
        if not ordenacao: ordenacao = "id"

        if ordenacao not in ["rating", "title", "artist", "id"]:
            return print("Ordenação inválida. Use '--by rating', '--by title' ou '--by artist'.")
        

        if ordenacao == "rating":
            musicas_ordenadas = sorted(self.musicas, key=lambda musica: musica["avaliacao"])
        elif ordenacao == "title":
            musicas_ordenadas = sorted(self.musicas, key=lambda musica: musica["titulo"])
        elif ordenacao == "artist":
            musicas_ordenadas = sorted(self.musicas, key=lambda musica: musica["artista"])
        else:
            musicas_ordenadas = sorted(self.musicas, key=lambda musica: musica["id"])

        for musica in musicas_ordenadas:
            # :02d adiciona um zero na esquerda se precisar
            print(f"{musica["titulo"]} — {musica["artista"]} ({musica["duracao"] // 60}:{musica["duracao"] % 60:02d})")


    def playlistNovo(self,nomePlaylist : str):
        playlist = DoublyLinkedList()
        self.playlist = nomePlaylist
        self.playlist_obj = playlist
        print(f'Playlist "{nomePlaylist}" criada.')


    def playlistAdicionar(self, musica_id : str):
        if self.playlist_obj is None:
            return print("Nenhuma playlist criada. Use 'playlist new <nome>' para criar uma playlist.")
        
        id = int(musica_id)
        aux = None
        for musica in self.musicas:
            if musica["id"] == id:
                aux = musica
                break
        
        if aux is None:
            print(f"Música com id {id} não encontrada na biblioteca.")
        else:
            self.playlist_obj.add(aux)


    def playlistRemover(self, pos : str):
        if self.playlist_obj is None:
            return print("Nenhuma playlist criada. Use 'playlist new <nome>' para criar uma playlist.")

        self.playlist_obj.remove_at(int(pos) - 1)


    def playlistMostrar(self):
        if self.playlist_obj is None:
            return print("Nenhuma playlist criada. Use 'playlist new <nome>' para criar uma playlist.")
        print(self.playlist_obj)


    def tocar(self):
        if self.playlist_obj is None:
            return print("Nenhuma playlist criada. Use 'playlist new <nome>' para criar uma playlist.")
        else:
            musica = self.playlist_obj.current() 
            self.historicoLista.append((musica, datetime.now()))
            
            return print(f'>>> Tocando: "{musica.get("titulo")}" — {musica.get("artista")} ({musica.get("duracao") // 60}:{musica.get("duracao") % 60:02d})')


    def proximo(self):
        if self.playlist_obj is None:
            return print("Nenhuma playlist criada. Use 'playlist new <nome>' para criar uma playlist.")
        else:
            if len(self.filaUpNext) > 0:
                musica = self.filaUpNext.popleft()
                self.historicoLista.append((musica, datetime.now()))
                print(f'>>> Tocando: "{musica.get("titulo")}" — {musica.get("artista")} ({musica.get("duracao") // 60}:{musica.get("duracao") % 60:02d})')
            else:
                if self.playlist_obj.move_next():
                    self.tocar()
                else:
                    print("Fim da playlist. Use 'playlist show' para ver as músicas ou 'enqueue <track_id>' para adicionar músicas à fila.")


    def anterior(self):
        if self.playlist_obj is None:
            return print("Nenhuma playlist criada. Use 'playlist new <nome>' para criar uma playlist.")
        else:
            if self.playlist_obj.move_prev():
                self.tocar()
            else:
                print("Início da playlist. Use 'playlist show' para ver as músicas ou 'enqueue <track_id>' para adicionar músicas à fila.")


    def enfileirar(self, musica_id : str):
        if self.playlist_obj is None:
            return print("Nenhuma playlist criada. Use 'playlist new <nome>' para criar uma playlist.")
        else:
            id = int(musica_id)
            aux = None
            for musica in self.musicas:
                if musica["id"] == id:
                    aux = musica
                    break

            if aux is None:
                print(f"Música com id {id} não encontrada na biblioteca.")
            else:
                self.filaUpNext.append(aux)


    def mostrarFila(self):
        for musica in self.filaUpNext:
            print(f"{musica.get('titulo')} — {musica.get('artista')} ({musica.get('duracao') // 60}:{musica.get('duracao') % 60:02d})")


    def historico(self):
        # interar ao contrário para mostrar a música mais recente primeiro
        for i in range(len(self.historicoLista)-1, -1, -1):
            musica, timestamp = self.historicoLista[i]
            print(f"{len(self.historicoLista) - i}. {musica.get('titulo')} — {musica.get('artista')} ({musica.get('duracao') // 60}:{musica.get('duracao') % 60:02d}) - Tocada em [{timestamp.strftime('%H:%M:%S')}]")


    def smartShuffle(self, n : str):
        musicas = self.musicas[:int(n)]
        lista = PriorityQueue()
        
        if len(self.historicoLista) != 0:
            historico = [item[0] for item in list(self.historicoLista)[-5:]]
            
            for musica in musicas:
                posicao_no_historico = 0

                for i in range(len(historico)-1, -1, -1):
                    if musica.get("id") == historico[i].get("id"):
                        musica.get("id")
                        historico[i].get("id")
                        posicao_no_historico = len(historico) - i
                        break

                penalidade = 0
                if posicao_no_historico != 0:
                    penalidade = 5 - posicao_no_historico

                chave = -(musica['avaliacao'] * 10) + penalidade
                lista.put((chave, musica))
            
            self.playlistNovo("Smart Shuffle")
            while not lista.empty():
                chave, musica = lista.get()
                self.playlistAdicionar(musica["id"])
            
            self.playlistMostrar()
        else:
            for musica in musicas:
                chave = (-(musica['avaliacao'] * 10), random.random())
                lista.put((chave, musica))
            
            self.playlistNovo("Smart Shuffle")
            while not lista.empty():
                chave, musica = lista.get()
                self.playlistAdicionar(musica["id"])
            
            self.playlistMostrar()


    def salvar(self, arquivo):
        if not arquivo:
            print("Arquivo não informado.")
            return

        playlist_ids = []
        cursor_index = None
        if self.playlist_obj is not None:
            playlist_ids = []
            for musica in self.playlist_obj:
                if musica is not None:
                    playlist_ids.append(musica.get("id"))
            cursor_track = self.playlist_obj.current()
            if cursor_track is not None:
                try:
                    cursor_index = playlist_ids.index(cursor_track.get("id"))
                except ValueError:
                    cursor_index = None

        fila_ids = [musica.get("id") for musica in self.filaUpNext if musica is not None]
        historico = []
        for musica, timestamp in self.historicoLista:
            if musica is None:
                continue
            historico.append(
                {
                    "id": musica.get("id"),
                    "timestamp": timestamp.isoformat(),
                }
            )

        estado = {
            "musicas": self.musicas,
            "playlist": {
                "nome": getattr(self, "playlist", None),
                "tracks": playlist_ids,
                "cursor_index": cursor_index,
            },
            "fila_up_next": fila_ids,
            "historico": historico,
        }

        with open(arquivo, "w", encoding="utf-8") as f:
            json.dump(estado, f, indent=2)
        print(f"Estado salvo em {arquivo}.")
        return


    def carregar(self, arquivo):
        if not arquivo or not Path(arquivo).exists():
            print("Arquivo não encontrado.")
            return

        with open(arquivo, "r", encoding="utf-8") as f:
            estado = json.load(f)

        self.musicas = estado.get("musicas", [])
        musicas_por_id = {musica.get("id"): musica for musica in self.musicas}

        playlist_info = estado.get("playlist", {})
        self.playlist = playlist_info.get("nome")
        self.playlist_obj = DoublyLinkedList()
        for track_id in playlist_info.get("tracks", []):
            musica = musicas_por_id.get(track_id)
            if musica is not None:
                self.playlist_obj.add(musica)

        cursor_index = playlist_info.get("cursor_index")
        if cursor_index is not None and self.playlist_obj is not None:
            self.playlist_obj.reset_cursor()
            for _ in range(cursor_index):
                if not self.playlist_obj.move_next():
                    break

        self.filaUpNext = deque()
        for track_id in estado.get("fila_up_next", []):
            musica = musicas_por_id.get(track_id)
            if musica is not None:
                self.filaUpNext.append(musica)

        self.historicoLista = deque(maxlen=20)
        for item in estado.get("historico", []):
            musica = musicas_por_id.get(item.get("id"))
            if musica is None:
                continue
            timestamp_str = item.get("timestamp")
            try:
                timestamp = datetime.fromisoformat(timestamp_str)
            except (TypeError, ValueError):
                timestamp = datetime.now()
            self.historicoLista.append((musica, timestamp))

        print(f"Estado carregado de {arquivo}.")
        return
    
    def registrarComandos(self):
        self.comandos = [
            {'comando': 'library list', 'opcao': '[--by rating|title|artist]', 'funcao': self.bibliotecaListar},
            {'comando': 'library load', 'opcao': '<arquivo>', 'funcao': self.bibliotecaCarregar},
            {'comando': 'playlist new', 'opcao': '<nome>', 'funcao': self.playlistNovo},
            {'comando': 'playlist add', 'opcao': 'track_id', 'funcao': self.playlistAdicionar},
            {'comando': 'playlist remove', 'opcao': 'pos', 'funcao': self.playlistRemover},
            {'comando': 'playlist show', 'opcao': None, 'funcao': self.playlistMostrar},
            {'comando': 'play', 'opcao': None, 'funcao': self.tocar},
            {'comando': 'next', 'opcao': None, 'funcao': self.proximo},
            {'comando': 'prev', 'opcao': None, 'funcao': self.anterior},
            {'comando': 'enqueue', 'opcao': '<track_id>', 'funcao': self.enfileirar},
            {'comando': 'queue show', 'opcao': None, 'funcao': self.mostrarFila},
            {'comando': 'history', 'opcao': None, 'funcao': self.historico},
            {'comando': 'smart-shuffle', 'opcao': '<n>', 'funcao': self.smartShuffle},
            {'comando': 'save', 'opcao': '<arquivo>', 'funcao': self.salvar},
            {'comando': 'load', 'opcao': '<arquivo>', 'funcao': self.carregar},
            {'comando': 'help', 'opcao': None, 'funcao': self.ajuda},
            {'comando': 'quit', 'opcao': None, 'funcao': self.quit},
        ]


    def ajuda(self):
        for comando in self.comandos:
            if comando['opcao']:
                print(f"{comando['comando']} {comando['opcao']}")
            else:
                print(comando['comando'])
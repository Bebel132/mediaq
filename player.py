from datetime import datetime
import json
from pathlib import Path
import random

from mediaq.models import Track
from mediaq.doubly_linked_list import DoublyLinkedList
from collections import deque
from queue import PriorityQueue

class MediaPlayer:
    def __init__(
            self, 
            running : bool = True,
            commands: list = [],
            playlist: DoublyLinkedList | None = None,
            up_next: deque = deque(),
        ):
        self.running = running;
        self.commands = commands;
        self.library = [];
        self.playlist = playlist;
        self.playlist_name = None
        self.up_next = up_next;
        self.history = deque(maxlen=20)

    def quit(self):
        self.running = False


    def load_library(self, file : str):
        if Path(file).exists():
            with open(file, "r", encoding="utf-8") as f:
                tracks = json.load(f)
                for track in tracks:
                    self.library.append(Track(
                        id=track.get("id"),
                        title=track.get("title"),
                        artist=track.get("artist"),
                        duration=track.get("duration"),
                        rating=track.get("rating"),
                        data_adicao=track.get("date_added"),   
                    ))
            print(f"Bibioteca carregada: {len(self.library)} faixas")
        else:
            print("Arquivo não encontrado.")


    def list_library(self, ordering : str | None = None):
        if ordering: ordering = ordering.split()[1]
        if not ordering: ordering = "id"

        if ordering not in ["rating", "title", "artist", "id"]:
            return print("Ordenação inválida. Use '--by rating', '--by title' ou '--by artist'.")
        

        if ordering == "rating":
            ordered_library = sorted(self.library, key=lambda track: track.rating)
        elif ordering == "title":
            ordered_library = sorted(self.library, key=lambda track: track.title)
        elif ordering == "artist":
            ordered_library = sorted(self.library, key=lambda track: track.artist)
        else:
            ordered_library = sorted(self.library, key=lambda track: track.id)

        for track in ordered_library:
            # :02d adiciona um zero na esquerda se precisar
            #print(f"{track.title} — {track.artist} ({track.duration // 60}:{track.duration % 60:02d})")
            print(f"{track.id}: {track.title} — {track.artist} {track.duration}")


    def new_playlist(self,nomePlaylist : str):
        playlist = DoublyLinkedList()
        self.playlist_name = nomePlaylist
        self.playlist = playlist
        print(f'Playlist "{nomePlaylist}" criada.')


    def add_to_playlist(self, id : int):
        if self.playlist is None:
            return print("Nenhuma playlist criada. Use 'playlist new <nome>' para criar uma playlist.")
        
        aux = None
        for track in self.library:
            if track.id == id:
                aux = track
                break
        
        if aux is None:
            print(f"Música com id {id} não encontrada na biblioteca.")
        else:
            self.playlist.add(aux)


    def remove_from_playlist(self, pos : str):
        if self.playlist is None:
            return print("Nenhuma playlist criada. Use 'playlist new <nome>' para criar uma playlist.")

        self.playlist.remove_at(int(pos) - 1)


    def playlist_show(self):
        if self.playlist is None:
            return print("Nenhuma playlist criada. Use 'playlist new <nome>' para criar uma playlist.")
        print(self.playlist)


    def play(self):
        if self.playlist is None:
            return print("Nenhuma playlist criada. Use 'playlist new <nome>' para criar uma playlist.")
        else:
            if len(self.up_next) > 0:
                track = self.up_next.popleft()
                self.history.append((track, datetime.now()))
                print(f'>>> Tocando: "{track.title}" — {track.artist} ({track.duration // 60}:{track.duration % 60:02d})')
                return track
            else:
                track = self.playlist.current() 
                self.history.append((track, datetime.now()))
                print(f'>>> Tocando: "{track.title}" — {track.artist} ({track.duration // 60}:{track.duration % 60:02d})')
                return track


    def next(self):
        if self.playlist is None:
            return print("Nenhuma playlist criada. Use 'playlist new <nome>' para criar uma playlist.")
        else:
            if len(self.up_next) > 0:
                track = self.up_next.popleft()
                self.history.append((track, datetime.now()))
                print(f'>>> Tocando: "{track.title}" — {track.artist} ({track.duration // 60}:{track.duration % 60:02d})')
                return track
            else:
                if self.playlist.move_next():
                    return self.play()
                else:
                    print("Fim da playlist. Use 'playlist show' para ver as músicas ou 'enqueue <track_id>' para adicionar músicas à fila.")


    def prev(self):
        if self.playlist is None:
            return print("Nenhuma playlist criada. Use 'playlist new <nome>' para criar uma playlist.")
        else:
            if self.playlist.move_prev():
                return self.play()
            else:
                print("Início da playlist. Use 'playlist show' para ver as músicas ou 'enqueue <track_id>' para adicionar músicas à fila.")


    def enqueue(self, id : int):
        if self.playlist is None:
            return print("Nenhuma playlist criada. Use 'playlist new <nome>' para criar uma playlist.")
        else:
            aux = None
            for track in self.library:
                if track.id == id:
                    aux = track
                    break

            if aux is None:
                print(f"Música com id {id} não encontrada na biblioteca.")
            else:
                self.up_next.append(aux)


    def queue_show(self):
        for track in self.up_next:
            print(f"{track.title} — {track.artist} ({track.duration // 60}:{track.duration % 60:02d})")


    def playback_history(self):
        # interar ao contrário para mostrar a música mais recente primeiro
        for i in range(len(self.history)-1, -1, -1):
            track, timestamp = self.history[i]
            print(f"{len(self.history) - i}. {track.title} — {track.artist} ({track.duration // 60}:{track.duration % 60:02d}) - Tocada em [{timestamp.strftime('%H:%M:%S')}]")


    def smart_shuffle(self, n : int):
        library = self.library[:n]
        lista = PriorityQueue()
        
        if len(self.history) != 0:
            historico = [item[0] for item in list(self.history)[-5:]]
            
            for track in library:
                posicao_no_historico = 0

                for i in range(len(historico)-1, -1, -1):
                    if track.id == historico[i].id:
                        track.id
                        historico[i].id
                        posicao_no_historico = len(historico) - i
                        break

                penalidade = 0
                if posicao_no_historico != 0:
                    penalidade = 5 - posicao_no_historico

                chave = -(track.rating * 10) + penalidade
                lista.put((chave, track))
            
            self.new_playlist("Smart Shuffle")
            while not lista.empty():
                chave, track = lista.get()
                self.add_to_playlist(track.id)
            
            self.playlist_show()
        else:
            for track in library:
                chave = (-(track.rating * 10), random.random())
                lista.put((chave, track))
            
            self.new_playlist("Smart Shuffle")
            while not lista.empty():
                chave, track = lista.get()
                self.add_to_playlist(track.id)
            
            self.playlist_show()


    def save_state(self, arquivo):
        if not arquivo:
            print("Arquivo não informado.")
            return

        playlist_ids = []
        cursor_index = None
        if self.playlist is not None:
            playlist_ids = []
            for track in self.playlist:
                if track is not None:
                    playlist_ids.append(track.id)
            cursor_track = self.playlist.current()
            if cursor_track is not None:
                try:
                    cursor_index = playlist_ids.index(cursor_track.id)
                except ValueError:
                    cursor_index = None

        up_next_ids = [track.id for track in self.up_next if track is not None]
        history = []
        for track, timestamp in self.history:
            print(track)
            if track is None:
                continue
            history.append(
                {
                    "id": track.id,
                    "timestamp": timestamp.isoformat(),
                }
            )
        library = []
        for track in self.library:
            library.append(
                {
                    "id": track.id,
                    "title": track.title,
                    "artist": track.artist,
                    "duration": track.duration,
                    "rating": track.rating,
                    "date_added": track.data_adicao,
                }
            )

        estado = {
            "library": library,
            "playlist": {
                "nome": self.playlist_name,
                "tracks": playlist_ids,
                "cursor_index": cursor_index,
            },
            "up_next": up_next_ids,
            "history": history,
        }

        with open(arquivo, "w", encoding="utf-8") as f:
            json.dump(estado, f, indent=2)
        print(f"Estado salvo em {arquivo}.")
        return


    def load_state(self, arquivo):
        if not arquivo:
            print("Arquivo não informado.")
            return

        if not Path(arquivo).exists():
            print("Arquivo não encontrado.")
            return

        with open(arquivo, "r", encoding="utf-8") as f:
            estado = json.load(f)

        library_data = estado.get("library", [])
        if library_data:
            self.library = []
            for track in library_data:
                self.library.append(
                    Track(
                        id=track.get("id"),
                        title=track.get("title"),
                        artist=track.get("artist"),
                        duration=track.get("duration"),
                        rating=track.get("rating"),
                        data_adicao=track.get("date_added") or track.get("data_adicao"),
                    )
                )

        id_to_track = {}
        for track in self.library:
            if track is not None:
                id_to_track[track.id] = track

        playlist_data = estado.get("playlist", {})
        playlist_ids = playlist_data.get("tracks", []) or []
        cursor_index = playlist_data.get("cursor_index")
        self.playlist_name = playlist_data.get("nome")

        playlist = DoublyLinkedList()
        for track_id in playlist_ids:
            track = id_to_track.get(track_id)
            if track is not None:
                playlist.add(track)

        if len(playlist) > 0:
            if isinstance(cursor_index, int) and 0 <= cursor_index < len(playlist):
                playlist.reset_cursor()
                for _ in range(cursor_index):
                    playlist.move_next()
            elif cursor_index is None:
                playlist._cursor = None
            else:
                playlist.reset_cursor()

        self.playlist = playlist

        self.up_next = deque()
        for track_id in estado.get("up_next", []) or []:
            track = id_to_track.get(track_id)
            if track is not None:
                self.up_next.append(track)

        self.history = deque(maxlen=20)
        for item in estado.get("history", []) or []:
            if not isinstance(item, dict):
                continue
            track = id_to_track.get(item.get("id"))
            if track is None:
                continue
            timestamp = item.get("timestamp")
            if timestamp:
                try:
                    ts = datetime.fromisoformat(timestamp)
                except ValueError:
                    ts = None
            else:
                ts = None
            self.history.append((track, ts))

        print(f"Estado carregado de {arquivo}.")
        return
    
    def registerCommands(self):
        self.commands = [
            {'command': 'library list', 'option': '[--by rating|title|artist]', 'function': self.list_library, 'input_type': str},
            {'command': 'library load', 'option': '<arquivo>', 'function': self.load_library, 'input_type': str},
            {'command': 'playlist new', 'option': '<nome>', 'function': self.new_playlist, 'input_type': str},
            {'command': 'playlist add', 'option': 'track_id', 'function': self.add_to_playlist, 'input_type': int},
            {'command': 'playlist remove', 'option': 'pos', 'function': self.remove_from_playlist, 'input_type': int},
            {'command': 'playlist show', 'option': None, 'function': self.playlist_show, 'input_type': None},
            {'command': 'play', 'option': None, 'function': self.play, 'input_type': None},
            {'command': 'next', 'option': None, 'function': self.next, 'input_type': None},
            {'command': 'prev', 'option': None, 'function': self.prev, 'input_type': None},
            {'command': 'enqueue', 'option': '<track_id>', 'function': self.enqueue, 'input_type': int},
            {'command': 'queue show', 'option': None, 'function': self.queue_show, 'input_type': None},
            {'command': 'history', 'option': None, 'function': self.playback_history, 'input_type': None},
            {'command': 'smart-shuffle', 'option': '<n>', 'function': self.smart_shuffle, 'input_type': int},
            {'command': 'save', 'option': '<arquivo>', 'function': self.save_state, 'input_type': str},
            {'command': 'load', 'option': '<arquivo>', 'function': self.load_state, 'input_type': str},
            {'command': 'help', 'option': None, 'function': self.help, 'input_type': None},
            {'command': 'quit', 'option': None, 'function': self.quit, 'input_type': None},
        ]


    def help(self):
        for command in self.commands:
            if command['option']:
                print(f"{command['command']} {command['option']}")
            else:
                print(command['command'])
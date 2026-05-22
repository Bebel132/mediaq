class DoublyLinkedList():
    class _DoublyNode:
        def __init__(self, track, prev, next):
            self._track = track
            self._prev = prev
            self._next = next

        def __str__(self):
            if self._track is not None:
                track = self._track
                return f"{track.title} — {track.artist} ({track.duration // 60}:{track.duration % 60:02d})\n"
            else:
                return '|'

        @property
        def track(self):
            return self._track

        @track.setter
        def track(self, track):
            self._track = track

        @property
        def previous(self):
            return self._prev

        @previous.setter
        def previous(self, node):
            self._prev = node

        @property
        def next(self):
            return self._next

        @next.setter
        def next(self, node):
            self._next = node

    def __init__(self, size=0):
        self._header = self._DoublyNode(None, None, None)
        self._trailer = self._DoublyNode(None, None, None)
        self._header.next = self._trailer
        self._trailer.previous = self._header
        self._cursor = None
        self._length = 0

        
    def add(self, track):
        if self.empty():
            new_track = self._DoublyNode(track, self._header, self._trailer)
            self._header.next = new_track
            self._trailer.previous = new_track
            self._cursor = new_track
        else:
            new_track = self._DoublyNode(track, self._trailer.previous, self._trailer)
            self._trailer.previous.next = new_track
            self._trailer.previous = new_track
        self._length += 1

    def remove_at(self, pos):
        if pos >= self._length or pos < 0:
            raise IndexError("Posição inválida")

        atual = self._header.next
        for _ in range(pos):
            atual = atual.next

        atual.previous.next = atual.next
        atual.next.previous = atual.previous

        if self._cursor == atual:
            if atual.next != self._trailer:
                self._cursor = atual.next
            elif atual.previous != self._header:
                self._cursor = atual.previous
            else:
                self._cursor = None

        self._length -= 1

    def current(self):
        if self._cursor is None:
            return None
        return self._cursor.track
    
    def move_next(self):
        if self._cursor is not None and self._cursor.next != self._trailer:
            self._cursor = self._cursor.next
            return True
        else:
            return False
        
    def move_prev(self):
        if self._cursor is not None and self._cursor.previous != self._header:
            self._cursor = self._cursor.previous
            return True
        else:
            return False
        
    def reset_cursor(self):
        self._cursor = self._header.next

    def empty(self):
        return self._length == 0
    
    def __iter__(self):
        itens = []
        current = self._header.next
        while current != self._trailer:
            itens.append(current.track)
            current = current.next
        return iter(itens)

    def __len__(self):
        return self._length
    
    def __str__(self):
        result = ''
        count = 1
        current = self._header.next
        while current != self._trailer:
            if current == self._cursor:
                result += f'> {count}. ' + str(current)
            else:
                result += f'  {count}. ' + str(current)
            current = current.next
            count += 1
        return result
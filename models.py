class Track:
    def __init__(self, id: int, title: str, artist: str, duration: int, rating: int, data_adicao: str):
        self.__id = id
        self.__title = title
        self.__artist = artist
        self.__duration = duration
        self.__rating = rating
        self.__data_adicao = data_adicao

    @property
    def id(self):
        return self.__id

    @property
    def title(self):
        return self.__title
    
    @title.setter
    def title(self, title):
        self.__title = title
    
    @property
    def artist(self):
        return self.__artist
    
    @artist.setter
    def artist(self, artist):
        self.__artist = artist

    @property
    def duration(self):
        return self.__duration
    
    @duration.setter
    def duration(self, duration):
        self.__duration = duration

    @property
    def rating(self):
        return self.__rating
    
    @rating.setter
    def rating(self, rating):
        self.__rating = rating

    @property
    def data_adicao(self):
        return self.__data_adicao
    
    @data_adicao.setter
    def data_adicao(self, data_adicao):
        self.__data_adicao = data_adicao

    def __str__(self):
        return f'{self.__id} - {self.__title} - {self.__artist} - {self.__duration} - {self.__rating} - {self.__data_adicao}'
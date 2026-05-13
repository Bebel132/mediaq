import datetime


class Track:
    def __init__(self, id: int, titulo: str, artista: str, duracao: int, avaliacao: int, data_adicao: str):
        self.__id = id
        self.__titulo = titulo
        self.__artista = artista
        self.__duracao = duracao
        self.__avaliacao = avaliacao
        self.__data_adicao = data_adicao

    @property
    def id(self):
        return self.__id

    @property
    def titulo(self):
        return self.__titulo
    
    @titulo.setter
    def titulo(self, titulo):
        self.__titulo = titulo
    
    @property
    def artista(self):
        return self.__artista
    
    @artista.setter
    def artista(self, artista):
        self.__artista = artista

    @property
    def duracao(self):
        return self.__duracao
    
    @duracao.setter
    def duracao(self, duracao):
        self.__duracao = duracao

    @property
    def avaliacao(self):
        return self.__avaliacao
    
    @avaliacao.setter
    def avaliacao(self, avaliacao):
        self.__avaliacao = avaliacao

    @property
    def data_adicao(self):
        return self.__data_adicao
    
    @data_adicao.setter
    def data_adicao(self, data_adicao):
        self.__data_adicao = data_adicao

    def __str__(self):
        return f'{self.__id} - {self.__titulo} - {self.__artista} - {self.__duracao} - {self.__avaliacao} - {self.__data_adicao}'
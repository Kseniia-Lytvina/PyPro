from pydantic import BaseModel
from abc import ABC, abstractmethod


class BookModel(BaseModel):
    title: str
    author: str
    year: int


class Publication(ABC):
    @abstractmethod
    def get_info(self) -> str:
        pass


class Book(Publication):
    def __init__(self, data: BookModel):
        self._data = data

    def get_info(self) -> str:
        return f"Книга: {self._data.title}, Автор: {self._data.author}, Рік: {self._data.year}"

    @property
    def author(self):
        return self._data.author

    @property
    def title(self):
        return self._data.title

    def to_dict(self):
        return self._data.dict()


class Magazine(Book):
    def get_info(self) -> str:
        return f"Журнал: {self._data.title}, Автор: {self._data.author}, Рік: {self._data.year}"
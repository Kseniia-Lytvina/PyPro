from typing import List, Generator
from models import Publication, BookModel, Book, Magazine
import functools
import json
import os


def log_addition(func):
    @functools.wraps(func)
    def wrapper(self, item):
        result = func(self, item)
        with open("library.log", "a", encoding="utf-8") as log_file:
            log_file.write(f"Додано: {item.get_info()}\n")
        return result
    return wrapper


def check_exists_before_removal(func):
    @functools.wraps(func)
    def wrapper(self, title):
        for book in self._books:
            if book.title == title:
                return func(self, title)
        raise ValueError(f"Книга '{title}' не знайдена в бібліотеці.")
    return wrapper


class Library:
    def __init__(self):
        self._books: List[Publication] = []

    def __iter__(self):
        return iter(self._books)

    def books_by_author(self, author_name: str) -> Generator[Publication, None, None]:
        return (book for book in self._books if book.author == author_name)

    @log_addition
    def add_book(self, item: Publication):
        self._books.append(item)

    @check_exists_before_removal
    def remove_book(self, title: str):
        removed = [book for book in self._books if book.title == title]
        self._books = [book for book in self._books if book.title != title]
        with open("library.log", "a", encoding="utf-8") as log_file:
            for book in removed:
                log_file.write(f"Видалено: {book.get_info()}\n")

    def show_books(self):
        for book in self._books:
            print(book.get_info())

    def to_list(self):
        return [book.to_dict() for book in self._books]

    def load_from_list(self, items: List[dict]):
        for item in items:
            self.add_book(Book(BookModel(**item)))


class LibraryFileManager:
    def __init__(self, library: Library, filename: str):
        self.library = library
        self.filename = filename

    def __enter__(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                    self.library._books.clear()
                    for item in data:
                        model = BookModel(**item)
                        if "вісник" in model.title.lower() or "журнал" in model.title.lower():
                            self.library.add_book(Magazine(model))
                        else:
                            self.library.add_book(Book(model))
                except json.JSONDecodeError:
                    pass
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            with open(self.filename, "w", encoding="utf-8") as f:
                json.dump(self.library.to_list(), f, ensure_ascii=False, indent=4)
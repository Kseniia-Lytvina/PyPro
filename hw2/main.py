from models import BookModel, Book, Magazine
from library import Library, LibraryFileManager

if __name__ == "__main__":
    lib = Library()

    book1 = Book(BookModel(title="Тарас Бульба", author="Микола Гоголь", year=1835))
    magazine1 = Magazine(BookModel(title="Літературний вісник", author="Микола Гоголь", year=1840))

    lib.add_book(book1)
    lib.add_book(magazine1)

    print("\n Усі публікації:")
    lib.show_books()

    print("\n Книги автора 'Микола Гоголь':")
    for b in lib.books_by_author("Микола Гоголь"):
        print(b.get_info())

    print("\n Видалення книги:")
    if any(book.title == "Тарас Бульба" for book in lib):
        lib.remove_book("Тарас Бульба")
    else:
        print("Книга 'Тарас Бульба' вже була видалена або не знайдена.")

    print("\n Після видалення:")
    lib.show_books()

    with LibraryFileManager(lib, "library.json"):
        print("\n Збережено до файлу.")

    with LibraryFileManager(lib, "library.json"):
        print("\n Завантажено з файлу")

    print("\n Фінальний список:")
    lib.show_books()

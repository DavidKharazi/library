import json
import os
from typing import List, Dict


class Book:
    def __init__(self, title: str, author: str, year: int):
        """Инициализация книги с автоматической генерацией уникального ID."""
        self.id = self.generate_unique_id()
        self.title = title
        self.author = author
        self.year = year
        self.status = "в наличии"

    @staticmethod
    def generate_unique_id() -> int:
        """Генерация уникального идентификатора для книги."""
        return int(os.urandom(4).hex(), 16)



class LibraryManagementSystem:
    def __init__(self, storage_file: str = 'library_books.json'):
        """Инициализация системы управления библиотекой."""
        self.storage_file = storage_file
        self.books: List[Book] = self.load_books()

    def load_books(self) -> List[Book]:
        """Загрузка книг из файла JSON."""
        if not os.path.exists(self.storage_file):
            return []

        try:
            with open(self.storage_file, 'r', encoding='utf-8') as f:
                book_data = json.load(f)
                return [self._dict_to_book(book) for book in book_data]
        except (json.JSONDecodeError, IOError):
            print("Ошибка при чтении файла. Создается новая библиотека.")
            return []

    def _dict_to_book(self, book_dict: Dict) -> Book:
        """Преобразование словаря в объект Book."""
        book = Book(book_dict['title'], book_dict['author'], book_dict['year'])
        book.id = book_dict['id']
        book.status = book_dict['status']
        return book

    def save_books(self):
        """Сохранение книг в файл JSON."""
        try:
            with open(self.storage_file, 'w', encoding='utf-8') as f:
                json.dump([book.__dict__ for book in self.books], f, ensure_ascii=False, indent=2)
        except IOError:
            print("Ошибка при сохранении книг.")

    def add_book(self, title: str, author: str, year: int) -> Book:
        """Добавление новой книги в библиотеку."""
        new_book = Book(title, author, year)
        self.books.append(new_book)
        self.save_books()
        return new_book

    def remove_book(self, book_id: int) -> bool:
        """Удаление книги по ID."""
        initial_length = len(self.books)
        self.books = [book for book in self.books if book.id != book_id]

        if len(self.books) < initial_length:
            self.save_books()
            return True
        return False

    def search_books(self, query: str, search_type: str = 'title') -> List[Book]:
        """Поиск книг по различным критериям."""
        query = query.lower()
        if search_type == 'title':
            return [book for book in self.books if query in book.title.lower()]
        elif search_type == 'author':
            return [book for book in self.books if query in book.author.lower()]
        elif search_type == 'year':
            return [book for book in self.books if str(query) == str(book.year)]
        return []

    def update_book_status(self, book_id: int, new_status: str) -> bool:
        """Обновление статуса книги."""
        if new_status not in ["в наличии", "выдана"]:
            return False

        for book in self.books:
            if book.id == book_id:
                book.status = new_status
                self.save_books()
                return True
        return False

    def display_books(self):
        """Отображение всех книг в библиотеке."""
        if not self.books:
            print("Библиотека пуста.")
            return

        for book in self.books:
            print(f"ID: {book.id}, Название: {book.title}, Автор: {book.author}, "
                  f"Год: {book.year}, Статус: {book.status}")


def main():
    library = LibraryManagementSystem()

    while True:
        print("\n--- Система управления библиотекой ---")
        print("1. Добавить книгу")
        print("2. Удалить книгу")
        print("3. Найти книгу")
        print("4. Показать все книги")
        print("5. Изменить статус книги")
        print("6. Выйти")

        choice = input("Выберите действие: ")

        try:
            if choice == '1':
                title = input("Введите название книги: ")
                author = input("Введите автора книги: ")
                year = int(input("Введите год издания: "))
                book = library.add_book(title, author, year)
                print(f"Книга добавлена. ID книги: {book.id}")

            elif choice == '2':
                book_id = int(input("Введите ID книги для удаления: "))
                if library.remove_book(book_id):
                    print("Книга успешно удалена.")
                else:
                    print("Книга не найдена.")

            elif choice == '3':
                search_type = input("Искать по (title/author/year): ")
                query = input("Введите поисковый запрос: ")
                results = library.search_books(query, search_type)

                if results:
                    print("Найденные книги:")
                    for book in results:
                        print(f"ID: {book.id}, Название: {book.title}, Автор: {book.author}")
                else:
                    print("Книги не найдены.")

            elif choice == '4':
                library.display_books()

            elif choice == '5':
                book_id = int(input("Введите ID книги: "))
                new_status = input("Введите новый статус (в наличии/выдана): ")
                if library.update_book_status(book_id, new_status):
                    print("Статус книги обновлен.")
                else:
                    print("Не удалось обновить статус.")

            elif choice == '6':
                print("Завершение работы...")
                break

            else:
                print("Неверный выбор. Попробуйте снова.")

        except ValueError:
            print("Введены некорректные данные. Попробуйте снова.")
        except Exception as e:
            print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    main()
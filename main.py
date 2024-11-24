import json
import os


class Book:
    def __init__(self, id, title, author, year, status="в наличии"):
        self.id = id
        self.title = title
        self.author = author
        self.year = year
        self.status = status

    def dictonary(self):
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "status": self.status
        }


class Library:
    def __init__(self, filename='library.json'):
        self.filename = filename
        self.books = []
        self.load_from_file()

    def load_from_file(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r', encoding='utf-8') as file:
                data = json.load(file)
                for item in data:
                    self.books.append(Book(**item))

    def save_to_file(self):
        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump([book.dictonary() for book in self.books], file, ensure_ascii=False, indent=4)

    def add_book(self, title, author, year):
        book_id = len(self.books) + 1
        new_book = Book(book_id, title, author, year)
        self.books.append(new_book)
        self.save_to_file()
        print(f'Книга "{title}" добавлена.')

    def remove_book(self, book_id):
        for book in self.books:
            if book.id == book_id:
                self.books.remove(book)
                self.save_to_file()
                print(f'Книга с id {book_id} удалена.')
                return
        print(f'Книга с id {book_id} не найдена.')

    def search_books(self, query):
        results = [book for book in self.books if query.lower() in book.title.lower() or
                   query.lower() in book.author.lower() or
                   str(book.year) == str(query)]
        if results:
            for book in results:
                print(
                    f'id: {book.id}, title: {book.title}, author: {book.author}, year: {book.year}, status: {book.status}')
        else:
            print("Книги не найдены.")

    def display_books(self):
        for book in self.books:
            print(
                f'id: {book.id}, title: {book.title}, author: {book.author}, year: {book.year}, status: {book.status}')

    def update_status(self, book_id, status):
        for book in self.books:
            if book.id == book_id:
                if status in ["в наличии", "выдана"]:
                    book.status = status
                    self.save_to_file()
                    print(f'Статус книги с id {book_id} изменен на "{status}".')
                    return
                else:
                    print('Неверный статус. Поддерживаемые статусы: "в наличии", "выдана".')
                    return
        print(f'Книга с id {book_id} не найдена.')


def main():
    library = Library()

    while True:
        print("\nКоманды:")
        print("1. Добавить книгу")
        print("2. Удалить книгу")
        print("3. Искать книги")
        print("4. Отобразить все книги")
        print("5. Изменить статус книги")
        print("6. Выход")

        choice = input("Выберите команду: ")

        if choice == '1':
            title = input("Введите название книги: ")
            author = input("Введите автора книги: ")
            year = input("Введите год издания: ")
            library.add_book(title, author, year)

        elif choice == '2':
            book_id = int(input("Введите id книги для удаления: "))
            library.remove_book(book_id)

        elif choice == '3':
            query = input("Введите название, автора или год для поиска: ")
            library.search_books(query)

        elif choice == '4':
            library.display_books()

        elif choice == '5':
            book_id = int(input("Введите id книги для изменения статуса: "))
            status = input("Введите новый статус (в наличии/выдана): ")
            library.update_status(book_id, status)

        elif choice == '6':
            print("Выход из программы...")
            break

        else:
            print("Неверный ввод. Пожалуйста, выберите команду снова.")


if __name__ == "__main__":
    main()

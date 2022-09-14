# This is a sample Python script.
import os.path
import sys
import json
import requests

from classes.Books import Book
from classes.Library import Library

reader_id = 1


# the login function will let you access the rest of the functions if the username and email you've entered appear in
# the users' api query result
# status - works
def login():
    username = input("enter username:  ")
    email = input("enter email: ")
    response = requests.get(f"https://jsonplaceholder.typicode.com/users?username={username}&email={email}")
    data = response.json()
    if len(data) == 0:
        print("Login failed")
        return False
    print("You logged in successfully")
    return True


# input - book name, author name, and number of pages
# the program creates a Book object from the input and adds it to the library.
# status - works
def one(lib: Library):
    name: str = input("Enter book name: ")
    author: str = input("Enter author: ")
    pages: int = int(input("Enter number of pages: "))
    try:
        book = Book(author, name, pages)
        lib.add_new_book(book)
        print(f"\n{book} was added")
    except Exception as err:
        print(err)


# input - book name
# the program deletes the book it got as an input value from the library
# status - works
def two(lib: Library):
    book_to_delete: str = input("What book would you like to delete?\nAnswer:\t")
    try:
        lib.delete_book(book_to_delete)
        print(f"book with the title of {book_to_delete.title()} was deleted from the library")
    except Exception as err:
        print(err)
    pass


# input - two book titles
# the program changes the locations of the books on the shelves
def three(lib: Library):
    print("To change the locations of the book, please enter the corresponding titles:")
    title_one: str = input("the title of the first book:  ")
    title_two: str = input("the title of the second book:  ")
    try:
        lib.change_locations(title_one, title_two)
        print("the books' locations swapped")
    except Exception as err:
        print(err)
    pass


# input - reader name
# the program creates a new reader and adds them to the library
# status - works
def four(lib: Library):
    print("Adding a new reader\n")
    reader_name: str = input("new reader name:  ")
    global reader_id
    try:
        lib.register_reader(reader_name, reader_id)
        print(f"{reader_name.title()} was added to readers list")
        reader_id += 1
    except Exception as err:
        print(err)
    pass


# input - reader name
# the program deletes an existing user
# status - works
def five(lib: Library):
    print("Deleting an existing reader\n")
    reader_name: str = input("reader name:  ")
    try:
        is_deleted: bool = lib.delete_reader(reader_name)
        if is_deleted:
            print(f"{reader_name.title()} was deleted from the readers list")
        else:
            print(f"There is no reader with the name {reader_name.title()} in the library")
    except Exception as err:
        print(err)
    pass


# input - author name
# the program will return a list of books, all of which were written by the same author
# status - works
def six(lib: Library):
    print("The program will print all the book written by the author you'll choose")
    author: str = input("Author name:  ")
    books_by_author: [Book] = lib.search_by_author(author)
    try:
        if len(books_by_author) == 0:
            print(f"No books under author {author} were found")
        for book in books_by_author:
            print(book)
    except Exception as err:
        print(err)
    pass


# input - reader name, and book title
# the program will add the book to an existing reader's reading list
# status - works
def seven(lib: Library):
    print("")
    reader_name: str = input("Reader Name: ")
    book_title: str = input("Book title:  ")
    try:
        reader_exist = lib.reader_read_book(reader_name, book_title)
        if reader_exist:
            print(f"Reader {reader_name.title()} read {book_title.title()}")
        else:
            print(f"Reader with the name {reader_name.title()} or book with title of "
                  f"{book_title.title()} doesn't exist")
    except Exception as err:
        print(err)
    pass


# orders all the books according to the number of pages on each shelf
# status - works
def eight(lib: Library):
    try:
        lib.order_books()
        print("Books ordered")
    except Exception as err:
        print(err)
    pass


# input - file name
# creates a file (if it doesn't exist) with all the relevant fields'
# status - works
def nine(lib: Library):
    # saves all the library data in a json file
    json_name = input("Json file name:  ")
    print(json.dumps(lib.to_json(), indent=2))
    print(f"Library saved to JSON file with the name {json_name}")
    with open(os.path.join(sys.path[0], json_name), 'w') as f:
        json.dump(lib.to_json(), f, indent=2)


# input - file name
# loads all the information in the file into the library
# status - works
def ten(lib: Library):
    # loads all the library data from a json object
    json_name = input("Json file name:  ")
    print(f"Library loaded from JSON file with the name {json_name}")
    with open(os.path.join(sys.path[0], json_name), 'r') as f:
        data = json.load(f)
        lib.set_lib(data)


def show_menu():
    options = {1: one,
               2: two,
               3: three,
               4: four,
               5: five,
               6: six,
               7: seven,
               8: eight,
               9: nine,
               10: ten}
    lib = Library()
    menu = '''
    For adding a book - press 1
    For deleting a book - press 2
    for changing books locations - press 3
    for registering a new reader - press 4
    for removing a reader - press 5
    for searching books by author - press 6
    for reading a book by reader - press 7
    for ordering all books - press 8
    for saving all data - press 9
    for loading data - press 10
    for exit - press 11
    '''
    answer = 1
    while 1 <= answer <= 10:

        print(menu)
        answer = int(input("your choice:  "))
        try:
            options[answer](lib)
            print("Done.\n")
        except Exception as err:
            print(f"{err}\nYou didn't press a key between 1 and 11. Try again\n")
        finally:
            print("\nContinue - Any key between 1 and 11\nFinish - 11")
            answer = int(input("your choice:  "))


if __name__ == '__main__':
    is_logged_in = login()
    if is_logged_in:
        show_menu()

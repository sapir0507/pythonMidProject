from classes.Books import Book


def swap(i, j):
    k = i
    i = j
    j = k


# takes a list of dict objects and creates a list of Book objects from it
def obj_from_json(obj_list: [dict]) -> [Book]:
    temp = []
    for item in obj_list:
        temp.append(item.from_json())
    return temp


class Shelf:
    __books: list
    __is_shelf_full: bool

    @property
    def is_shelf_full(self):
        if len(self.books) == 5:
            self._shelf['is shelf full'] = True
        else:
            self._shelf['is shelf full'] = False

        return self._shelf['is shelf full']

    @property
    def books(self):
        return self._shelf['books']

    def __init__(self, book: None | Book | list | dict = None):
        self._shelf = {
            "is shelf full": False,
            "books": []
        }
        if isinstance(book, Book):
            self.add_book(book)
        elif isinstance(book, list):
            for b in book:
                if isinstance(b, Book):
                    self.add_book(book)
                elif isinstance(b, dict):
                    try:
                        self.add_book(Book().from_json(b))
                    except Exception as e:
                        print(e)
                    finally:
                        pass
        elif isinstance(book, dict):
            self._shelf['is shelf full'] = book['shelve']['is shelf full']

    # returns the book at place index inside a bookshelf
    def __getitem__(self, index):
        return self._shelf['books'][index]

    # returns the number of books a bookshelf contains
    def __len__(self):
        return len(self._shelf['books'])

    # checks to see if the bookshelf is empty
    def __bool__(self):
        return len(self._shelf['books']) != 0

    # inserts a value at the place key inside the list
    def __setitem__(self, key, value):
        self._shelf['books'].insert(key, value)

    # checks to see if a book Object is inside the bookshelf, or if a book with a specific title exists in the
    # bookshelf.
    def __contains__(self, item: Book | str):
        for book in self.books:
            if isinstance(item, str) and book.title.title() == item.title():
                return True
            elif isinstance(item, Book) and book.title.title() == item.title.title():
                return True
        return False

    # compares two bookshelves to see if they have the same books in the same order.
    def __cmp__(self, other):
        if isinstance(other, Shelf):
            for i, book in enumerate(self.books):
                if book != other[i]:
                    return False
            return True
        return False

    # returns a book in the index specified
    def pop(self, index):
        return self.books.pop(index)

    # adds a book to the shelf
    def add_book(self, book):
        try:
            if isinstance(book, Book) and not self.is_shelf_full:
                self.books.append(book)
            elif self.is_shelf_full:
                print(f"book {book.title} was not added to the shelf because it's full")
            else:
                print("object is not a book")
        except Exception as err:
            print(err)

    # swaps the books with the following indexes: index1, index2
    def replace_books(self, index1, index2):
        if index1 > index2:
            swap(index1, index2)

        if index1 < 0:
            print(f"book {index1} doesn't exist")
            return
        if len(self.books) < index2:
            print(f"book {index2} doesn't exist")
            return

        a = self.books[index1]
        self.books[index1] = self.books[index2]
        self.books[index2] = a

    # orders all the books in the shelf according to the number of pages they have
    def order_books(self):
        self.books.sort(key=lambda x: x.num_of_pages)

    # checks if a book with the title book_title exists in this shelf
    def contain_book(self, book_title: str):
        return self.__contains__(book_title)

    # inserts a book Object to the Shelf
    def insert(self, index, book: Book):
        self.books.insert(index, book)

    # returns a dict representation of the Shelf
    def to_json(self) -> dict:
        dict_list = []
        for book in self.books:
            dict_list.append(book.to_json())
        return {
            "is shelf full": self.is_shelf_full,
            "books": dict_list
        }

    # creates a Shelf object from a dict object
    @classmethod
    def from_json(cls, json: dict):
        return cls(json['books'])






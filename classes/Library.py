from classes.Books import Book
from classes.Shelfs import Shelf
from classes.Reader import Reader


def obj_to_json(obj_list: [Shelf | list | Reader]) -> [dict]:
    temp = []
    try:
        for item in obj_list:
            if isinstance(item, Shelf):
                temp.append(item.to_json())
            elif isinstance(item, dict) and isinstance(item['reader'], Reader):
                temp.append({
                    'reader': item['reader'].to_json(),
                    'reader_name': item['reader_name']
                })

    except Exception as e:
        print(e)
    finally:
        return temp


def shelf_class_from_json(obj_list: [dict]) -> [Shelf]:
    temp = Shelf(obj_list['books'])
    return temp


def reader_class_from_json(obj_list: [dict]) -> [Reader]:
    temp = []
    for item in obj_list:
        temp.append(item.to_json())
    return temp


class Library:
    __readers: list
    __shelves: list

    @property
    def shelves(self):
        return self._lib['shelves']

    @property
    def readers(self):
        return self._lib['readers']

    @shelves.setter
    def shelves(self, new_shelves: [Shelf]):
        self.shelves.clear()
        self.shelves.extend(new_shelves)

    @readers.setter
    def readers(self, readers: [{str, Reader}]):
        self.readers.clear()
        self.readers.extend(readers)

    def __init__(self, shelf: list | dict | None = None,
                 reader: list | dict | None = None):
        self._lib = {'shelves': [], 'readers': []}
        if isinstance(shelf, dict):
            try:
                s = Shelf().from_json(shelf)
                self._lib['shelves'].append(s)
                pass
            except Exception as e:
                print(e)
            finally:
                pass
        elif isinstance(shelf, list):
            for i in range(0, 3):
                item = shelf[i]
                if isinstance(item, Shelf):
                    self._lib['shelves'].append(item)
                elif isinstance(item, dict):
                    try:
                        s = Shelf().from_json(item)
                        self._lib['shelves'].append(s)
                        pass
                    except Exception as e:
                        print(e)
                    finally:
                        pass
                else:
                    self._lib['shelves'].append(Shelf())
        else:
            self._lib['shelves'] = [Shelf(), Shelf(), Shelf()]
        if isinstance(reader, dict):
            try:
                r = Reader().from_json(reader)
                self._lib['reader'].append(r)
            except Exception as e:
                print(e)
            finally:
                pass
        elif isinstance(reader, list):
            for item in reader:
                if isinstance(item, dict):
                    try:
                        if isinstance(item['reader_name'], str) and isinstance(item['reader'], Reader):
                            self._lib['readers'].append(item)
                        if isinstance(item['reader_name'], str) and isinstance(item['reader'], dict):
                            try:
                                r1 = Reader().from_json(item['reader'])
                                item['reader'] = r1
                            except Exception as e:
                                print(e)
                            finally:
                                self._lib['readers'].append(item)
                    except Exception as e:
                        print(f"Library readers doesn't have reader name or Reader class object\n{e}")

        elif isinstance(reader, dict):
            try:
                r = {
                    'reader_name': reader['reader_name'],
                    'reader': Reader().from_json(reader['reader'])
                }
                self._lib['reader'].append(r)
            except Exception as e:
                print(e)
            finally:
                pass

    # checks to see if all the bookshelves are full
    def is_there_a_place_for_new_book(self):
        for shelve in self.shelves:
            if not shelve.is_shelf_full:
                return True
        return False

    # inserts a book in the first empty bookshelf
    def add_new_book(self, book: Book):
        if not self.is_there_a_place_for_new_book():
            print("There's no more place to store books inside the library")
        else:
            for shelve in self.shelves:
                if not shelve.is_shelf_full:
                    if isinstance(shelve, Shelf):
                        shelve.add_book(book)
                    else:
                        print(shelve)
                    return

    # deletes book with the title of book_title from the bookshelves if exists
    def delete_book(self, book_title: str):
        for shelf_index, shelf in enumerate(self.shelves):
            for book_index, book in enumerate(shelf):
                if book_title.title() == book.title.title():
                    return shelf.pop(book_index)

    # changes the location of two books inside the library with the titles: book_title1, book_title2 if they exist.
    def change_locations(self, book_title1: str, book_title2: str):
        book_row_1 = None
        book_row_2 = None
        book_col_1 = None
        book_col_2 = None
        for i, bookshelf in enumerate(self.shelves):
            if bookshelf.contain_book(book_title1) and bookshelf.contain_book(book_title2):
                self.change_locations_on_the_same_shelf(i, book_title1, book_title2)
                break
            else:
                if bookshelf.contain_book(book_title1) or bookshelf.contain_book(book_title2):
                    book_row_2 = book_row_1
                    book_row_1 = i
                    for j, book in enumerate(bookshelf):
                        if book.title.title() == book_title1.title() or book.title.title() == book_title2.title():
                            book_col_2 = book_col_1
                            book_col_1 = j
                            break
        if isinstance(book_row_1, int) and isinstance(book_row_2, int):
            temp = self.shelves[book_row_1].pop(book_col_1)
            self.shelves[book_row_1].insert(book_col_1, self.shelves[book_row_2].pop(book_col_2))
            self.shelves[book_row_2].insert(book_col_2, temp)

    # change the location of two books with the titles of: book1_name, book2_name in a specific shelf: shelf_number
    def change_locations_on_the_same_shelf(self, shelf_number, book1_name, book2_name):
        book1_index = -1
        book2_index = -1
        try:
            for index, book in enumerate(self.shelves[shelf_number]):
                if book.title == book1_name.title():
                    book1_index = index
                elif book.title == book2_name.title():
                    book2_index = index

            if 0 <= book1_index <= book2_index <= 5:
                self.shelves[shelf_number].replace_books(book1_index, book2_index)
        except Exception as err:
            print(err)

    # orders each shelf in the library so that its books are placed according to the number of pages they have
    def order_books(self):
        for shelf in self.shelves:
            shelf.order_books()

    # returns a list of all the books written by the same author: author.
    def search_by_author(self, author: str):
        book_list_by_author = []
        for shelf in self.shelves:
            for book in shelf.books:
                if book.author.title() == author.title():
                    book_list_by_author.append(book)

        return book_list_by_author

    # creates a new reader with the name of 'reader_name' and a corresponding id.
    def register_reader(self, reader_name: str, reader_id: int):
        self.readers.append({
            'reader': Reader(reader_id),
            'reader_name': reader_name
        })

    # deletes a reader with the name reader_name from the library
    def delete_reader(self, reader_name):
        for reader in self.readers:
            if reader['reader_name'].title() == reader_name.title():
                self.readers.remove(reader)
                return True
        return False

    # makes a reader with the name 'reader_name' read a book with the name of 'book_title' if both exist.
    def reader_read_book(self, reader_name, book_title):
        for reader in self.readers:
            if reader['reader_name'].title() == reader_name.title():
                for item in self.shelves:
                    if item.contain_book(book_title):
                        reader['reader'].read_book(book_title)
                        return True
                return False
        return False

    # cast a library object into a dict object
    def to_json(self) -> dict:
        shelves = obj_to_json(self.shelves)
        if isinstance(self.readers, list):
            readers = obj_to_json(self.readers)
            return {
                'shelves': shelves,
                'readers': readers
            }
        else:
            return {
                'shelves': shelves,
                'readers': []
            }

    # cast a dict object into a library object and sets this library to contain the same readers and shelves as the
    # object
    def set_lib(self, json: dict):
        new_lib = Library().from_json(json)
        self._lib = {
            'readers': new_lib.readers,
            'shelves': new_lib.shelves
        }

    # casting - takes a dict object and returns a class Library object
    @classmethod
    def from_json(cls, json: dict):
        return cls(json['shelves'], json['readers'])

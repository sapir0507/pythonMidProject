import datetime


class Reader:
    @property
    def identity(self):
        return self._reader['id']

    @property
    def books(self):
        return self._reader['books']

    @identity.setter
    def identity(self, identifier):
        self._reader['id'] = identifier

    @books.setter
    def books(self, books):
        self.books.clear()
        for book in books:
            self.read_book(book)

    def __init__(self, reader_id: int = 0, readers: None | list = None):
        self._reader = {
            "id": reader_id,
            "books": []
        }
        if isinstance(readers, list) and len(readers) > 0:
            for reader in readers:
                try:
                    if isinstance(reader, dict) and isinstance(reader['book title'], str) and isinstance(reader['date'],
                                                                                                         str):
                        self._reader['books'].append(reader)
                except Exception as e:
                    print(e)

    # reads an existing book and adds it to a reader's list of 'books read'.
    def read_book(self, book_title):
        self.books.append({
            "book title": book_title,
            "date": datetime.datetime.now().__str__()
        })

    # returns a list of all the books a reader had read
    def get_books(self):
        return self.books

    # returns the id of the reader
    def get_id(self):
        return self.identity

    # cast the Reader class into a simple dict object
    def to_json(self) -> dict:
        return self._reader

    # returns the number of books a reader had read
    def __len__(self):
        return len(self.books)

    # returns a newly created class from a dict object
    @classmethod
    def from_json(cls, json: dict):
        return cls(json['id'], json['books'])

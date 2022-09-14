class Book:
    _author: str
    _title: str
    _num_of_pages: int

    @property
    def book(self):
        return self._book

    @property
    def author(self):
        return self._book['author']

    @author.setter
    def author(self, author):
        if isinstance(author, str):
            self._book['author'] = author

    @property
    def title(self):
        return self._book['title']

    @title.setter
    def title(self, title1):
        if isinstance(title1, str):
            self._book['title'] = title1

    @property
    def num_of_pages(self):
        return self._book['num of pages']

    @num_of_pages.setter
    def num_of_pages(self, num_of_pages):
        if isinstance(num_of_pages, int) and num_of_pages > 0:
            self._book['num of pages'] = num_of_pages

    def __init__(self, author1='', title1='', num_of_pages1=0):
        self._book = {
            "author": author1,
            "title": title1,
            "num of pages": num_of_pages1
        }

    # compares between two book objects and checks if they have the same values
    # if so, returns true, else returns false
    def __cmp__(self, other):
        if isinstance(other, Book) and other.title == self.title and other.author == self.author \
                and other.num_of_pages == self.num_of_pages:
            return True
        else:
            return False

    # returns a string interpretation of the class
    def __str__(self):
        book = self._book
        return f"Book with the title of '{book['title'].title()}', was written by '{book['author'].title()}' and has " \
               f"{book['num of pages']} pages "

    # returns a dict object of the Book object (casting)
    def to_json(self) -> dict:
        return self.book

    # takes a dict object and creates a book object
    @classmethod
    def from_json(cls, json: dict):
        return cls(json['author'], json['title'], json['num of pages'])


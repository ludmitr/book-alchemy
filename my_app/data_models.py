from my_app import db

class Author(db.Model):
    __tablename__ = 'authors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    birth_date = db.Column(db.Date, nullable=True)
    date_of_death = db.Column(db.Date, nullable=True)

    # Define a one-to-many relationship with Book model
    books = db.relationship('Book', backref='author', lazy=True)

    def __repr__(self):
        return f"<Author(id={self.id}, name='{self.name}', " \
               f"birth_date={self.birth_date}, date_of_death={self.date_of_death})>"

    def __str__(self):
        return f"Author: {self.name}, ID: {self.id}"


class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String(20), nullable=False, unique=True)
    title = db.Column(db.String(200), nullable=False)
    publication_year = db.Column(db.Integer, nullable=False)
    cover = db.Column(db.String(200), nullable=True)

    # foreign key
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'),
                          nullable=False)

    def __repr__(self):
        return f"<Book(id={self.id}, isbn='{self.isbn}', title='{self.title}', " \
               f"publication_year={self.publication_year}, author_id={self.author_id})>"

    def __str__(self):
        return f"Book: {self.title}, ISBN: {self.isbn}, Author ID: {self.author_id}"


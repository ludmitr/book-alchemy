from my_app.data_models import Author, Book
from datetime import datetime
from data_managers.books_api_data_handler import get_book_cover
from sqlalchemy import func
import config
import shutil


def get_all_authors(session):
    return session.query(Author).all()

def add_author_to_db(session, name: str, birth_date: str, death_date: str):
    # Convert birthdate_str and deathdate_str to datetime objects
    birth_date = datetime.strptime(birth_date, '%Y-%m-%d') if birth_date else None
    death_date = datetime.strptime(death_date, '%Y-%m-%d') if death_date else None

    # Data validation
    if birth_date and death_date and death_date < birth_date:
        raise ValueError("Deathdate cannot be before birthdate")
    if death_date and not birth_date:
        raise ValueError("Birthdate is required if deathdate is provided")
    same_name_in_db = session.query(Author).filter(Author.name == name).first()
    if same_name_in_db:
        raise ValueError("Author with that name already exist")

    # Create a new author and add it to the database
    new_author = Author(name=name, birth_date=birth_date, date_of_death=death_date)
    session.add(new_author)
    session.commit()


def add_book_to_db(session, title, author_id, isbn, publication_year):
    # Data validation
    if not title or not author_id or not publication_year or not isbn:
        raise ValueError("All fields are required")
    if not publication_year.isnumeric():
        raise ValueError("Invalid publication year")

    existing_book_with_same_title = session.query(Book).filter(Book.title == title).first()
    if existing_book_with_same_title is not None:
        raise ValueError("A book with this title already exists")

    existing_book_with_same_isbn = session.query(Book).filter(Book.isbn == isbn).first()
    if existing_book_with_same_isbn is not None:
        raise ValueError("A book with this isbn already exists")

    # Create a new book and add it to the database
    new_book = Book(isbn=isbn, title=title, publication_year=int(publication_year),
                    author_id=author_id, cover=get_book_cover(isbn))
    session.add(new_book)
    session.commit()


def get_all_books_from_db(session):
    return session.query(Book).join(Book.author).all()

def get_books_sorted_by(session, sorted_by):
    sort_map = {"author": Author.name,
                "title": Book.title,
                "publication_year": Book.publication_year}
    sorted_books = session.query(Book).join(Book.author).order_by(sort_map[sorted_by]).all()
    return sorted_books


def get_books_by_search_term(session, search_text: str):
    search_result = session.query(Book).join(Book.author)\
        .filter(func.lower(Book.title).contains(search_text.lower())).all()
    return search_result


def delete_book_by_id(session, book_id: int):
    """Delete book by book id. If deleted  - return book title, if not - returns None"""
    book_to_delete = session.query(Book).filter(Book.id == book_id).first()
    if book_to_delete is not None:
        session.delete(book_to_delete)
        session.commit()
        return book_to_delete.title

    return None


def restore_db_to_default():
    shutil.copy(config.get_absolute_path_default_db(), config.get_absolute_path_current_db())

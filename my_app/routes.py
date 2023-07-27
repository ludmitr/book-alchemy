from flask import Flask, request, url_for, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from my_app import app, db
from my_app.data_models import Author, Book
from datetime import datetime
from sqlalchemy.exc import IntegrityError


@app.route('/')
def home():
    all_books = db.session.query(Book).join(Book.author)
    return render_template('home.html', books=all_books)

@app.route('/add_author', methods=['GET','POST'])
def add_author():
    if request.method == 'GET':
        return render_template('add_author.html')
    elif request.method == 'POST':
        name = request.form.get('name')
        birthdate_str = request.form.get('birthdate')
        deathdate_str = request.form.get('deathdate')

        # Convert birthdate_str and deathdate_str to datetime objects
        birthdate = datetime.strptime(birthdate_str,
                                      '%Y-%m-%d') if birthdate_str else None
        deathdate = datetime.strptime(deathdate_str,
                                      '%Y-%m-%d') if deathdate_str else None

        # Data validation
        if birthdate and deathdate and deathdate < birthdate:
            return jsonify({"error": "Deathdate cannot be before birthdate"}), 400
        if deathdate and not birthdate:
            return jsonify({"error": "Birthdate is required if deathdate is provided"}), 400

        # Create a new author and add it to the database
        new_author = Author(name=name, birth_date=birthdate, date_of_death=deathdate)
        db.session.add(new_author)
        db.session.commit()

        # Return a success message
        return jsonify({"message": "Author added successfully"}), 201

@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    """Handling GET and POST request
        GET - render a page with add book FORM.
        POST - Getting arguments and adding the book to the db.
    """
    try:
        if request.method == 'GET':
            all_authors = db.session.query(Author).all()
            return render_template('add_book.html', authors=all_authors)

        elif request.method == 'POST':
            # getting arguments from add book form
            title = request.form.get('title')
            author_id = request.form.get('author')
            isbn = request.form.get('isbn')
            publication_year = request.form.get('publication_year')  # Correct the form field name

            # Data validation
            if not title or not author_id or not publication_year or not isbn:
                return jsonify({"error": "All fields are required"}), 400
            if not publication_year.isnumeric():
                return jsonify({"error": "Invalid publication year"}), 400

            # Create a new book and add it to the database
            new_book = Book(isbn=isbn, title=title, publication_year=int(publication_year), author_id=author_id)
            db.session.add(new_book)
            db.session.commit()

            # Return a success message
            return jsonify({"message": "Book added successfully"}), 201

    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Book with this ISBN already exists"}), 400

    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred - {e}"}), 500



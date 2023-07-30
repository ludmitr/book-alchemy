from flask import request, url_for, render_template, jsonify
from data_managers import db_manager
from my_app import app, db


@app.route('/')
def home():
    sorted_by = request.args.get('sorted_by')
    search_criteria = request.args.get('search')

    allowed_sorts = ["author", "title", "publication_year"]

    # getting data according to request
    if sorted_by in allowed_sorts:
        all_books = db_manager.get_books_sorted_by(db.session, sorted_by)
    elif search_criteria:
        all_books = db_manager.get_books_by_search_term(db.session, search_criteria)
    else:
        all_books = db_manager.get_all_books_from_db(db.session)

    if search_criteria:
        message = f"Search results for: {search_criteria} " if all_books else f'No matches for: {search_criteria} '
        return render_template('home.html', books=all_books, message=message)

    return render_template('home.html', books=all_books)


@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    """
    Handle GET and POST requests for adding an author.

    GET: Render an add_author HTML page.
    POST: Validate the request data and add an author to the database.
    Return a success message upon successful addition or an error message otherwise.
    """
    if request.method == 'GET':
        return render_template('add_author.html')
    elif request.method == 'POST':
        # get data from request
        name = request.form.get('name')
        birth_date = request.form.get('birthdate')
        death_date = request.form.get('deathdate')
        try:
            db_manager.add_author_to_db(db.session, name, birth_date, death_date)
            return jsonify({"message": "Author added successfully"}), 201
        except ValueError as ve:
            return jsonify({"error": str(ve)}), 400
        except Exception as e:
            return jsonify({"error": "An error occurred while adding the author: " + str(e)}), 500


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    """
    Handle GET and POST requests for adding a book.

    GET: Render an add_book HTML page with all authors.
    POST: Validate the request data and add a book to the database.
    Return a success message upon successful addition or an error message otherwise.
    """
    try:
        if request.method == 'GET':
            all_authors = db_manager.get_all_authors(db.session)
            return render_template('add_book.html', authors=all_authors)

        elif request.method == 'POST':
            # getting arguments from request
            title = request.form.get('title')
            author_id = request.form.get('author')
            isbn = request.form.get('isbn')
            publication_year = request.form.get('publication_year')

            db_manager.add_book_to_db(db.session, title, author_id, isbn, publication_year)
            return jsonify({"message": "Book added successfully"}), 201
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": "An error occurred while adding the book: " + str(e)}), 500

@app.route('/book/<int:book_id>/delete', methods=['POST'])
def delete_book(book_id):
    """Delete book by passed id"""
    book_name = db_manager.delete_book_by_id(db.session, book_id)
    all_books = db_manager.get_all_books_from_db(db.session)

    message_for_user = f"'{book_name}' - deleted successfully." if book_name else 'An error occurred, the book was not deleted.'
    return render_template('home.html', books=all_books, message=message_for_user)


@app.route('/book/restore', methods=['POST'])
def restore_db():
    db.session.remove()  # This will close the session
    db.engine.dispose()  # This will close the engine
    db_manager.restore_db_to_default()
    message_for_user = 'Database RESTORED!'
    all_books = db_manager.get_all_books_from_db(db.session)
    return render_template('home.html', books=all_books, message=message_for_user)
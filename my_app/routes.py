from flask import Flask, request, url_for, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from my_app import app, db
from my_app.data_models import Author, Book
from datetime import datetime


@app.route('/')
def home():
    return 'HeLLO BLIAT'

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
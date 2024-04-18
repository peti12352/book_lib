# book_app.py

# Import necessary libraries
from flask import Flask, render_template, abort, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate
import os

# Initialize Flask app
app = Flask(__name__)
# Get the absolute path to the instance folder
instance_path = os.path.join(app.root_path, 'instance')

# Configure SQLAlchemy to use the SQLite database file in the instance folder
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(instance_path, 'database.db')

# Suppress deprecation warning
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Define models for books and rentals


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    available = db.Column(db.Boolean, nullable=False, default=True)


class Rental(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book_id'), nullable=False)
    return_date = db.Column(db.DateTime, nullable=True)


# Load book IDs from CSV
def load_books():
    with open('api/books.csv', 'r') as file:
        books = [line.strip() for line in file.readlines()[1:]]
    return books


books = load_books()


@app.route('/book/<int:book_id>', methods=['POST'])
def rent_book(book_id):

    if Book.query.get(book_id).available:
        rental = Rental(book_id=book_id)
        db.session.add(rental)
        Book.query.get(book_id).available = False
        db.session.commit()
        flash('You have successfully rented the book!', 'success')

    else:
        flash('The book is not available for rent.', 'error')
    return redirect(url_for('book', book_id=book_id))


@app.route('/book/<int:book_id>', methods=['POST'])
def return_book(book_id):
    book = Book.query.get_or_404(book_id)
    rental = Rental.query.filter_by(book_id=book_id, return_date=None).first()
    if rental:
        rental.return_date = datetime.now()
        book.available = True
        db.session.commit()
        flash('You have successfully returned the book!', 'success')
    else:
        flash('You have not rented this book.', 'error')
    return redirect(url_for('book', book_id=book_id))


# Home route
@app.route('/')
def index():
    return render_template('index.html', books=books)


# Book route
@app.route('/book/<int:book_id>')
def book(book_id):
    if str(book_id) in books:
        return render_template('book.html', book_id=book_id)
    else:
        abort(404)


# Error handling
@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html'), 404


if __name__ == '__main__':
    app.run(debug=True)

# book_app.py

from flask import Flask, render_template, abort
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

# Define models for users, books, and rentals


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    rentals = db.relationship('Rental', backref='user', lazy=True)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    author = db.Column(db.String(128), nullable=False)
    isbn = db.Column(db.String(20), nullable=False, unique=True)
    available = db.Column(db.Boolean, nullable=False, default=True)
    rentals = db.relationship('Rental', backref='book', lazy=True)


class Rental(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    rental_date = db.Column(db.TIMESTAMP, nullable=False,
                            server_default=db.func.current_timestamp())
    return_date = db.Column(db.TIMESTAMP)


app = Flask(__name__)

# Load book IDs from CSV


def load_books():
    with open('books.csv', 'r') as file:
        books = [line.strip() for line in file.readlines()[1:]]
    return books


books = load_books()

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

# Rental route


@app.route('/book/<int:book_id>/rental', methods=['POST'])
def rental(book_id):
    # Implement rental logic here
    return f"Rental option selected for Book {book_id}"

# Return route


@app.route('/book/<int:book_id>/return', methods=['POST'])
def return_book(book_id):
    # Implement return logic here
    return f"Return option selected for Book {book_id}"

# Error handling


@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html'), 404


if __name__ == '__main__':
    app.run(debug=True)

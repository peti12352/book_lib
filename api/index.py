# book_app.py

from flask import Flask, render_template, abort

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

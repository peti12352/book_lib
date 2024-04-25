from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Book, Note, User, Rent
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        book_name = request.form.get('book_name')
        author = request.form.get('author')
        genre = request.form.get('genre')
        new_book = Book(book_name=book_name, author=author,
                        genre=genre, isAvailable=True)
        db.session.add(new_book)
        db.session.commit()
        flash('Book added successfully', category='success')
    return render_template("home.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    # this function expects a JSON from the INDEX.js file
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})


@views.route('/rent-book', methods=['POST'])
def rent_book():
    book = json.loads(request.data)
    bookId = book['bookId']
    book = Book.query.get(bookId)
    if book:
        if book.isAvailable:
            book.isAvailable = False
            new_rent = Rent(user_id=current_user.id, book_id=bookId)
            db.session.add(new_rent)
            db.session.commit()

    return jsonify({})


@views.route('/return-book', methods=['POST'])
def return_book():
    book = json.loads(request.data)
    bookId = book['bookId']
    rent = Rent.query.filter_by(book_id=bookId).first()
    if rent:
        db.session.delete(rent)
        book = Book.query.get(bookId)
        book.isAvailable = True
        db.session.commit()

    return jsonify({})

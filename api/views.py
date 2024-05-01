from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Book, Rent
from . import db
views = Blueprint('views', __name__)


@views.route('/', methods=['GET'])
@login_required
def home():
    # Get all books which are rented by the current user
    rents = Rent.query.filter_by(user_id=current_user.id).all()

    if not rents:
        flash('No books found!', category='error')
        return render_template("home.html", user=current_user, books=[])

    return render_template("home.html", user=current_user, books=rents)

# Route for displaying each book's page based on its ID
# load books

# book page with rent/return button (which is registered in the db) for each book based on its ID


@views.route('/<int:book_id>', methods=['GET', 'POST'])
@login_required
def book_detail(book_id):
    # Get the book by ID
    book = Book.query.get(book_id)

    if request.method == 'POST':  # determined by the form action in book_page.html

        if book.isRented and request.form.get('action') == 'return':
            # Return the book
            rent_record = Rent.query.filter_by(
                user_id=current_user.id, book_id=book.id).first()
            if rent_record:
                # Delete the Rent record and update the book's rented status
                db.session.delete(rent_record)
                book.isRented = False
                db.session.commit()
                flash('Book returned successfully!', category='success')
            else:
                flash('Book is not currently rented by you.', category='error')

        elif not book.isRented and request.form.get('action') == 'rent':
            # Rent the book
            rent = Rent(user_id=current_user.id, book_id=book.id)
            db.session.add(rent)
            book.isRented = True
            db.session.commit()
            flash('Book rented successfully!', category='success')

        else:
            flash('Invalid action.', category='error')

        # Redirect back to the book_page.html
        return redirect(url_for('views.book_detail', book_id=book.id))

    rent_record = Rent.query.filter_by(
        user_id=current_user.id, book_id=book.id).first()
    is_rented_by_user = rent_record is not None

    return render_template('book_page.html', user=current_user, book=book,
                           is_rented_by_user=is_rented_by_user)

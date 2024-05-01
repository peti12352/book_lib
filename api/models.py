from . import db
from flask_login import UserMixin

from sqlalchemy.sql import func


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))

    rents = db.relationship('Rent', back_populates='user',
                            cascade='all, delete-orphan')

    def __repr__(self):
        return f'<User {self.first_name}>'


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    isRented = db.Column(db.Boolean, default=False)

    # Relationship with Rent
    rents = db.relationship('Rent', back_populates='book',
                            cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Book {self.id}>'


class Rent(db.Model):
    # Relationships
    book = db.relationship('Book', back_populates='rents')
    user = db.relationship('User', back_populates='rents')

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    date = db.Column(db.DateTime(timezone=True), default=func.now())

    def __repr__(self):
        return f'<Rent {self.id}>'

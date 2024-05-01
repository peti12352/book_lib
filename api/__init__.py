from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
import pandas as pd

db = SQLAlchemy()
DB_NAME = "database.db"


def load_books_from_csv(csv_file):
    # Load CSV data
    books_df = pd.read_csv(csv_file)

    # import book
    from .models import Book

    # Insert data into the database
    for index, row in books_df.iterrows():
        book = Book(id=row['id'], title=row['title'], isRented=False)

        db.session.add(book)
        db.session.commit()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secretkey'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    # Initialize the database
    db.init_app(app)

    # Import blueprints
    from .views import views
    from .auth import auth

    # Register blueprints
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    # Import models
    from .models import User

    # Initialize the database
    create_database(app)

    # Configure login manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # This command can be run using flask load_books
    @app.cli.command('load_books')
    def load_books():
        load_books_from_csv('books.csv')

    return app


def create_database(app):
    # Only create the database if it doesn't exist
    # There should be a row for each book in the database

    if not path.exists(f'{DB_NAME}'):
        with app.app_context():
            db.create_all()
            print('Database created!')

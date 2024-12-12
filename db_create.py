from config import SQLALCHEMY_DATABASE_URI
from app import db
import os.path
from app import app, db  # Import your app and db instances


if __name__ == '__main__':
    with app.app_context():  # Create an application context
        db.create_all()



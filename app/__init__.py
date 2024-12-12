from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config.from_object('config')
app.config['SECRET_KEY']='lInkinPaRkisGoATband'

Bootstrap(app)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
migrate = Migrate(app, db)

csrf = CSRFProtect(app)

from app import views, models

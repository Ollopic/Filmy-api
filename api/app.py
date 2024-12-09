from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@db:5432/filmy'
db = SQLAlchemy(app)

migrate = Migrate(app, db)

# Importation des modèles
from .models import Person, Film, CreditsFilm, User, CollectionItem

@app.route('/')
def hello():
    return 'Hello, World!'
from flask import Flask

app = Flask(__name__)


# Importation des modèles
from .models import Person, Film, CreditsFilm, User, CollectionItem

@app.route('/')
def hello():
    return 'Hello, World!'
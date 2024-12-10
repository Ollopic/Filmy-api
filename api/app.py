from flask import Flask

app = Flask(__name__)


# Importation des modèles
from .models import CollectionItem, CreditsFilm, Film, Person, User


@app.route("/")
def hello():
    return "Hello, World!"

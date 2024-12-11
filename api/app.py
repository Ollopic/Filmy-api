from flask import Flask

app = Flask(__name__)

# Importation des modèles
from .models import *
from .routes import *

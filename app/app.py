from flask import Flask

app = Flask(__name__)

# Importation des routes
from app.routes import *

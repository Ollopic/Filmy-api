from flask import Flask

app = Flask(__name__)

# Importation des routes
from app.routes.movies_routes import *
from app.routes.users_routes import *
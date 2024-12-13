from flask import Flask
from flask_jwt_extended import JWTManager

from app.config import jwtSecretKeyConfig

app = Flask(__name__)

# Importation des routes
from app.routes import *

app.config["JWT_SECRET_KEY"] = jwtSecretKeyConfig
jwt = JWTManager(app)

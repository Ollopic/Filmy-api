from flask import Flask
from flask_jwt_extended import JWTManager
from datetime import timedelta

from app.config import jwtSecretKeyConfig, jwtAccessTokenExpiresConfig, jwtRefreshTokenExpiresConfig

app = Flask(__name__)

# Importation des routes
from app.routes import *

app.config["JWT_SECRET_KEY"] = jwtSecretKeyConfig
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(jwtAccessTokenExpiresConfig)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(jwtRefreshTokenExpiresConfig)
jwt = JWTManager(app)

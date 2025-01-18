from datetime import timedelta

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from app.config import (
    jwtAccessTokenExpiresConfig,
    jwtSecretKeyConfig,
)

app = Flask(__name__)

# Import routes
from app.routes import *  # noqa: E402, F403

app.config["JWT_SECRET_KEY"] = jwtSecretKeyConfig
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=jwtAccessTokenExpiresConfig)
jwt = JWTManager(app)

CORS(app, resources={r"/*": {"origins": "http://localhost:8080"}})

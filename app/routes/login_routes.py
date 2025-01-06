import bcrypt
from flask import request
from flask_jwt_extended import create_access_token

from app.app import app
from app.db.models import User


@app.route("/token", methods=["POST"])
def create_token():
    data = request.json
    user = User.query.filter_by(mail=data["mail"]).first()

    if not user or not bcrypt.checkpw(data["password"].encode("utf-8"), user.password.encode("utf-8")):
        return {"error": "Mail ou mot de passe incorrect"}, 401

    return {
        "message": "User logged in successfully",
        "token": create_access_token(identity=str(user.id)),
    }, 200

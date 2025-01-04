from datetime import datetime

import bcrypt
from flask import request
from flask_jwt_extended import create_access_token, create_refresh_token

from app.app import app
from app.db.models import User


@app.route("/token", methods=["POST"])
def create_token():
    data = request.json
    user = User.query.filter_by(mail=data["mail"]).first()

    if not user:
        return {"error": "User not found"}, 404

    if bcrypt.checkpw(data["password"].encode("utf-8"), user.password.encode("utf-8")):
        return {
            "message": "User logged in successfully",
            "token": create_access_token(identity=str(user.id)),
            "token_expires_at": round(datetime.timestamp(datetime.now() + app.config["JWT_ACCESS_TOKEN_EXPIRES"])),
        }, 200

    return {"error": "Invalid password"}, 401

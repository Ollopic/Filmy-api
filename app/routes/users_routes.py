import bcrypt
from flask import request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required

from app.app import app
from app.db.database import db
from app.db.models import CollectionItem, User
from app.util import hash_password


@app.route("/user/<int:id>", methods=["GET"])
@jwt_required()
def get_user(id):
    user = db.session.query(User).get(id)
    user_request = db.session.query(User).get(get_jwt_identity())

    if user_request.id != user.id and not user_request.is_admin:
        return {"error": "Unauthorized"}, 401

    if user is None:
        return {"error": "User not found"}, 404

    user_info = {
        "id": user.id,
        "username": user.username,
        "mail": user.mail,
        "is_admin": user.is_admin,
    }
    return user_info, 200


@app.route("/user", methods=["POST"])
def create_user():
    data = request.json

    existing_user = User.query.filter(
        (User.username == data["username"]) | (User.mail == data["mail"])
    ).first()

    if existing_user:
        if existing_user.username == data["username"]:
            return {"error": "Username already exists"}, 409
        elif existing_user.mail == data["mail"]:
            return {"error": "Email already exists"}, 409

    user = User(
        username=data["username"],
        mail=data["mail"],
        password=hash_password(data["password"]),
        is_admin=data["is_admin"],
    )
    db.session.add(user)
    db.session.commit()
    return {"message": "User created successfully"}, 201


@app.route("/user/<int:id>", methods=["PATCH"])
@jwt_required()
def update_user(id):
    data = request.json
    user = db.session.query(User).get(id)
    user_request = db.session.query(User).get(get_jwt_identity())

    if user_request.id != user.id and not user_request.is_admin:
        return {"error": "Unauthorized"}, 401

    if user is None:
        return {"error": "User not found"}, 404

    if "username" in data and data["username"]:
        user.username = data["username"]
    if "mail" in data and data["mail"]:
        user.mail = data["mail"]
    if "password" in data and data["password"]:
        user.password = hash_password(data["password"])
    if "is_admin" in data and data["is_admin"]:
        user.is_admin = data["is_admin"]

    db.session.commit()
    return {"message": "User updated successfully"}


@app.route("/user/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_user(id):
    user = db.session.query(User).get(id)
    user_request = db.session.query(User).get(get_jwt_identity())

    if user_request.id != user.id and not user_request.is_admin:
        return {"error": "Unauthorized"}, 401

    if user is None:
        return {"error": "User not found"}, 404

    db.session.query(CollectionItem).filter(CollectionItem.user_id == id).delete()
    db.session.delete(user)
    db.session.commit()
    return {"message": "User deleted successfully"}


@app.route("/user/login", methods=["GET"])
def login_user():
    data = request.json
    user = User.query.filter_by(mail=data["mail"]).first()

    if user is None:
        return {"error": "User not found"}, 404

    if bcrypt.checkpw(data["password"].encode("utf-8"), user.password.encode("utf-8")):
        return {
            "message": "User logged in successfully",
            "token": create_access_token(identity=str(user.id)),
        }, 200
    else:
        return {"error": "Invalid password"}, 401

from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.app import app
from app.db.database import db
from app.db.models import CollectionItem, User
from app.utils import hash_password


@app.route("/user/me", methods=["GET"])
@jwt_required()
def get_me():
    user_id = get_jwt_identity()

    user = db.session.get(User, user_id)

    if not user:
        return {"error": "Utilisateur introuvable"}, 404

    return {"id": user.id, "username": user.username, "mail": user.mail, "is_admin": user.is_admin}, 200


@app.route("/user/<int:identifier>", methods=["GET"])
@jwt_required()
def get_user(identifier: int):
    user = db.session.get(User, identifier)
    user_request = db.session.get(User, get_jwt_identity())

    if not user:
        return {"error": "User not found"}, 404

    if user_request.id != user.id and not user_request.is_admin:
        return {"error": "Unauthorized"}, 401

    return {
        "id": user.id,
        "username": user.username,
        "mail": user.mail,
        "is_admin": user.is_admin,
    }, 200


@app.route("/user", methods=["POST"])
def create_user():
    data = request.json

    existing_user = User.query.filter(User.mail == data["mail"]).first()

    if existing_user:
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


@app.route("/user/<int:identifier>", methods=["PATCH"])
@jwt_required()
def update_user(identifier: int):
    data = request.json
    user = db.session.get(User, identifier)
    user_request = db.session.get(User, get_jwt_identity())

    if user is None:
        return {"error": "User not found"}, 404

    if user_request.id != user.id and not user_request.is_admin:
        return {"error": "Unauthorized"}, 401

    if data.get("username"):
        user.username = data["username"]
    if data.get("mail"):
        user.mail = data["mail"]
    if data.get("password"):
        user.password = hash_password(data["password"])
    if data.get("is_admin"):
        user.is_admin = data["is_admin"]

    db.session.commit()
    return {"message": "User updated successfully"}


@app.route("/user/<int:identifier>", methods=["DELETE"])
@jwt_required()
def delete_user(identifier: int):
    user = db.session.get(User, identifier)
    user_request = db.session.get(User, get_jwt_identity())

    if not user:
        return {"error": "User not found"}, 404

    if user_request.id != user.id and not user_request.is_admin:
        return {"error": "Unauthorized"}, 401

    db.session.query(CollectionItem).filter(CollectionItem.user_id == identifier).delete()
    db.session.delete(user)
    db.session.commit()
    return {"message": "User deleted successfully"}

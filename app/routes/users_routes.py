from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.app import app
from app.db.database import db
from app.db.models import Collection, CollectionItem, User
from app.utils import hash_password


@app.route("/user/me", methods=["GET"])
@jwt_required()
def get_me():
    user_id = get_jwt_identity()

    user = db.session.get(User, user_id)

    if not user:
        return {"error": "Utilisateur introuvable"}, 404

    return {
        "id": user.id,
        "username": user.username,
        "mail": user.mail,
        "is_admin": user.is_admin,
        "profile_image": user.profile_image,
    }, 200


@app.route("/user/<int:identifier>", methods=["GET"])
@jwt_required()
def get_user(identifier: int):
    user = db.session.get(User, identifier)
    user_request = db.session.get(User, get_jwt_identity())

    if not user:
        return {"error": "Utilisateur introuvable"}, 404

    if user_request.id != user.id and not user_request.is_admin:
        return {"error": "Non autorisé"}, 401

    return {
        "id": user.id,
        "username": user.username,
        "mail": user.mail,
        "is_admin": user.is_admin,
        "profile_image": user.profile_image,
    }, 200


@app.route("/user", methods=["POST"])
def create_user():
    data = request.json

    existing_mail = User.query.filter(User.mail == data["mail"]).first()
    existing_username = User.query.filter(User.username == data["username"]).first()

    if existing_mail:
        return {"error": "Email déjà utilisé"}, 409

    if existing_username:
        return {"error": "Nom d'utilisateur déjà utilisé"}, 409

    user = User(
        username=data["username"],
        mail=data["mail"],
        password=hash_password(data["password"]),
        is_admin=data.get("is_admin", False),
    )

    db.session.add(user)
    db.session.commit()

    collection = Collection(
        name="Defaut",
        user_id=user.id,
    )

    db.session.add(collection)
    db.session.commit()

    return {"message": "Utilisateur créé avec succès"}, 201


@app.route("/user", methods=["PATCH"])
@app.route("/user/<int:identifier>", methods=["PATCH"])
@jwt_required()
def update_user(identifier: int = None):
    data = request.json
    if not identifier:
        identifier = get_jwt_identity()

    user = db.session.get(User, identifier)
    user_request = db.session.get(User, get_jwt_identity())

    if user is None:
        return {"error": "Utilisateur introuvable"}, 404

    if user_request.id != user.id and not user_request.is_admin:
        return {"error": "Non autorisé"}, 401

    if data.get("username"):
        user.username = data["username"]
    if data.get("mail"):
        user.mail = data["mail"]
    if data.get("password"):
        user.password = hash_password(data["password"])
    if data.get("is_admin"):
        user.is_admin = data["is_admin"]
    if data.get("profile_image"):
        user.profile_image = data["profile_image"]

    db.session.commit()
    return {
        "username": user.username,
        "mail": user.mail,
        "is_admin": user.is_admin,
        "profile_image": user.profile_image,
    }, 200


@app.route("/user/<int:identifier>", methods=["DELETE"])
@jwt_required()
def delete_user(identifier: int):
    user = db.session.get(User, identifier)
    user_request = db.session.get(User, get_jwt_identity())

    if not user:
        return {"error": "Utilisateur introuvable"}, 404

    if user_request.id != user.id and not user_request.is_admin:
        return {"error": "Non autorisé"}, 401

    db.session.delete(user)
    db.session.commit()
    return {"message": "Utilisateur supprimé avec succès"}

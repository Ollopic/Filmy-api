from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.app import app
from app.db.database import db
from app.db.models import CollectionItem, User
from app.utils import validate_boolean_param, validate_state_param


@app.route("/user/<int:identifier>/collection", methods=["GET"])
@jwt_required()
def get_collection(identifier: int):
    user = db.session.get(User, identifier)
    user_request = db.session.get(User, get_jwt_identity())

    if user is None:
        return {"error": "Utilisateur introuvable"}, 404

    if user_request.id != user.id and not user_request.is_admin:
        return {"error": "Non autorisé"}, 401

    wishlist = request.args.get("wishlist")
    favorite = request.args.get("favorite")
    state = request.args.get("state")
    borrowed = request.args.get("borrowed")

    query = db.session.query(CollectionItem).filter(CollectionItem.user_id == identifier)

    if wishlist is not None:
        if not validate_boolean_param(wishlist):
            return {"error": "La valeur de wishlist doit être un booléen"}, 400

        query = query.filter(CollectionItem.in_wishlist == wishlist)

    if favorite is not None:
        if not validate_boolean_param(favorite):
            return {"error": "La valeur de favorite doit être un booléen"}, 400
        query = query.filter(CollectionItem.favorite == favorite)

    if state:
        if not validate_state_param(state):
            return {"error": "La valeur de state doit être 'Physique' ou 'Numérique'"}, 400
        query = query.filter(CollectionItem.state == state)

    if borrowed is not None:
        if not validate_boolean_param(borrowed):
            return {"error": "La valeur de borrowed doit être un booléen"}, 400
        query = query.filter(CollectionItem.borrowed == borrowed)

    collection = query.all()

    if not collection:
        return {"error": "Aucun item trouvé"}, 404

    return [
        {
            "id": item.id,
            "state": item.state,
            "borrowed": item.borrowed,
            "borrowed_at": item.borrowed_at,
            "borrowed_by": item.borrowed_by,
            "favorite": item.favorite,
            "in_wishlist": item.in_wishlist,
            "film": {
                "id": item.film.id,
                "id_tmdb": item.film.id_tmdb,
                "data": item.film.data,
                "image_path": item.film.image_path,
                "poster_path": item.film.poster_path,
            },
        }
        for item in collection
    ]


@app.route("/user/<int:identifier>/collection", methods=["POST"])
@jwt_required()
def create_item(identifier: int):
    user = db.session.get(User, identifier)
    user_request = db.session.get(User, get_jwt_identity())

    if user is None:
        return {"error": "Utilisateur introuvable"}, 404

    if user_request.id != user.id and not user_request.is_admin:
        return {"error": "Non autorisé"}, 401

    data = request.json

    item = CollectionItem(
        user_id=identifier,
        film_id=data["film_id"],
        state=data["state"],
        borrowed=data["borrowed"],
        favorite=data["favorite"],
        in_wishlist=data["in_wishlist"],
    )

    db.session.add(item)
    db.session.commit()

    return {"message": "Item ajouté avec succès"}, 201


@app.route("/user/<int:identifier>/collection/<int:item_id>", methods=["PATCH"])
@jwt_required()
def update_item(identifier: int, item_id: int):
    user = db.session.get(User, identifier)
    user_request = db.session.get(User, get_jwt_identity())

    if user is None:
        return {"error": "Utilisateur introuvable"}, 404

    if user_request.id != user.id and not user_request.is_admin:
        return {"error": "Non autorisé"}, 401

    item = db.session.get(CollectionItem, item_id)

    if item is None:
        return {"error": "Item introuvable"}, 404

    if item.user_id != identifier and not user_request.is_admin:
        return {"error": "Non autorisé"}, 401

    data = request.json

    if "film_id" in data:
        item.film_id = data["film_id"]
    if "state" in data:
        item.state = data["state"]
    if "borrowed" in data:
        item.borrowed = data["borrowed"]
    if "favorite" in data:
        item.favorite = data["favorite"]
    if "in_wishlist" in data:
        item.in_wishlist = data["in_wishlist"]

    db.session.commit()

    return {"message": "Item mis à jour avec succès"}, 200


@app.route("/user/<int:identifier>/collection/<int:item_id>", methods=["DELETE"])
@jwt_required()
def delete_item(identifier: int, item_id: int):
    user = db.session.get(User, identifier)
    user_request = db.session.get(User, get_jwt_identity())

    if user is None:
        return {"error": "Utilisateur introuvable"}, 404

    if user_request.id != user.id and not user_request.is_admin:
        return {"error": "Non autorisé"}, 401

    item = db.session.get(CollectionItem, item_id)

    if item is None:
        return {"error": "Item introuvable"}, 404

    if item.user_id != identifier and not user_request.is_admin:
        return {"error": "Non autorisé"}, 401

    db.session.delete(item)
    db.session.commit()

    return {"message": "Item supprimé avec succès"}, 200

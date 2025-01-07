from flask import request
from flask_jwt_extended import jwt_required

from app.app import app
from app.db.database import db
from app.db.models import CollectionItem
from app.utils import validate_boolean_param, validate_state_param


@app.route("/user/<int:identifier>/collection", methods=["GET"])
@jwt_required()
def get_collection(identifier: int):
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

    return  {"message": "Item ajouté avec succès"}, 201
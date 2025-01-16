from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.app import app
from app.db.database import db
from app.db.models import Collection, CollectionItem, Film, User
from app.utils import create_movie_if_not_exists, validate_state_param


@app.route("/collection", methods=["GET"])
@jwt_required()
def get_all_collections():
    user_id = get_jwt_identity()
    collections = Collection.query.filter_by(user_id=user_id).all()

    return [
        {"id": c.id, "name": c.name, "picture": c.picture, "items_count": len(c.collection_items)} for c in collections
    ]


@app.route("/collection", methods=["POST"])
@jwt_required()
def create_collection():
    user = db.session.get(User, get_jwt_identity())
    data = request.json

    if not data.get("name"):
        return {"error": "Name is required"}, 400

    collection = Collection(name=data["name"], picture=data.get("picture"), user_id=user.id)

    db.session.add(collection)
    db.session.commit()

    return {"message": "Collection créé avec succès"}, 201


@app.route("/collection/<int:identifier>", methods=["GET"])
@jwt_required()
def get_collection(identifier):
    user = db.session.get(User, get_jwt_identity())
    if user is None:
        return {"error": "Utilisateur non trouvé"}, 404

    collection = db.session.get(Collection, identifier)
    if collection is None:
        return {"error": "Collection introuvable"}, 404

    if collection.user_id != user.id:
        return {"error": "Unauthorized"}, 403

    collection_items = db.session.query(CollectionItem).filter(CollectionItem.collection_id == identifier).all()

    items_data = []
    for item in collection_items:
        film = db.session.query(Film).filter(Film.id == item.film_id).first()
        items_data.append(
            {
                "state": item.state,
                "borrowed": item.borrowed,
                "borrowed_at": item.borrowed_at,
                "borrowed_by": item.borrowed_by,
                "favorite": item.favorite,
                "in_wishlist": item.in_wishlist,
                "film": {
                    "id": film.data["id"],
                    "title": film.data["title"],
                    "poster_path": film.data["poster_path"],
                }
                if film
                else None,
            }
        )

    return {
        "id": collection.id,
        "name": collection.name,
        "picture": collection.picture,
        "items": items_data,
    }


@app.route("/collection/<int:identifier>", methods=["POST"])
@jwt_required()
def create_item_collection(identifier):
    user = db.session.get(User, get_jwt_identity())
    data = request.json

    collection = Collection.query.get(identifier)

    if collection is None:
        return {"error": "Collection introuvable"}, 404

    if collection.user_id != user.id:
        return {"error": "Unauthorized"}, 403

    if not data.get("film_id"):
        return {"error": "Film ID is required"}, 400

    if not data.get("state"):
        return {"error": "State is required"}, 400

    if not validate_state_param(data["state"]):
        return {"error": "Invalid state"}, 400

    film = db.session.query(Film).filter(Film.id_tmdb == data["film_id"]).first()
    if film is None:
        film = create_movie_if_not_exists(data["film_id"])

    existing_item = (
        db.session.query(CollectionItem)
        .filter(CollectionItem.film_id == film.id, CollectionItem.collection_id == identifier)
        .first()
    )
    if existing_item:
        return {"error": "Film déjà présent dans la collection"}, 400

    item = CollectionItem(
        state=data["state"],
        borrowed=data.get("borrowed"),
        borrowed_at=data.get("borrowed_at"),
        borrowed_by=data.get("borrowed_by"),
        favorite=data.get("favorite"),
        in_wishlist=data.get("in_wishlist"),
        film_id=film,
        collection_id=identifier,
    )

    db.session.add(item)
    db.session.commit()

    return {"message": "Item de collection créé avec succès"}, 201

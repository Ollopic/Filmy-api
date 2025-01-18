from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from sqlalchemy.exc import IntegrityError

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
        return {"error": "Le champ name est requis"}, 400

    collection = Collection(name=data["name"], picture=data.get("picture"), user_id=user.id)

    try:
        db.session.add(collection)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return {"error": "Une collection avec ce nom existe déjà pour cet utilisateur."}, 409

    return {"message": "Collection créé avec succès"}, 201


@app.route("/collection/<int:identifier>", methods=["PATCH"])
@jwt_required()
def update_collection(identifier):
    user = db.session.get(User, get_jwt_identity())
    collection = db.session.get(Collection, identifier)
    data = request.json

    if collection.user_id != user.id:
        return {"error": "Non autorisé"}, 403

    if data.get("name"):
        collection.name = data["name"]
    if data.get("picture"):
        collection.picture = data["picture"]

    db.session.commit()

    return {"message": "Collection modifié avec succès"}, 200


@app.route("/collection/<int:identifier>", methods=["DELETE"])
@jwt_required()
def delete_collection(identifier):
    user = db.session.get(User, get_jwt_identity())
    collection = db.session.get(Collection, identifier)

    if collection is None:
        return {"error": "Collection introuvable"}, 404

    if collection.user_id != user.id:
        return {"error": "Non autorisé"}, 403

    db.session.delete(collection)
    db.session.commit()

    return {"message": "Collection supprimé avec succès"}, 200


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
        return {"error": "Non autorisé"}, 403

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
        return {"error": "Non autorisé"}, 403

    if not data.get("film_id"):
        return {"error": "film_id est requis"}, 400

    if not data.get("state"):
        return {"error": "state est requis"}, 400

    if not validate_state_param(data["state"]):
        return {"error": "state invalide"}, 400

    film = db.session.query(Film).filter(Film.id_tmdb == data["film_id"]).first()
    if film is None:
        film = create_movie_if_not_exists(data["film_id"])

    existing_item = (
        db.session.query(CollectionItem)
        .filter(
            CollectionItem.film_id == film.id,
            CollectionItem.collection_id == identifier,
            CollectionItem.user_id == user,
        )
        .first()
    )
    if existing_item:
        return {"error": "Film déjà présent dans une des collections"}, 400

    item = CollectionItem(
        state=data["state"],
        borrowed=data.get("borrowed"),
        borrowed_at=data.get("borrowed_at"),
        borrowed_by=data.get("borrowed_by"),
        favorite=data.get("favorite"),
        in_wishlist=data.get("in_wishlist"),
        film_id=film.id,
        collection_id=identifier,
    )

    db.session.add(item)
    db.session.commit()

    return {"message": "Item de collection créé avec succès"}, 201


@app.route("/collection/<int:collection_id>/<int:film_id>", methods=["PATCH"])
@jwt_required()
def update_item_collection(collection_id, film_id):
    user = db.session.get(User, get_jwt_identity())
    collection = db.session.get(Collection, collection_id)
    data = request.json

    if collection.user_id != user.id:
        return {"error": "Non autorisé"}, 403

    film_idtmdb = db.session.query(Film).filter(Film.id_tmdb == film_id).first()

    item = (
        db.session.query(CollectionItem)
        .filter(CollectionItem.film_id == film_idtmdb.id, CollectionItem.collection_id == collection_id)
        .first()
    )
    if item is None:
        return {"error": "Item introuvable"}, 404

    if data.get("state"):
        if not validate_state_param(data["state"]):
            return {"error": "state invalide"}, 400
        item.state = data["state"]
    if data.get("borrowed"):
        item.borrowed = data["borrowed"]
    if data.get("borrowed_at"):
        item.borrowed_at = data["borrowed_at"]
    if data.get("borrowed_by"):
        item.borrowed_by = data["borrowed_by"]
    if data.get("favorite"):
        item.favorite = data["favorite"]
    if data.get("in_wishlist"):
        item.in_wishlist = data["in_wishlist"]

    db.session.commit()

    return {"message": "Item de collection modifié avec succès"}, 200


@app.route("/collection/<int:collection_id>/<int:film_id>", methods=["DELETE"])
@jwt_required()
def delete_item_collection(collection_id, film_id):
    user = db.session.get(User, get_jwt_identity())
    collection = db.session.get(Collection, collection_id)

    if collection is None:
        return {"error": "Collection introuvable"}, 404

    if collection.user_id != user.id:
        return {"error": "Non autorisé"}, 403

    film_idtmdb = db.session.query(Film).filter(Film.id_tmdb == film_id).first()

    item = (
        db.session.query(CollectionItem)
        .filter(CollectionItem.film_id == film_idtmdb.id, CollectionItem.collection_id == collection_id)
        .first()
    )
    if item is None:
        return {"error": "Item introuvable"}, 404

    db.session.delete(item)
    db.session.commit()

    return {"message": "Item de collection supprimé avec succès"}, 200

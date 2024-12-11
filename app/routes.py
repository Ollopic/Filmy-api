from flask import jsonify, request

from .app import app
from .database import db
from .models import Film, User


# Récupérer la liste de tous les films
@app.route("/movies", methods=["GET"])
def get_movies():
    movies = db.session.query(Film).all()
    movies_data = []
    for movie in movies:
        film_info = {
            "id": movie.id,
            "id_tmdb": movie.id_tmdb,
            "data": movie.data,
            "image_path": movie.image_path,
            "poster_path": movie.poster_path,
        }
        movies_data.append(film_info)
    return jsonify(movies_data)


# Récupérer un film par son ID
@app.route("/movies/<int:id>", methods=["GET"])
def get_movie(id):
    movie = db.session.query(Film).get(id)

    if movie is None:
        return jsonify({"error": "Movie not found"}), 404

    film_info = {
        "id": movie.id,
        "id_tmdb": movie.id_tmdb,
        "data": movie.data,
        "image_path": movie.image_path,
        "poster_path": movie.poster_path,
    }
    return jsonify(film_info)


# Récupérer les infos d'un utilisateur
@app.route("/user/<int:id>", methods=["GET"])
def get_user(id):
    user = db.session.query(User).get(id)

    if user is None:
        return jsonify({"error": "User not found"}), 404

    user_info = {
        "id": user.id,
        "username": user.username,
        "mail": user.mail,
        "is_admin": user.is_admin,
    }
    return jsonify(user_info)


# Créer un nouvel utilisateur
@app.route("/user", methods=["POST"])
def create_user():
    data = request.json

    existing_user = User.query.filter(
        (User.username == data["username"]) | (User.mail == data["mail"])
    ).first()

    if existing_user:
        if existing_user.username == data["username"]:
            return jsonify({"error": "Username already exists"}), 409
        elif existing_user.mail == data["mail"]:
            return jsonify({"error": "Email already exists"}), 409

    user = User(
        username=data["username"],
        mail=data["mail"],
        password=data["password"],
        is_admin=data["is_admin"],
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User created successfully"}), 201


# Modifier les informations d'un utilisateur
@app.route("/user/<int:id>", methods=["PATCH"])
def update_user(id):
    data = request.json
    user = db.session.query(User).get(id)

    if user is None:
        return jsonify({"error": "User not found"}), 404

    if "username" in data and data["username"]:
        user.username = data["username"]
    if "mail" in data and data["mail"]:
        user.mail = data["mail"]
    if "password" in data and data["password"]:
        user.password = data["password"]
    if "is_admin" in data and data["is_admin"]:
        user.is_admin = data["is_admin"]

    db.session.commit()
    return jsonify({"message": "User updated successfully"})


# Supprimer un utilisateur
@app.route("/user/<int:id>", methods=["DELETE"])
def delete_user(id):
    user = db.session.query(User).get(id)

    if user is None:
        return jsonify({"error": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully"})

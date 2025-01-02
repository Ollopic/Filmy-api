import json

from flask import request

from app.app import app
from app.db.database import db
from app.db.models import Film


@app.route("/movies", methods=["GET"])
def get_movies():
    return [
        {
            "id": movie.id,
            "id_tmdb": movie.id_tmdb,
            "data": movie.data,
            "image_path": movie.image_path,
            "poster_path": movie.poster_path,
        }
        for movie in db.session.query(Film).all()
    ]


@app.route("/movies/<int:id>", methods=["GET"])
def get_movie(id: int):
    movie = db.session.get(Film, id)

    if not movie:
        return {"error": "Movie not found"}, 404

    return {
        "id": movie.id,
        "id_tmdb": movie.id_tmdb,
        "data": movie.data,
        "image_path": movie.image_path,
        "poster_path": movie.poster_path,
    }


@app.route("/movies", methods=["POST"])
def create_movie():
    data = request.json

    existing_movie = Film.query.filter(Film.id_tmdb == data["id_tmdb"]).first()

    if not isinstance(data.get("data"), (dict, list)):
        return {"error": "The 'data' field must be a JSON object or array"}, 400

    if existing_movie:
        return {"error": "Movie already exists"}, 409

    movie = Film(
        id_tmdb=data["id_tmdb"],
        data=data["data"],
        image_path=data["image_path"],
        poster_path=data["poster_path"],
    )

    db.session.add(movie)
    db.session.commit()

    return {"message": "Movie created successfully"}, 201

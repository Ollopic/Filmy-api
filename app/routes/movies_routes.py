from flask import request

from app.app import app
from app.db.database import db
from app.db.models import CreditsFilm, Film
from app.themoviedb.client import Client


@app.route("/movies/popular", methods=["GET"])
def get_popular_movies():
    client = Client()
    response = client.get_popular_movies()

    return response["results"], 200


@app.route("/movies/trending", methods=["GET"])
def get_trending_movies():
    client = Client()
    response = client.get_trending_movies()

    return response["results"], 200


@app.route("/movies/search", methods=["GET"])
def search_movie():
    title = request.args.get("title")

    if not title:
        return {"error": "Paramètre 'title' manquant"}, 400

    client = Client()
    response = client.get_movie_by_title(title)

    return response["results"], 200


@app.route("/movies/<int:identifier>", methods=["GET"])
def get_movie(identifier: int):
    movie = db.session.get(Film, identifier)

    if not movie:
        tmdb_client = Client()
        movie_data = tmdb_client.get_movie_by_id(identifier)

        return movie_data, 200

    return {
        "id": movie.id,
        "id_tmdb": movie.id_tmdb,
        "data": movie.data,
        "image_path": movie.image_path,
        "poster_path": movie.poster_path,
    }


@app.route("/movies/<int:identifier>/credits", methods=["GET"])
def get_movie_credits(identifier: int):
    movie = db.session.get(Film, identifier)
    if not movie:
        return {"error": "Movie not found"}, 404

    credits = db.session.query(CreditsFilm).filter(CreditsFilm.film_id == identifier).all()

    result = [
        {
            "person_id": credit.person_id,
            "character": credit.character,
        }
        for credit in credits
    ]

    return result, 200


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

from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from requests.exceptions import HTTPError

from app.app import app
from app.db.database import db
from app.db.models import CollectionItem, CreditsFilm, Film
from app.themoviedb.client import Client
from app.utils import search_movie_in_tmdb

tmdb_client = Client()


@app.route("/movies/popular", methods=["GET"])
def get_popular_movies():
    data = tmdb_client.get_popular_movies()["results"]

    result = [
        {
            "id_tmdb": movie["id"],
            "title": movie["title"],
            "release_date": movie["release_date"],
            "vote_average": movie["vote_average"],
            "poster_path": movie["poster_path"],
        }
        for movie in data
    ]

    return result, 200


@app.route("/movies/trending", methods=["GET"])
def get_trending_movies():
    data = tmdb_client.get_trending_movies()["results"]

    result = [
        {
            "id_tmdb": movie["id"],
            "title": movie["title"],
            "release_date": movie["release_date"],
            "vote_average": movie["vote_average"],
            "poster_path": movie["poster_path"],
        }
        for movie in data
    ]

    return result, 200


@app.route("/movies/top_rated", methods=["GET"])
def get_top_rating_movies():
    data = tmdb_client.get_top_rating_movies()["results"]

    result = [
        {
            "id_tmdb": movie["id"],
            "title": movie["title"],
            "release_date": movie["release_date"],
            "vote_average": movie["vote_average"],
            "poster_path": movie["poster_path"],
        }
        for movie in data
    ]

    return result, 200


@app.route("/movies/upcoming", methods=["GET"])
def get_upcoming_movies():
    data = tmdb_client.get_upcoming_movies()["results"]

    result = [
        {
            "id_tmdb": movie["id"],
            "title": movie["title"],
            "release_date": movie["release_date"],
            "vote_average": movie["vote_average"],
            "poster_path": movie["poster_path"],
        }
        for movie in data
    ]

    return result, 200


@app.route("/movies/now_playing", methods=["GET"])
def get_movies_now_playing():
    data = tmdb_client.get_movies_now_playing()["results"]

    result = [
        {
            "id_tmdb": movie["id"],
            "title": movie["title"],
            "release_date": movie["release_date"],
            "vote_average": movie["vote_average"],
            "poster_path": movie["poster_path"],
        }
        for movie in data
    ]

    return result, 200


@app.route("/movies", methods=["GET"])
def search_movie():
    title = request.args.get("title")
    data = tmdb_client.get_movie_by_title(title)

    result = [
        {
            "id_tmdb": movie["id"],
            "title": movie["title"],
            "overview": movie["overview"],
            "poster_path": movie["poster_path"],
        }
        for movie in data["results"]
    ]

    return {
        "total_results": data["total_results"],
        "movies": result,
    }, 200


@app.route("/movies/<int:identifier>", methods=["GET"])
@jwt_required(optional=True)
def get_movie(identifier: int):
    movie = db.session.query(Film).filter(Film.id_tmdb == identifier).first()
    user_id = get_jwt_identity()

    if not movie:
        try:
            movie_data, _ = search_movie_in_tmdb(identifier)
            return movie_data, 200

        except HTTPError as e:
            if e.response.status_code == 404:
                return {"error": "Film introuvable"}, 404
            return {"error": "Erreur lors de la communication avec l'API TMDB"}, 500

    if user_id:
        user_movie = (
            db.session.query(CollectionItem)
            .filter(CollectionItem.user_id == user_id, CollectionItem.film_id == movie.id)
            .first()
        )

        if user_movie:
            movie.data["collection_item"] = {
                "state": user_movie.state,
                "borrowed": user_movie.borrowed,
                "borrowed_at": user_movie.borrowed_at,
                "borrowed_by": user_movie.borrowed_by,
                "favorite": user_movie.favorite,
            }

    return movie.data, 200


@app.route("/movies/<int:identifier>/credits", methods=["GET"])
def get_movie_credits(identifier: int):
    film_id = db.session.query(Film).filter(Film.id_tmdb == identifier).first()
    if not film_id:
        movie_data = tmdb_client.get_movie_credits(identifier)

        result = [
            {
                "id_tmdb": person["id"],
                "name": person["name"],
                "character": person["character"] if "character" in person else None,
                "profile_path": person["profile_path"],
            }
            for person in movie_data["cast"]
        ]

        return result, 200

    credits = db.session.query(CreditsFilm).filter(CreditsFilm.film_id == film_id.id).all()

    result = [
        {
            "id_tmdb": credit.person.id_tmdb,
            "name": credit.person.data["name"],
            "character": credit.character,
            "profile_path": credit.person.data["profile_path"],
        }
        for credit in credits
    ]

    return result, 200

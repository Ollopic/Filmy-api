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

    results = [
        {
            "id_tmdb": movie["id"],
            "title": movie["title"],
            "release_date": movie["release_date"],
            "vote_average": movie["vote_average"],
            "poster_path": movie["poster_path"],
        }
        for movie in data
    ]

    return results, 200


@app.route("/movies/trending", methods=["GET"])
def get_trending_movies():
    data = tmdb_client.get_trending_movies()["results"]

    results = [
        {
            "id_tmdb": movie["id"],
            "title": movie["title"],
            "release_date": movie["release_date"],
            "vote_average": movie["vote_average"],
            "poster_path": movie["poster_path"],
        }
        for movie in data
    ]

    return results, 200


@app.route("/movies/top_rated", methods=["GET"])
def get_top_rating_movies():
    data = tmdb_client.get_top_rating_movies()["results"]

    results = [
        {
            "id_tmdb": movie["id"],
            "title": movie["title"],
            "release_date": movie["release_date"],
            "vote_average": movie["vote_average"],
            "poster_path": movie["poster_path"],
        }
        for movie in data
    ]

    return results, 200


@app.route("/movies/upcoming", methods=["GET"])
def get_upcoming_movies():
    data = tmdb_client.get_upcoming_movies()["results"]

    results = [
        {
            "id_tmdb": movie["id"],
            "title": movie["title"],
            "release_date": movie["release_date"],
            "vote_average": movie["vote_average"],
            "poster_path": movie["poster_path"],
        }
        for movie in data
    ]

    return results, 200


@app.route("/movies/now_playing", methods=["GET"])
def get_movies_now_playing():
    data = tmdb_client.get_movies_now_playing()["results"]

    results = [
        {
            "id_tmdb": movie["id"],
            "title": movie["title"],
            "release_date": movie["release_date"],
            "vote_average": movie["vote_average"],
            "poster_path": movie["poster_path"],
        }
        for movie in data
    ]

    return results, 200


@app.route("/movies", methods=["GET"])
def search_movie():
    title = request.args.get("title")
    page = request.args.get("page", 1, type=int)

    data = tmdb_client.get_movie_by_title(title, page)

    results = [
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
        "movies": results,
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
            if user_movie.collection_id:
                movie.data["collection_item"] = {
                    "state": user_movie.state,
                    "borrowed": user_movie.borrowed,
                    "borrowed_at": user_movie.borrowed_at,
                    "borrowed_by": user_movie.borrowed_by,
                    "favorite": user_movie.favorite,
                    "id": user_movie.collection_id,
                }
            else:
                movie.data["wishlist"] = True

    return movie.data, 200


@app.route("/movies/<int:identifier>/credits", methods=["GET"])
def get_movie_credits(identifier: int):
    film_id = db.session.query(Film).filter(Film.id_tmdb == identifier).first()
    if not film_id:
        movie_data = tmdb_client.get_movie_credits(identifier)

        results = [
            {
                "id_tmdb": person["id"],
                "name": person["name"],
                "character": person["character"] if "character" in person else None,
                "profile_path": person["profile_path"],
            }
            for person in movie_data["cast"]
        ]

        return results, 200

    credits = db.session.query(CreditsFilm).filter(CreditsFilm.film_id == film_id.id).all()

    results = [
        {
            "id_tmdb": credit.person.id_tmdb,
            "name": credit.person.data["name"],
            "character": credit.character,
            "profile_path": credit.person.data["profile_path"],
        }
        for credit in credits
    ]

    return results, 200


@app.route("/movies/genres", methods=["GET"])
def get_movie_genre_list():
    return tmdb_client.get_movie_genres()["genres"], 200


@app.route("/movies/discover", methods=["GET"])
def discover_movies():
    params = {}
    genres = request.args.getlist("with_genres")
    page = request.args.get("page", 1, type=int)
    if page:
        params["page"] = page

    if genres:
        params["with_genres"] = ",".join(genres)

    sort_by = request.args.get("sort_by")
    if sort_by:
        params["sort_by"] = sort_by

    release_date_gte = request.args.get("release_date.gte")
    if release_date_gte:
        params["release_date.gte"] = release_date_gte

    release_date_lte = request.args.get("release_date.lte")
    if release_date_lte:
        params["release_date.lte"] = release_date_lte

    with_runtime_gte = request.args.get("with_runtime.gte")
    if with_runtime_gte:
        params["with_runtime.gte"] = with_runtime_gte

    with_runtime_lte = request.args.get("with_runtime.lte")
    if with_runtime_lte:
        params["with_runtime.lte"] = with_runtime_lte

    data = tmdb_client.discover_movies(params)["results"]

    results = [
        {
            "id_tmdb": movie["id"],
            "title": movie["title"],
            "release_date": movie["release_date"],
            "vote_average": movie["vote_average"],
            "poster_path": movie["poster_path"],
        }
        for movie in data
    ]

    return results, 200

from flask import request
from requests.exceptions import HTTPError

from app.app import app
from app.db.database import db
from app.db.models import CreditsFilm, Film
from app.themoviedb.client import Client
from app.utils import create_credits_if_not_exists, create_movie_if_not_exists

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


@app.route("/movies/search", methods=["GET"])
def search_movie():
    title = request.args.get("title")
    data = tmdb_client.get_movie_by_title(title)["results"]

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


@app.route("/movies/<int:identifier>", methods=["GET"])
def get_movie(identifier: int):
    movie = db.session.query(Film).filter(Film.id_tmdb == identifier).first()

    if not movie:
        try:
            movie_data = tmdb_client.get_movie_by_id(identifier)
            data_person = tmdb_client.get_movie_credits(identifier)

            director = None
            for person in data_person["crew"]:
                if person["job"] == "Director":
                    director = person["name"]
            movie_data["director"] = director

            trailer = tmdb_client.get_movie_videos(identifier)["results"][0]
            if trailer is not None:
                if trailer["site"] != "YouTube":
                    movie_data["trailerKey"] = None
                movie_data["trailerKey"] = trailer["key"]

            data_movie = {
                "id_tmdb": movie_data["id"],
                "data": movie_data,
            }

            film_id = create_movie_if_not_exists(data_movie)
            create_credits_if_not_exists(data_person, film_id)
            return movie_data, 200

        except HTTPError as e:
            if e.response.status_code == 404:
                return {"error": "Film introuvable"}, 404
            return {"error": "Erreur lors de la communication avec l'API TMDB"}, 500

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
                "order": person["order"],
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
            "order": credit.person.data["order"],
        }
        for credit in credits
    ]

    return result, 200

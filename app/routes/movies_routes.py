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
    data = tmdb_client.get_movie_by_title(title)

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
def get_movie(identifier: int):
    movie = db.session.query(Film).filter(Film.id_tmdb == identifier).first()

    if not movie:
        try:
            movie_data = tmdb_client.get_movie_by_id(identifier)
            data_person = tmdb_client.get_movie_credits(identifier)

            # Get director
            director = None
            for person in data_person["crew"]:
                if person["job"] == "Director":
                    director = person["name"]
            movie_data["director"] = director

            # Get trailer
            trailers = tmdb_client.get_movie_videos(identifier)["results"] or []
            for trailer in trailers:
                if trailer["site"].lower() == "youtube" and trailer["type"].lower() == "trailer":
                    movie_data["trailer_key"] = trailer["key"]
                    break

            if not trailers:
                movie_data["trailer_key"] = None

            # Get release dates FR
            release_dates = tmdb_client.get_movie_release_dates(identifier)["results"]
            for release_date in release_dates:
                if release_date["iso_3166_1"] == "FR":
                    movie_data["age_restriction"] = release_date["release_dates"][0]["certification"]
                    break

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
    if genres:
        params["with_genres"] = ','.join(genres)

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

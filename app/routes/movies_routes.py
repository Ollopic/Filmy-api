from app.app import app
from app.db.database import db
from app.db.models import Film


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
    return movies_data


@app.route("/movies/<int:id>", methods=["GET"])
def get_movie(id):
    movie = db.session.query(Film).get(id)

    if movie is None:
        return {"error": "Movie not found"}, 404

    film_info = {
        "id": movie.id,
        "id_tmdb": movie.id_tmdb,
        "data": movie.data,
        "image_path": movie.image_path,
        "poster_path": movie.poster_path,
    }
    return film_info

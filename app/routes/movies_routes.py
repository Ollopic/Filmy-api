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
def get_movie(identifier: int):
    movie = db.session.query(Film).get(identifier)

    if not movie:
        return {"error": "Movie not found"}, 404

    return {
        "id": movie.id,
        "id_tmdb": movie.id_tmdb,
        "data": movie.data,
        "image_path": movie.image_path,
        "poster_path": movie.poster_path,
    }

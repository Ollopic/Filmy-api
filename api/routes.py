from .app import app
from flask import jsonify
from .database import db
from .models import Film


# Récupérer la liste de tous les films
@app.route('/movies', methods=['GET'])
def get_movies():
    movies = db.session.query(Film).all()
    movies_data = []
    for movie in movies:
        film_info = {
            "id": movie.id,
            "id_tmdb": movie.id_tmdb,
            "data": movie.data,
            "image_path": movie.image_path,
            "poster_path": movie.poster_path
        }
        movies_data.append(film_info)
    return jsonify(movies_data)


# Récupérer un film par son ID
@app.route('/movies/<int:id>', methods=['GET'])
def get_movie(id):
    movie = db.session.query(Film).get(id)
    film_info = {
        "id": movie.id,
        "id_tmdb": movie.id_tmdb,
        "data": movie.data,
        "image_path": movie.image_path,
        "poster_path": movie.poster_path
    }
    return jsonify(film_info)
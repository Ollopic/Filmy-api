import json

with open("app/db/fixtures/datas/films.json", "r") as file:
    data = json.load(file)


def test_get_movies_returns_list(client):
    """Test que l'endpoint /movies renvoie une liste de films"""
    response = client.get('/movies')
    assert response.status_code == 200
    movies = response.json
    assert isinstance(movies, list)
    assert len(movies) > 0


def test_get_movies_contains_specific_movie(client):
    """Test que l'endpoint /movies contient un film avec des informations spécifiques"""
    response = client.get('/movies')
    assert response.status_code == 200

    movies = response.json
    specific_movie = {
        "id_tmdb": 1241982,
        "data": data["film1"],
        "image_path": "/tElnmtQ6yz1PjN1kePNl8yMSb59.jpg",
        "poster_path": "/m0SbwFNCa9epW1X60deLqTHiP7x.jpg",
    }

    assert any(
        movie["id_tmdb"] == specific_movie["id_tmdb"]
        and movie["data"] == specific_movie["data"]
        and movie["image_path"] == specific_movie["image_path"]
        and movie["poster_path"] == specific_movie["poster_path"]
        for movie in movies
    )


def test_get_movie_by_id(client):
    """Test que l'endpoint /movies/<int:id> renvoie bien les informations d'un film"""
    specific_id = 1
    response = client.get(f'/movies/{specific_id}')
    assert response.status_code == 200

    movie = response.json
    expected_movie = {
        "id": specific_id,
        "id_tmdb": 1241982,
        "data": data["film1"],
        "image_path": "/tElnmtQ6yz1PjN1kePNl8yMSb59.jpg",
        "poster_path": "/m0SbwFNCa9epW1X60deLqTHiP7x.jpg",
    }

    assert movie["id"] == expected_movie["id"]
    assert movie["id_tmdb"] == expected_movie["id_tmdb"]
    assert movie["data"] == expected_movie["data"]
    assert movie["image_path"] == expected_movie["image_path"]
    assert movie["poster_path"] == expected_movie["poster_path"]


def test_get_movie_by_id_not_found(client):
    """Test que l'endpoint /movies/<int:id> renvoie une erreur 404 si le film n'existe pas"""
    non_existent_id = 9999
    response = client.get(f'/movies/{non_existent_id}')
    assert response.status_code == 404

    error_response = response.json
    assert "error" in error_response
    assert error_response["error"] == "Film introuvable"

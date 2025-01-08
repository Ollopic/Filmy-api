import json

with open("app/db/fixtures/datas/films.json", "r") as file:
    data = json.load(file)

#
# ---- GET ----
#

def test_get_popular_movies(client):
    """Test que l'endpoint /movies/popular renvoie des films populaires"""
    response = client.get('/movies/popular')
    assert response.status_code == 200

    movies = response.json
    assert isinstance(movies, list)
    assert len(movies) > 0



def test_get_trending_movies(client):
    """Test que l'endpoint /movies/trending renvoie des films tendances"""
    response = client.get('/movies/trending')
    assert response.status_code == 200

    movies = response.json
    assert isinstance(movies, list)
    assert len(movies) > 0


def test_search_movie(client):
    """Test que l'endpoint /movies/search renvoie des films correspondant à un titre"""
    title = "The Matrix"
    response = client.get(f'/movies/search?title={title}')
    assert response.status_code == 200

    movies = response.json
    assert isinstance(movies, list)
    assert len(movies) > 0

    for movie in movies:
        assert "matrix" in movie["title"].lower()


def test_get_movie_by_id(client):
    """Test que l'endpoint /movies/<int:id> renvoie bien les informations d'un film"""
    response = client.get(f'/movies/2')
    assert response.status_code == 200

    movie = response.json
    expected_movie = {
        "id_tmdb": 2,
        "data": data["film2"]["data"],
        "poster_path": "/4HTJHLPLvhDG4D0m8IcUMh7i9h4.jpg",
        "backdrop_path": "/hQ4pYsIbP22TMXOUdSfC2mjWrO0.jpg",
    }

    assert movie["id_tmdb"] == expected_movie["id_tmdb"]
    assert movie["data"] == expected_movie["data"]
    assert movie["poster_path"] == expected_movie["poster_path"]
    assert movie["backdrop_path"] == expected_movie["backdrop_path"]


def test_get_movie_by_id_not_found(client):
    """Test que l'endpoint /movies/<int:id> renvoie une erreur 404 si le film n'existe pas"""
    non_existent_id = 999999999
    response = client.get(f'/movies/{non_existent_id}')
    assert response.status_code == 404

    error_response = response.json
    assert "error" in error_response
    assert error_response["error"] == "Film introuvable"


def test_get_movie_credits(client):
    """Test que l'endpoint /movies/<int:id>/credits renvoie les crédits d'un film"""   
    response = client.get(f'/movies/2/credits')
    assert response.status_code == 200

    credits = response.json
    assert isinstance(credits, list)

    expected_credits = [
        {"person_id": 6, "character": "Taisto Kasurinen"},
        {"person_id": 7, "character": "Irmeli Pihlaja"},
    ]

    for expected_credit in expected_credits:
        assert any(
            credit["person_id"] == expected_credit["person_id"]
            and credit["character"] == expected_credit["character"]
            for credit in credits
        ), f"Expected credit {expected_credit} not found in response"

#
# ---- CREATE MOVIE ----
#

def test_create_movie(client):
    """Test que l'endpoint /movies/id permet de créer un film correctement s'il n'existe pas dans la db"""
    response = client.get(f'/movies/11')
    assert response.status_code == 200

    movie = response.json
    expected_movie = {
        "id_tmdb": 11,
        "data": data["film7"]["data"],
        "poster_path": "/qelTNHrBSYjPvwdzsDBPVsqnNzc.jpg",
        "backdrop_path": "/4qCqAdHcNKeAHcK8tJ8wNJZa9cx.jpg",
    }

    assert movie["id_tmdb"] == expected_movie["id_tmdb"]
    assert movie["data"] == expected_movie["data"]
    assert movie["poster_path"] == expected_movie["poster_path"]
    assert movie["backdrop_path"] == expected_movie["backdrop_path"]

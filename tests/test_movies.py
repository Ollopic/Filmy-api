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


def test_get_top_rating_movies(client):
    """Test que l'endpoint /movies/top_rated renvoie des films bien notés"""
    response = client.get('/movies/top_rated')
    assert response.status_code == 200

    movies = response.json
    assert isinstance(movies, list)
    assert len(movies) > 0


def test_get_upcoming_movies(client):
    """Test que l'endpoint /movies/upcoming renvoie des films à venir"""
    response = client.get('/movies/upcoming')
    assert response.status_code == 200

    movies = response.json
    assert isinstance(movies, list)
    assert len(movies) > 0


def test_get_movies_now_playing(client):
    """Test que l'endpoint /movies/now_playing renvoie des films actuellement en salles"""
    response = client.get('/movies/now_playing')
    assert response.status_code == 200

    movies = response.json
    assert isinstance(movies, list)
    assert len(movies) > 0


def test_search_movie(client):
    """Test que l'endpoint /movies renvoie des films correspondant à un titre"""
    title = "The Matrix"
    response = client.get(f'/movies?title={title}')
    assert response.status_code == 200

    results = response.json

    assert "total_results" in results

    movies = results["movies"]
    assert isinstance(movies, list)
    assert len(movies) > 0

    for movie in movies:
        assert "matrix" in movie["title"].lower()


def test_get_movie_by_id(client):
    """Test que l'endpoint /movies/<int:id> renvoie bien les informations d'un film"""
    response = client.get('/movies/2')
    assert response.status_code == 200

    movie = response.json
    expected_movie = data["film2"]["data"]

    assert movie == expected_movie


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
    response = client.get('/movies/11/credits')
    assert response.status_code == 200

    credits = response.json
    assert isinstance(credits, list)

    expected_credits = [
        {
            "character": "Luke Skywalker",
            "id_tmdb": 2,
            "name": "Mark Hamill",
            "profile_path": "/2ZulC2Ccq1yv3pemusks6Zlfy2s.jpg"
        }
    ]

    for expected_credit in expected_credits:
        assert any(
            credit["id_tmdb"] == expected_credit["id_tmdb"]
            and credit["character"] == expected_credit["character"]
            and credit["name"] == expected_credit["name"]
            and credit["profile_path"] == expected_credit["profile_path"]
            for credit in credits
        ), f"Expected credit {expected_credit} not found in response"


#
# ---- CREATE MOVIE ----
#

def test_create_movie(client):
    """Test que l'endpoint /movies/id permet de créer un film correctement s'il n'existe pas dans la db"""
    response = client.get('/movies/11')
    assert response.status_code == 200

    movie = response.json
    expected_movie = data["film7"]["data"]

    assert movie == expected_movie

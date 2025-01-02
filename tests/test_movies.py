import json

with open("app/db/fixtures/datas/films.json", "r") as file:
    data = json.load(file)

#
# ---- GET ----
#

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
    assert error_response["error"] == "Movie not found"


def test_get_movie_credits(client):
    """Test que l'endpoint /movies/<int:id>/credits renvoie les crédits d'un film"""   
    specific_id = 1
    response = client.get(f'/movies/{specific_id}/credits')
    assert response.status_code == 200

    credits = response.json
    assert isinstance(credits, list)

    expected_credits = [
        {"person_id": 1, "character": "John Doe"},
        {"person_id": 2, "character": "Jane Doe"},
    ]

    for expected_credit in expected_credits:
        assert any(
            credit["person_id"] == expected_credit["person_id"]
            and credit["character"] == expected_credit["character"]
            for credit in credits
        ), f"Expected credit {expected_credit} not found in response"

#
# ---- POST ----
#

def test_create_movie(client):
    """Test que l'endpoint /movies permet de créer un film correctement"""
    new_movie = {
        "id_tmdb": 9999,
        "data": data["film2"],
        "image_path": "/tElnmtQ6yz1PjN1kePNl8yMSb59.jpg",
        "poster_path": "/m0SbwFNCa9epW1X60deLqTHiP7x.jpg",
    }

    response = client.post('/movies', json=new_movie)
    assert response.status_code == 201

    success_response = response.json
    assert "message" in success_response
    assert success_response["message"] == "Movie created successfully"


def test_create_movie_already_exists(client):
    """Test que l'endpoint /movies renvoie une erreur 409 si le film existe déjà"""
    existing_movie = {
        "id_tmdb": 9999,
        "data": data["film2"],
        "image_path": "/tElnmtQ6yz1PjN1kePNl8yMSb59.jpg",
        "poster_path": "/m0SbwFNCa9epW1X60deLqTHiP7x.jpg",
    }

    response = client.post('/movies', json=existing_movie)
    assert response.status_code == 409

    error_response = response.json
    assert "error" in error_response
    assert error_response["error"] == "Movie already exists"


def test_create_movie_invalid_data(client):
    """Test que l'endpoint /movies renvoie une erreur 400 si le champ 'data' n'est pas un JSON valide"""
    invalid_data_movie = {
        "id_tmdb": 9999,
        "data": "invalid_json",
        "image_path": "/tElnmtQ6yz1PjN1kePNl8yMSb59.jpg",
        "poster_path": "/m0SbwFNCa9epW1X60deLqTHiP7x.jpg",
    }

    response = client.post('/movies', json=invalid_data_movie)
    assert response.status_code == 400

    error_response = response.json
    assert "error" in error_response
    assert error_response["error"] == "The 'data' field must be a JSON object or array"
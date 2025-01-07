import json

with open("app/db/fixtures/datas/films.json", "r") as file:
    data = json.load(file)

#
# ---- GET ----
#

def test_get_collection_returns_list(client):
    """Test que l'endpoint /user/<int:identifier>/collection renvoie une liste d'items"""
    admin_login = client.post(
        "/token",
        json={"mail": "admin@example.com", "password": "admin"},
    )
    admin_token = admin_login.json["token"]
    
    response = client.get(
        '/user/3/collection',
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    collection = response.json
    assert isinstance(collection, list)
    assert len(collection) > 0


def test_get_collection_contains_specific_item(client):
    """Test que l'endpoint /user/<int:identifier>/collection contient un item avec des informations spécifiques"""
    admin_login = client.post(
        "/token",
        json={"mail": "admin@example.com", "password": "admin"},
    )
    admin_token = admin_login.json["token"]
    
    response = client.get(
        '/user/3/collection',
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200

    collection = response.json
    specific_item = {
        "id": 1,
        "state": "Physique",
        "borrowed": True,
        "borrowed_at": "2025-01-01 00:00:00",
        "borrowed_by": "User 1",
        "favorite": True,
        "in_wishlist": True,
        "film": {
            "id": 1,
            "id_tmdb": 1241982,
            "data": "Film 1",
            "image_path": "/tElnmtQ6yz1PjN1kePNl8yMSb59.jpg",
            "poster_path": "/m0SbwFNCa9epW1X60deLqTHiP7x.jpg",
        },
    }

    assert any(
        item["id"] == specific_item["id"]
        and item["state"] == specific_item["state"]
        and item["borrowed"] == specific_item["borrowed"]
        and item["borrowed_at"] == specific_item["borrowed_at"]
        and item["borrowed_by"] == specific_item["borrowed_by"]
        and item["favorite"] == specific_item["favorite"]
        and item["in_wishlist"] == specific_item["in_wishlist"]
        and item["film"]["id"] == specific_item["film"]["id"]
        and item["film"]["id_tmdb"] == specific_item["film"]["id_tmdb"]
        and item["film"]["data"] == specific_item["film"]["data"]
        and item["film"]["image_path"] == specific_item["film"]["image_path"]
        and item["film"]["poster_path"] == specific_item["film"]["poster_path"]
        for item in collection
    )


def test_get_collection_with_good_param(client):
    admin_login = client.post(
        "/token",
        json={"mail": "admin@example.com", "password": "admin"},
    )
    admin_token = admin_login.json["token"]

    # Test with wishlist
    response = client.get(
        '/user/3/collection?wishlist=true',
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    collection = response.json
    assert all(item["in_wishlist"] == True for item in collection)

    # Test with favorite
    response = client.get(
        '/user/3/collection?favorite=false',
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    collection = response.json
    assert all(item["favorite"] == False for item in collection)

    # Test with state
    response = client.get(
        '/user/3/collection?state=Physique',
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    collection = response.json
    assert all(item["state"] == "Physique" for item in collection)

    # Test with borrowed
    response = client.get(
        '/user/3/collection?borrowed=false',
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    collection = response.json
    assert all(item["borrowed"] == False for item in collection)


def test_get_collection_with_invalid_param(client):
    admin_login = client.post(
        "/token",
        json={"mail": "admin@example.com", "password": "admin"},
    )
    admin_token = admin_login.json["token"]

    # Test with invalid wishlist
    response = client.get(
        '/user/3/collection?wishlist=invalid',
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 400
    assert response.json == {"error": "La valeur de wishlist doit être un booléen"}

    # Test with invalid state
    response = client.get(
        '/user/3/collection?state=InvalidState',
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 400
    assert response.json == {"error": "La valeur de state doit être 'Physique' ou 'Numérique'"}

    # Test with invalid borrowed
    response = client.get(
        '/user/3/collection?borrowed=true',
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    collection = response.json
    assert all(item["borrowed"] == True for item in collection)

    # Test with invalid favorite
    response = client.get(
        '/user/3/collection?favorite=invalid',
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 400
    assert response.json == {"error": "La valeur de favorite doit être un booléen"}


def test_get_collection_without_filters(client):
    admin_login = client.post(
        "/token",
        json={"mail": "admin@example.com", "password": "admin"},
    )
    admin_token = admin_login.json["token"]

    response = client.get(
        '/user/3/collection',
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    collection = response.json
    assert isinstance(collection, list)
    assert len(collection) > 0


def test_get_collection_with_no_matching_items(client):
    admin_login = client.post(
        "/token",
        json={"mail": "admin@example.com", "password": "admin"},
    )
    admin_token = admin_login.json["token"]

    response = client.get(
        '/user/3/collection?wishlist=true&borrowed=true&state=Numérique&favorite=true',
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 404
    assert response.json == {"error": "Aucun item trouvé"}


def test_get_collection_without_jwt(client):
    response = client.get('/user/3/collection')
    assert response.status_code == 401
    assert response.json == {"msg": "Missing Authorization Header"}


def test_get_collection_with_invalid_jwt(client):
    user_login = client.post(
        "/token",
        json={"mail": "unadmin@example.com", "password": "user"},
    )

    user_token = user_login.json["token"]

    response = client.get(
        '/user/3/collection',
        headers={"Authorization": f"Bearer {user_token}"}
    )

    assert response.status_code == 401
    assert response.json == {"error": "Non autorisé"}

#
# ---- POST ----
#

def test_create_item_returns_created_item(client):
    admin_login = client.post(
        "/token",
        json={"mail": "admin@example.com", "password": "admin"},
    )
    admin_token = admin_login.json["token"]

    response = client.post(
        '/user/3/collection',
        headers={"Authorization": f"Bearer {admin_token}"},
        json={
            "film_id": 2,
            "state": "Physique",
            "borrowed": False,
            "favorite": False,
            "in_wishlist": False,
        }
    )

    assert response.status_code == 201
    assert response.json == {"message": "Item ajouté avec succès"}
    
    response = client.get(
        '/user/3/collection',
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    collection = response.json
    assert any(item["film"]["id"] == 2 for item in collection)


def test_create_item_with_invalid_jwt(client):
    user_login = client.post(
        "/token",
        json={"mail": "unadmin@example.com", "password": "user"},
    )

    user_token = user_login.json["token"]

    response = client.post(
        '/user/3/collection',
        headers={"Authorization": f"Bearer {user_token}"},
        json={
            "film_id": 2,
            "state": "Physique",
            "borrowed": False,
            "favorite": False,
            "in_wishlist": False,
        }
    )

    assert response.status_code == 401
    assert response.json == {"error": "Non autorisé"}

#
# ---- PATCH ----
#


def test_patch_item(client):
    admin_login = client.post(
        "/token",
        json={"mail": "admin@example.com", "password": "admin"},
    )
    admin_token = admin_login.json["token"]

    item_data = {
        "film_id": 1,
        "state": "Physique",
        "borrowed": False,
        "favorite": False,
        "in_wishlist": False
    }
    response = client.post("/user/1/collection", json=item_data, headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 201
    item_id = client.get(
        "/user/1/collection",
        headers={"Authorization": f"Bearer {admin_token}"}
    ).json[0]["id"]

    update_data = {
        "borrowed": True,
        "favorite": True
    }
    response = client.patch(f"/user/1/collection/{item_id}", json=update_data, headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 200
    assert response.json["message"] == "Item mis à jour avec succès"

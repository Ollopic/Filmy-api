#
# ---- GET ----
#

def test_get_collection_returns_list(client):
    """Test que l'endpoint /collection renvoie une liste d'items"""
    user_login = client.post(
        "/token",
        json={"mail": "unadmin@example.com", "password": "user"},
    )
    user_token = user_login.json["token"]

    response = client.get(
        '/collection',
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 200
    collection = response.json
    assert isinstance(collection, list)
    assert len(collection) > 0


def test_get_collection_contains_specific_item(client):
    """Test que l'endpoint /collection contient un item avec des informations spécifiques"""
    user_login = client.post(
        "/token",
        json={"mail": "unadmin@example.com", "password": "user"},
    )
    user_token = user_login.json["token"]
    
    response = client.get(
        '/collection',
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 200

    collection = response.json
    specific_item = {
        "id": 1,
        "items_count": 2,
        "name": "Collection 1",
        "picture": None,
    }

    assert specific_item in collection


def test_get_wishlist(client):
    """Test que l'endpoint GET /collection/wishlist renvoie la wishlist de l'utilisateur"""
    user_login = client.post(
        "/token",
        json={"mail": "unadmin@example.com", "password": "user"},
    )
    user_token = user_login.json["token"]

    response = client.get(
        '/collection/wishlist',
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 200
    wishlist = response.json
    assert isinstance(wishlist, list)


#
# ---- POST ----
#
def test_create_collection(client):
    """Test que l'endpoint POST /collection crée une collection"""
    user_login = client.post(
        "/token",
        json={"mail": "unadmin@example.com", "password": "user"},
    )
    user_token = user_login.json["token"]

    response = client.post(
        '/collection',
        headers={"Authorization": f"Bearer {user_token}"},
        json={"name": "Nouvelle Collection", "picture": "image.png"},
    )
    assert response.status_code == 201
    assert response.json["message"] == "Collection créé avec succès"


def test_create_collection_duplicate_name(client):
    """Test que l'endpoint POST /collection renvoie une erreur pour un nom de collection en doublon"""
    user_login = client.post(
        "/token",
        json={"mail": "unadmin@example.com", "password": "user"},
    )
    user_token = user_login.json["token"]

    # Créer une première collection
    client.post(
        '/collection',
        headers={"Authorization": f"Bearer {user_token}"},
        json={"name": "Collection Duplicate", "picture": "image.png"},
    )

    # Tenter d'en créer une autre avec le même nom
    response = client.post(
        '/collection',
        headers={"Authorization": f"Bearer {user_token}"},
        json={"name": "Collection Duplicate", "picture": "image2.png"},
    )
    assert response.status_code == 409
    assert "Une collection avec ce nom existe déjà" in response.json["error"]


def test_create_item_in_collection(client):
    """Test que l'endpoint POST /collection/<id> ajoute un item dans une collection"""
    user_login = client.post(
        "/token",
        json={"mail": "unadmin@example.com", "password": "user"},
    )
    user_token = user_login.json["token"]

    response = client.post(
        '/collection/1',
        headers={"Authorization": f"Bearer {user_token}"},
        json={"film_id": 11, "state": "Physique"},
    )
    assert response.status_code == 201
    assert response.json["message"] == "Item de collection créé avec succès"


def test_create_item_wishlist(client):
    """Test que l'endpoint POST /collection/wishlist ajoute un item dans la wishlist"""
    user_login = client.post(
        "/token",
        json={"mail": "unadmin@example.com", "password": "user"},
    )
    user_token = user_login.json["token"]

    response = client.post(
        '/collection/wishlist',
        headers={"Authorization": f"Bearer {user_token}"},
        json={"film_id": 12},
    )
    assert response.status_code == 201
    assert response.json["message"] == "Item ajouté à la wishlist"


def test_create_item_wishlist_duplicate(client):
    """Test que l'endpoint POST /collection/wishlist renvoie une erreur pour un film déjà dans la wishlist"""
    user_login = client.post(
        "/token",
        json={"mail": "unadmin@example.com", "password": "user"},
    )
    user_token = user_login.json["token"]

    client.post(
        '/collection/wishlist',
        headers={"Authorization": f"Bearer {user_token}"},
        json={"film_id": 13},
    )

    response = client.post(
        '/collection/wishlist',
        headers={"Authorization": f"Bearer {user_token}"},
        json={"film_id": 13},
    )
    assert response.status_code == 400
    assert "Film déjà présent dans la wishlist" in response.json["error"]

#
# ---- PATCH ----
#

def test_update_collection(client):
    """Test que l'endpoint PATCH /collection/<id> met à jour une collection"""
    user_login = client.post(
        "/token",
        json={"mail": "unadmin@example.com", "password": "user"},
    )
    user_token = user_login.json["token"]

    response = client.patch(
        '/collection/1',
        headers={"Authorization": f"Bearer {user_token}"},
        json={"name": "Nom Modifié", "picture": "image_modifiee.png"},
    )
    assert response.status_code == 200
    assert response.json["message"] == "Collection modifié avec succès"

#
# ---- DELETE ----
#

def test_delete_item_in_collection(client):
    """Test que l'endpoint DELETE /collection/<id>/<film_id> supprime un item dans une collection"""
    user_login = client.post(
        "/token",
        json={"mail": "unadmin@example.com", "password": "user"},
    )
    user_token = user_login.json["token"]

    response = client.delete(
        '/collection/1/11',
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 200
    assert response.json["message"] == "Item de collection supprimé avec succès"

def test_delete_collection(client):
    """Test que l'endpoint DELETE /collection/<id> supprime une collection"""
    user_login = client.post(
        "/token",
        json={"mail": "unadmin@example.com", "password": "user"},
    )
    user_token = user_login.json["token"]

    response = client.delete(
        '/collection/1',
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 200
    assert response.json["message"] == "Collection supprimé avec succès"

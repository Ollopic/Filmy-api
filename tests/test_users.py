import base64

#
# ---- GET ----
#

def test_get_me(client):
    """Test que l'utilisateur connecté peut récupérer ses propres infos"""
    user_login = client.post(
        "/token",
        json={"mail": "admin@example.com", "password": "admin"},
    )

    user_token = user_login.json["token"]

    user_infos = client.get(
        "/user/me",
        headers={"Authorization": f"Bearer {user_token}"},
    )

    assert user_infos.status_code == 200
    assert user_infos.json == {
        "id": 1,
        "username": "admin",
        "mail": "admin@example.com",
        "is_admin": True,
        "profile_image": None,
    }


def test_get_user_as_user(client):
    """Test que l'utilisateur connecté peut récupérer ses propres infos"""
    user_login = client.post(
        "/token",
        json={"mail": "unadmin@example.com", "password": "user"},
    )

    user_token = user_login.json["token"]

    response = client.get("/user/2", headers={"Authorization": f"Bearer {user_token}"})

    assert response.status_code == 200
    assert response.json == {
        "id": 2,
        "username": "user",
        "mail": "unadmin@example.com",
        "is_admin": False,
        "profile_image": None,
    }


def test_get_user_as_admin(client):
    """Test que l'admin peut récupérer les infos d'un autre utilisateur"""
    admin_login = client.post(
        "/token",
        json={"mail": "admin@example.com", "password": "admin"},
    )

    admin_token = admin_login.json["token"]

    response = client.get("/user/2", headers={"Authorization": f"Bearer {admin_token}"})

    assert response.status_code == 200
    assert response.json == {
        "id": 2,
        "username": "user",
        "mail": "unadmin@example.com",
        "is_admin": False,
        "profile_image": None,
    }


def test_get_user_not_found(client):
    """Test de la gestion d'erreur d'un utilisateur inexistant"""
    admin_login = client.post(
        "/token",
        json={"mail": "admin@example.com", "password": "admin"},
    )

    admin_token = admin_login.json["token"]

    response = client.get("/user/999", headers={"Authorization": f"Bearer {admin_token}"})

    assert response.status_code == 404
    assert response.json == {"error": "Utilisateur introuvable"}


def test_get_user_unauthenticated(client):
    """Test de la gestion d'erreur d'un utilisateur non connecté"""
    response = client.get("/user/1")

    assert response.status_code == 401
    assert response.json == {"msg": "Missing Authorization Header"}


def test_get_user_unauthorized(client):
    """Test de la gestion d'erreur d'un utilisateur non autorisé (un utilisateur tente d'accéder à un autre utilisateur sans être admin)"""
    user_login = client.post(
        "/token",
        json={"mail": "unadmin@example.com", "password": "user"},
    )

    user_token = user_login.json["token"]

    response = client.get("/user/4", headers={"Authorization": f"Bearer {user_token}"})

    assert response.status_code == 401
    assert response.json == {"error": "Non autorisé"}


#
# ---- POST ----
#

def test_create_user_success(client):
    """Test de création d'un nouvel utilisateur"""
    response = client.post(
        "/user",
        json={
            "username": "newuser",
            "mail": "newuser@example.com",
            "password": "newuserPassword",
            "is_admin": False,
        },
    )

    assert response.status_code == 201
    assert response.json == {"message": "Utilisateur créé avec succès"}

    """Test que le mot de passe est bien hashé dans la base de données en tentant de se connecter"""
    response = client.post(
        "/token",
        json={"mail": "newuser@example.com", "password": "newuserPassword"},
    )

    assert response.status_code == 200
    assert "token" in response.json
    assert response.json["message"] == "Utilisateur connecté avec succès"


def test_create_user_email_exists(client):
    """Test de gestion d'erreur d'un email déjà existant"""
    response = client.post(
        "/user",
        json={
            "username": "existinguser",
            "mail": "admin@example.com",
            "password": "adminPassword",
            "is_admin": False,
        },
    )

    assert response.status_code == 409
    assert response.json == {"error": "Email déjà utilisé"}


#
# ---- PATCH ----
#

def test_update_user_success(client):
    """Test de mise à jour d'un utilisateur"""
    admin_login = client.post(
        "/token",
        json={"mail": "admin@example.com", "password": "admin"},
    )
    admin_token = admin_login.json["token"]
    
    image_path = "app/db/fixtures/datas/photo_profil.png"
    with open(image_path, "rb") as image_file:
        image_binary = image_file.read()
        image_base64 = base64.b64encode(image_binary).decode('utf-8')
    
    response = client.patch(
        "/user/2",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"username": "updateduser", "profile_image": image_base64},
    )

    assert response.status_code == 200
    assert response.json == {"message": "Utilisateur mis à jour avec succès"}

    updated_user = client.get("/user/2", headers={"Authorization": f"Bearer {admin_token}"})
    assert updated_user.json["username"] == "updateduser"
    assert updated_user.json["profile_image"] == image_base64


def test_update_user_not_found(client):
    """Test de gestion d'erreur d'un utilisateur inexistant"""
    admin_login = client.post(
        "/token",
        json={"mail": "admin@example.com", "password": "admin"},
    )
    admin_token = admin_login.json["token"]

    response = client.patch(
        "/user/999",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"username": "updateduser"},
    )

    assert response.status_code == 404
    assert response.json == {"error": "Utilisateur introuvable"}


def test_update_user_unauthorized(client):
    """Test de gestion d'erreur d'un utilisateur non autorisé (un utilisateur tente de mettre à jour un autre utilisateur sans être admin)"""
    user_login = client.post(
        "/token",
        json={"mail": "unadmin@example.com", "password": "user"},
    )
    user_token = user_login.json["token"]

    response = client.patch(
        "/user/4",
        headers={"Authorization": f"Bearer {user_token}"},
        json={"username": "unauthorizedupdate"},
    )

    assert response.status_code == 401
    assert response.json == {"error": "Non autorisé"}


#
# ---- DELETE ----
#

def test_delete_user_success_admin(client):
    """Test de suppression d'un utilisateur en tant qu'admin"""
    admin_login = client.post(
        "/token",
        json={"mail": "admin@example.com", "password": "admin"},
    )
    admin_token = admin_login.json["token"]

    response = client.delete(
        "/user/2",
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    assert response.status_code == 200
    assert response.json == {"message": "Utilisateur supprimé avec succès"}


def test_delete_user_success_user(client, reset_db):
    """Test de suppression de son propre compte en tant qu'utilisateur"""
    user_login = client.post(
        "/token",
        json={"mail": "unadmin@example.com", "password": "user"},
    )
    user_token = user_login.json["token"]

    response = client.delete(
        "/user/2",
        headers={"Authorization": f"Bearer {user_token}"},
    )

    assert response.status_code == 200
    assert response.json == {"message": "Utilisateur supprimé avec succès"}


def test_delete_user_not_found(client):
    """Test de gestion d'erreur d'un utilisateur inexistant"""
    admin_login = client.post(
        "/token",
        json={"mail": "admin@example.com", "password": "admin"},
    )
    admin_token = admin_login.json["token"]

    response = client.delete(
        "/user/999",
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    assert response.status_code == 404
    assert response.json == {"error": "Utilisateur introuvable"}


def test_delete_user_unauthorized(client, reset_db):
    """Test de gestion d'erreur d'un utilisateur non autorisé (un utilisateur tente de supprimer un autre utilisateur sans être admin)"""
    user_login = client.post(
        "/token",
        json={"mail": "unadmin@example.com", "password": "user"},
    )
    user_token = user_login.json["token"]

    response = client.delete(
        "/user/4",
        headers={"Authorization": f"Bearer {user_token}"},
    )

    assert response.status_code == 401
    assert response.json == {"error": "Non autorisé"}

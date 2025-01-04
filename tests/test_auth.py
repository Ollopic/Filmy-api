def test_login_user_success(client):
    """Test de connexion d'un utilisateur"""
    response = client.post(
        "/token",
        json={"mail": "admin@example.com", "password": "admin"},
    )

    assert response.status_code == 200
    assert "token" in response.json
    assert "token_expires_at" in response.json
    assert response.json["message"] == "User logged in successfully"


def test_login_user_invalid_password(client):
    """Test de connexion avec un mauvais mot de passe"""
    response = client.post(
        "/token",
        json={"mail": "admin@example.com", "password": "wrongpassword"},
    )

    assert response.status_code == 401
    assert response.json == {"error": "Invalid password"}


def test_login_user_not_found(client):
    """Test de connexion avec un utilisateur inexistant"""
    response = client.post(
        "/token",
        json={"mail": "nonexistent@example.com", "password": "password"},
    )

    assert response.status_code == 404
    assert response.json == {"error": "User not found"}

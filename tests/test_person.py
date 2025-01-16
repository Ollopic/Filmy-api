def test_get_popular_person(client):
    """Test que l'endpoint /person/popular renvoie des personnes populaires"""
    response = client.get('/person/popular')
    assert response.status_code == 200

    persons = response.json
    assert isinstance(persons, list)
    assert len(persons) > 0


def test_search_person(client):
    """Test que l'endpoint /person renvoie des personnes correspondant à un nom"""
    name = "Didier Bourdon"
    response = client.get(f'/person?name={name}')
    assert response.status_code == 200

    results = response.json
    assert "total_results" in results

    persons = results["persons"]
    assert isinstance(persons, list)
    assert len(persons) > 0

    for person in persons:
        assert name.lower() in person["name"].lower()
        

def test_get_person_by_id(client):
    """Test que l'endpoint /person/<int:id> renvoie bien les informations d'une personne"""
    response = client.get('/person/59031')
    assert response.status_code == 200

    person = response.json
    assert person["name"] == "Didier Bourdon"
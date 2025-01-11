from flask import request

from app.app import app
from app.db.database import db
from app.db.models import Person
from app.themoviedb.client import Client

tmdb_client = Client()


@app.route("/person", methods=["GET"])
def search_person():
    name = request.args.get("name")
    data = tmdb_client.get_person_by_name(name)["results"]

    result = [
        {
            "id_tmdb": person["id"],
            "name": person["name"],
            "profile_path": person["profile_path"],
            "known_for": person["known_for_department"],
        }
        for person in data
    ]

    return result, 200


@app.route("/person/<int:identifier>", methods=["GET"])
def get_person(identifier: int):
    person = Person.query.filter(Person.id_tmdb == identifier).first()
    if person is None or "birthday" not in person.data:
        person = tmdb_client.get_person_by_id(identifier)
        if person is None:
            return {"error": "Personne introuvable"}, 404

        new_person = Person(id_tmdb=person["id"], data=person)
        db.session.add(new_person)
        db.session.commit()
        return {
            "data": person,
        }, 200

    return {
        "data": person.data,
    }, 200


@app.route("/person/popular", methods=["GET"])
def get_popular_person():
    data = tmdb_client.get_popular_person()["results"]

    result = [
        {
            "id_tmdb": person["id"],
            "name": person["name"],
            "profile_path": person["profile_path"],
            "known_for": person["known_for_department"],
        }
        for person in data
    ]

    return result, 200

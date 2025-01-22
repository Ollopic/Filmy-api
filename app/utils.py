import bcrypt

from app.db.database import db
from app.db.models import CreditsFilm, Film, Person
from app.themoviedb.client import Client

tmdb_client = Client()


def hash_password(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")


def validate_boolean_param(param):
    """Helper function to validate boolean-like parameters."""
    return param in ["true", "false", "True", "False", "1", "0"]


def validate_state_param(state):
    """Helper function to validate state parameter."""
    return state in ["Physique", "Numérique"]


def search_movie_in_tmdb(identifier):
    movie_data = tmdb_client.get_movie_by_id(identifier)
    data_person = tmdb_client.get_movie_credits(identifier)

    # Get director
    director = None
    for person in data_person["crew"]:
        if person["job"] == "Director":
            director = person["name"]
    movie_data["director"] = director

    # Get trailer
    trailers = tmdb_client.get_movie_videos(identifier)["results"] or []
    for trailer in trailers:
        if trailer["site"].lower() == "youtube" and trailer["type"].lower() == "trailer":
            movie_data["trailer_key"] = trailer["key"]
            break

    if not trailers:
        movie_data["trailer_key"] = None

    # Get release dates FR
    release_dates = tmdb_client.get_movie_release_dates(identifier)["results"]
    for release_date in release_dates:
        if release_date["iso_3166_1"] == "FR":
            movie_data["age_restriction"] = release_date["release_dates"][0]["certification"]
            break

    return movie_data, data_person


def create_movie_if_not_exists(identifier):
    movie_data, data_person = search_movie_in_tmdb(identifier)

    movie = Film(
        id_tmdb=movie_data["id"],
        data=movie_data,
    )

    db.session.add(movie)
    db.session.commit()

    create_credits_if_not_exists(data_person, movie.id)

    # Retourner l'id de notre base de données
    return movie


def create_credits_if_not_exists(data_person, film_id):
    all_cast_ids = [person["id"] for person in data_person["cast"]]

    existing_people = db.session.query(Person).filter(Person.id_tmdb.in_(all_cast_ids)).all()
    existing_people_mapping = {person.id_tmdb: person.id for person in existing_people}

    missing_ids = set(all_cast_ids) - set(existing_people_mapping.keys())

    for person in data_person["cast"]:
        if person["id"] in missing_ids:
            new_person = Person(
                id_tmdb=person["id"],
                data=person,
            )
            db.session.add(new_person)
            db.session.flush()
            existing_people_mapping[person["id"]] = new_person.id

    for person in data_person["cast"]:
        local_person_id = existing_people_mapping[person["id"]]
        credits = CreditsFilm(
            person_id=local_person_id,
            character=person["character"],
            film_id=film_id,
        )
        db.session.add(credits)

    db.session.commit()

import bcrypt

from app.db.database import db
from app.db.models import CreditsFilm, Film, Person


def hash_password(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")


def create_movie_if_not_exists(data_movie):
    movie = Film(
        id_tmdb=data_movie["id_tmdb"],
        data=data_movie["data"],
        poster_path=data_movie["poster_path"],
        backdrop_path=data_movie["backdrop_path"],
    )

    db.session.add(movie)
    db.session.commit()
    return movie.id


def create_credits_if_not_exists(data_person, film_id):
    person_id_mapping = {}

    for person in data_person["cast"]:
        existing_person = db.session.query(Person).filter_by(id_tmdb=person["id"]).first()
        if not existing_person:
            new_person = Person(
                id_tmdb=person["id"],
                data=person,
            )
            db.session.add(new_person)
            db.session.flush()
            person_id_mapping[person["id"]] = new_person.id
        else:
            person_id_mapping[person["id"]] = existing_person.id

    for person in data_person["cast"]:
        local_person_id = person_id_mapping[person["id"]]
        credits = CreditsFilm(
            person_id=local_person_id,
            character=person["character"],
            film_id=film_id,
        )
        db.session.add(credits)

    db.session.commit()

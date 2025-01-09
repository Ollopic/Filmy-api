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
    )

    db.session.add(movie)
    db.session.commit()
    return movie.id


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

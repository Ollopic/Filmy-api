import json
import random

from faker import Faker

from app.app import app
from app.db.database import db
from app.db.models import Collection, CollectionItem, CreditsFilm, Film, Person, User
from app.utils import hash_password

fake = Faker()


def generate_test_data():
    with app.app_context():
        db.drop_all()
        db.create_all()

        admin_user = User(
            username="admin",
            mail="admin@example.com",
            password=hash_password("admin"),
            is_admin=True,
        )

        unadmin_user = User(
            username="user",
            mail="unadmin@example.com",
            password=hash_password("user"),
            is_admin=False,
        )

        db.session.add(admin_user)
        db.session.add(unadmin_user)

        # Générer des utilisateurs aléatoires
        users = []
        for _ in range(5):
            user = User(
                username=fake.user_name(),
                mail=fake.email(),
                password=hash_password(fake.password()),
                is_admin=fake.boolean(chance_of_getting_true=10),
            )
            users.append(user)
            db.session.add(user)

        with open("app/db/fixtures/datas/films.json", "r") as file:
            data = json.load(file)

        films = []
        film1 = Film(
            id_tmdb=1241982,
            data=data["film1"],
        )
        films.append(film1)
        db.session.add(film1)
        film2 = Film(
            id_tmdb=1034541,
            data=data["film2"],
        )
        films.append(film2)
        db.session.add(film2)
        film3 = Film(
            id_tmdb=114975,
            data=data["film3"],
        )
        films.append(film3)
        db.session.add(film3)
        film4 = Film(
            id_tmdb=912649,
            data=data["film4"],
        )
        films.append(film4)
        db.session.add(film4)
        film5 = Film(
            id_tmdb=558449,
            data=data["film5"],
        )
        films.append(film5)
        db.session.add(film5)

        film6 = Film(
            id_tmdb=1241982,
            data={"id": 1241982, "title": "Film 1", "poster_path": "/aLVkiINlIeCkcZIzb7XHzPYgO6L.jpg"},
        )
        films.append(film6)
        db.session.add(film6)

        film7 = Film(
            id_tmdb=1241983, data={"id": 1241983, "title": "Film 2", "poster_path": "/96FR5o2M8bshJBPy6yDah2E0oAa.jpg"}
        )
        films.append(film7)
        db.session.add(film7)

        with open("app/db/fixtures/datas/persons.json", "r") as file:
            data = json.load(file)

        persons = []
        person1 = Person(id_tmdb=1241982, data=data["person1"])
        persons.append(person1)
        db.session.add(person1)

        person2 = Person(id_tmdb=1034541, data=data["person2"])
        persons.append(person2)
        db.session.add(person2)

        person3 = Person(id_tmdb=114975, data=data["person3"])
        persons.append(person3)
        db.session.add(person3)

        person4 = Person(id_tmdb=912649, data=data["person4"])
        persons.append(person4)
        db.session.add(person4)

        person5 = Person(id_tmdb=558449, data=data["person5"])
        persons.append(person5)
        db.session.add(person5)

        # Ajout manuel de crédits
        credit1 = CreditsFilm(film_id=1, person_id=1, character="John Doe")
        credit2 = CreditsFilm(film_id=1, person_id=2, character="Jane Doe")
        db.session.add(credit1)
        db.session.add(credit2)

        # Générer des crédits
        for film in films:
            num_credits = random.randint(3, 7)
            for _ in range(num_credits):
                person = random.choice(persons)
                credit = CreditsFilm(film=film, person=person, character=fake.name())
                db.session.add(credit)

        collection1 = Collection(
            name="Collection 1",
            user_id=2,
        )

        db.session.add(collection1)

        item_true = CollectionItem(
            state="Physique",
            borrowed=True,
            borrowed_at="2025-01-01 00:00:00",
            borrowed_by="User 1",
            favorite=True,
            film_id=6,
            collection_id=1,
            user_id=2,
        )

        item_false = CollectionItem(
            state="Physique",
            borrowed=False,
            borrowed_at=None,
            borrowed_by=None,
            favorite=False,
            film_id=7,
            collection_id=1,
            user_id=2,
        )

        db.session.add(item_true)
        db.session.add(item_false)

        db.session.commit()
        print("Données de test générées avec succès !")


if __name__ == "__main__":
    generate_test_data()

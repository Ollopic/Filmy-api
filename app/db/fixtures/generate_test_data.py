import json
import random

from faker import Faker

from app.app import app
from app.db.database import db
from app.db.models import CollectionItem, CreditsFilm, Film, Person, User
from app.util import hash_password

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
        db.session.add(admin_user)

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
            image_path="/tElnmtQ6yz1PjN1kePNl8yMSb59.jpg",
            poster_path="/m0SbwFNCa9epW1X60deLqTHiP7x.jpg",
        )
        films.append(film1)
        db.session.add(film1)
        film2 = Film(
            id_tmdb=1034541,
            data=data["film2"],
            image_path="/2ndyL4HjM9JLMqBSgbyCM57aMWl.jpg",
            poster_path="/ju10W5gl3PPK3b7TjEmVOZap51I.jpg",
        )
        films.append(film2)
        db.session.add(film2)
        film3 = Film(
            id_tmdb=114975,
            data=data["film3"],
            image_path="/idoSsWF6oOlrMFBd966OUd0aB8g.jpg",
            poster_path="/ne83mYnmEBLhXnU8qawebKTA1nv.jpg",
        )
        films.append(film3)
        db.session.add(film3)
        film4 = Film(
            id_tmdb=912649,
            data=data["film4"],
            image_path="/3sh2UA2Q2l7fihgoj1LhFFPTlIM.jpg",
            poster_path="/fTGJWXuFDcRSIVPgQLbxziGquOC.jpg",
        )
        films.append(film4)
        db.session.add(film4)
        film5 = Film(
            id_tmdb=558449,
            data=data["film5"],
            image_path="/euYIwmwkmz95mnXvufEmbL6ovhZ.jpg",
            poster_path="/2cxhvwyEwRlysAmRH4iodkvo0z5.jpg",
        )
        films.append(film5)
        db.session.add(film5)

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

        # Générer des crédits
        for film in films:
            num_credits = random.randint(3, 7)
            for _ in range(num_credits):
                person = random.choice(persons)
                credit = CreditsFilm(film=film, person=person, character=fake.name())
                db.session.add(credit)
        # Générer des éléments de collection
        collection_items = []
        for user in users:
            num_items = random.randint(3, 7)
            for _ in range(num_items):
                item = CollectionItem(
                    state=random.choice(["Physique", "Numérique"]),
                    borrowed=fake.boolean(chance_of_getting_true=20),
                    borrowed_at=fake.date_time_between(start_date="-1y", end_date="now")
                    if fake.boolean(chance_of_getting_true=20)
                    else None,
                    borrowed_by=fake.name()
                    if fake.boolean(chance_of_getting_true=20)
                    else None,
                    favorite=fake.boolean(chance_of_getting_true=20),
                    in_wishlist=fake.boolean(chance_of_getting_true=20),
                    user=user,
                )
                collection_items.append(item)
                db.session.add(item)

        db.session.commit()
        print("Données de test générées avec succès !")


if __name__ == "__main__":
    generate_test_data()

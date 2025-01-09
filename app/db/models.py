from app.db.database import db


# Modèle pour la table 'Person'
class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_tmdb = db.Column(db.Integer, nullable=False)
    data = db.Column(db.JSON, nullable=False)

    # Relation ManyToOne avec 'Film' (via CreditsFilm)
    films = db.relationship("CreditsFilm", back_populates="person")


# Modèle pour la table 'Film'
class Film(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_tmdb = db.Column(db.Integer, nullable=False)
    data = db.Column(db.JSON, nullable=False)

    credits = db.relationship("CreditsFilm", back_populates="film")
    collection_items = db.relationship("CollectionItem", back_populates="film")


# Modèle pour la table 'CreditsFilm'
class CreditsFilm(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    film_id = db.Column(db.Integer, db.ForeignKey("film.id"), nullable=False)
    person_id = db.Column(db.Integer, db.ForeignKey("person.id"), nullable=False)
    character = db.Column(db.String, nullable=False)

    # Relations inverses
    film = db.relationship("Film", back_populates="credits")
    person = db.relationship("Person", back_populates="films")


# Modèle pour la table 'User'
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    mail = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    profile_image = db.Column(db.Text, nullable=True)

    # Relation OneToMany avec 'CollectionItem'
    collection = db.relationship("CollectionItem", back_populates="user")


# Modèle pour la table 'CollectionItem'
class CollectionItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.String, nullable=False)  # Par exemple, "Physique", "Numérique"
    borrowed = db.Column(db.Boolean, default=False)
    borrowed_at = db.Column(db.DateTime, nullable=True)
    borrowed_by = db.Column(db.String, nullable=True)  # Peut aussi être une relation si besoin
    favorite = db.Column(db.Boolean, default=False)
    in_wishlist = db.Column(db.Boolean, default=False)

    # Relations avec 'User' et 'Film'
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user = db.relationship("User", back_populates="collection")

    film_id = db.Column(db.Integer, db.ForeignKey("film.id"), nullable=False)
    film = db.relationship("Film", back_populates="collection_items")

from .app import db

# Modèle pour la table 'Person'
class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_tmdb = db.Column(db.Integer, nullable=False)
    data = db.Column(db.JSON, nullable=False)

    # Relation ManyToOne avec 'Film' (via CreditsFilm)
    films = db.relationship('CreditsFilm', back_populates='person')

# Modèle pour la table 'Film'
class Film(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_tmdb = db.Column(db.Integer, nullable=False)
    data = db.Column(db.JSON, nullable=False)
    image_path = db.Column(db.String, nullable=True)

    # Relation OneToMany avec 'CreditsFilm'
    credits = db.relationship('CreditsFilm', back_populates='film')

    # Relation ManyToMany avec 'CollectionItem'
    collection_items = db.relationship('CollectionItem', secondary='film_collection', back_populates='films')

# Modèle pour la table 'CreditsFilm'
class CreditsFilm(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    film_id = db.Column(db.Integer, db.ForeignKey('film.id'), nullable=False)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=False)
    character = db.Column(db.String, nullable=False)

    # Relations inverses
    film = db.relationship('Film', back_populates='credits')
    person = db.relationship('Person', back_populates='films')

# Modèle pour la table 'User'
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    mail = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    # Relation OneToMany avec 'CollectionItem'
    collection = db.relationship('CollectionItem', back_populates='user')

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
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', back_populates='collection')

    films = db.relationship('Film', secondary='film_collection', back_populates='collection_items')

# Table intermédiaire pour la relation ManyToMany entre 'Film' et 'CollectionItem'
film_collection = db.Table(
    'film_collection',
    db.Column('film_id', db.Integer, db.ForeignKey('film.id'), primary_key=True),
    db.Column('collection_item_id', db.Integer, db.ForeignKey('collection_item.id'), primary_key=True)
)
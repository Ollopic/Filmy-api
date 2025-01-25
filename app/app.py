from datetime import timedelta

from flask import Flask
from flask_admin import Admin
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate, upgrade
from sqlalchemy import inspect

from app.admin.view.collectionItemView import CollectionItemAdmin
from app.admin.view.collectionView import CollectionAdmin
from app.admin.view.movieView import FilmAdmin
from app.admin.view.personView import PersonAdmin
from app.admin.view.userView import UserAdmin
from app.config import (
    front_url,
    jwtAccessTokenExpiresConfig,
    jwtSecretKeyConfig,
    postgresqlConfig,
    secretKeyConfig,
    sqlalchemyTrackModificationsConfig,
)
from app.db.database import db
from app.db.models import Collection, CollectionItem, Film, Person, User
from app.utils import hash_password

app = Flask(__name__)

# Database #
app.config["SQLALCHEMY_DATABASE_URI"] = postgresqlConfig
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = sqlalchemyTrackModificationsConfig
db.init_app(app)
migrate = Migrate(app, db)

# Admin #
admin = Admin(app, name="Filmy Admin", template_mode="bootstrap4")
admin.add_view(CollectionAdmin(Collection, db.session))
admin.add_view(CollectionItemAdmin(CollectionItem, db.session))
admin.add_view(FilmAdmin(Film, db.session))
admin.add_view(PersonAdmin(Person, db.session))
admin.add_view(UserAdmin(User, db.session))

# Import routes
from app.routes import *  # noqa: E402, F403

app.config["JWT_SECRET_KEY"] = jwtSecretKeyConfig
app.config["SECRET_KEY"] = secretKeyConfig
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=int(jwtAccessTokenExpiresConfig))
jwt = JWTManager(app)

CORS(app, resources={r"/*": {"origins": front_url}})


def init_db():
    with app.app_context():
        print("Vérification de la base de données")
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        if not tables or (len(tables) == 1 and tables[0] == "alembic_version"):
            print("Base de données vide, création des tables")

            upgrade()
            print("Tables créés")
        else:
            print("Base de données déjà initialisée")

        admin = User.query.filter_by(username="admin").first()
        if not admin:
            print("Création de l'utilisateur admin")
            admin = User(username="admin", mail="admin@example.com", password=hash_password("admin"), is_admin=True)
            db.session.add(admin)
            db.session.commit()
            collection = Collection(name="Defaut", user_id=admin.id)
            db.session.add(collection)
            db.session.commit()
            print("Utilisateur admin créé")
        else:
            print("Utilisateur admin déjà créé")


with app.app_context():
    init_db()

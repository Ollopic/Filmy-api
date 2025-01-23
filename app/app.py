from datetime import timedelta

from flask import Flask
from flask_admin import Admin
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

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

if __name__ == "__main__":
    app.run()

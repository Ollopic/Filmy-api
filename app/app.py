from datetime import timedelta

from flask import Flask
from flask_admin import Admin
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

from app.admin.view.collectionView import CollectionAdmin
from app.admin.view.userView import UserAdmin
from app.config import (
    jwtAccessTokenExpiresConfig,
    jwtSecretKeyConfig,
    postgresqlConfig,
    secretKeyConfig,
    sqlalchemyTrackModificationsConfig,
)
from app.db.database import db
from app.db.models import Collection, User

app = Flask(__name__)

# Database #
app.config["SQLALCHEMY_DATABASE_URI"] = postgresqlConfig
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = sqlalchemyTrackModificationsConfig
db.init_app(app)
migrate = Migrate(app, db)

# Admin #
admin = Admin(app, name="Filmy Admin", template_mode="bootstrap4")
admin.add_view(UserAdmin(User, db.session))
admin.add_view(CollectionAdmin(Collection, db.session))

# Import routes
from app.routes import *  # noqa: E402, F403

app.config["JWT_SECRET_KEY"] = jwtSecretKeyConfig
app.config["SECRET_KEY"] = secretKeyConfig
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=jwtAccessTokenExpiresConfig)
jwt = JWTManager(app)

if __name__ == "__main__":
    app.run()

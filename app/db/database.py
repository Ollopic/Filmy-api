from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from app.config import postgresqlConfig, sqlalchemyTrackModificationsConfig

from app.app import app

app.config["SQLALCHEMY_DATABASE_URI"] = postgresqlConfig
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = sqlalchemyTrackModificationsConfig
db = SQLAlchemy(app)

migrate = Migrate(app, db)

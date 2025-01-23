import os

postgresqlConfig = os.getenv('POSTGRESQL_CONFIG', 'postgresql://postgres:postgres@db:5432/postgres')
sqlalchemyTrackModificationsConfig = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS', False)
MOVIE_DB_TOKEN = os.getenv('MOVIE_DB_TOKEN', 'your_token')
jwtSecretKeyConfig = os.getenv('JWT_SECRET_KEY', 'your_secret_key')
secretKeyConfig = os.getenv('SECRET_KEY', 'your_secret_key')
jwtAccessTokenExpiresConfig = os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 1)
front_url = os.getenv('FRONT_URL', 'http://localhost:8080')
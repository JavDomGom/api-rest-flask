import os

# Variables de la base de datos.
db_user = os.environ['DB_USER']
db_pass = os.environ['DB_PASS']
db_host = os.environ['DB_HOST']
db_name = os.environ['DB_NAME']
DB_URL = f'mysql+pymysql://{db_user}:{db_pass}@{db_host}/{db_name}'

# JWT.
jwt_secret_key = os.environ['JWT_SECRET_KEY']

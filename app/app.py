import datetime
from flask import Flask
from flask_jwt_extended import JWTManager
from gevent.pywsgi import WSGIServer
from sqlalchemy_utils import create_database, database_exists

import settings
from database import db
from routes.routes import blue_print

# Instancia de la app.
app = Flask(__name__)

# Configuración de la app.
app.config['SQLALCHEMY_DATABASE_URI'] = settings.DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = settings.jwt_secret_key
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(hours=12)

# Instancia de JWT.
jwt = JWTManager(app)

# Iniciamos SQLAlchemy.
db.init_app(app)

# Instanciamos las rutas
app.register_blueprint(blue_print)

# Creamos la base de datos.
with app.app_context():
    if not database_exists(settings.DB_URL):
        create_database(settings.DB_URL)
    db.create_all()


if __name__ == '__main__':
    """ Production enviroment. """
    http_server = WSGIServer(
        ('0.0.0.0', 5000),
        app,
        log=None
    )
    http_server.serve_forever()

    """ For  Debug/Development  enviroment comment  the two  previous lines and
    uncomment this line. """
    # app.run(host='0.0.0.0', debug=True, port=5000)

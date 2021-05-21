from flask import Flask
from gevent.pywsgi import WSGIServer
from sqlalchemy_utils import create_database, database_exists

from database import db

app = Flask(__name__)

# Bse de datos.
db_usuario = 'xxxxxxxxxx'
db_clave = 'xxxxxxxxxx'
db_host = 'xxxxxxxxxx'


@app.route('/', methods=['GET'])
def inicio():
    return '<h1>Flask API</h1>'


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

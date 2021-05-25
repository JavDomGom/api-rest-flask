import bcrypt
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required  # noqa: E501

from database import db
from models.models import Usuario, Pelicula
from schema.schemas import pelicula_schema, peliculas_schema

blue_print = Blueprint('app', __name__)


# Ruta de inicio.
@blue_print.route('/', methods=['GET'])
def inicio():
    return jsonify(respuesta='Rest API con Python, Flask y MySQL.')


# Ruta de registro de usuario.
@blue_print.route('/auth/registrar', methods=['POST'])
def registrar_usuario():
    try:
        # Obtener el usuario.
        usuario = request.json.get('usuario')
        # Obtener la clave.
        clave = request.json.get('clave')

        if not usuario or not clave:
            return jsonify(respuesta='Campos inválidos'), 400

        # Consultar la base de datos.
        existe_usuario = Usuario.query.filter_by(usuario=usuario).first()

        if existe_usuario:
            return jsonify(respuesta='El usuario ya existe'), 400

        # Ciframos clave de usuario.
        clave_cifrada = bcrypt.hashpw(clave.encode('utf-8'), bcrypt.gensalt())

        # Creamos el modelo a guardar en base de datos.
        nuevo_usuario = Usuario(usuario, clave_cifrada)

        db.session.add(nuevo_usuario)
        db.session.commit()

        return jsonify(respuesta='Usuario creado con éxito'), 201

    except Exception:
        return jsonify(respuesta='Error en la petición'), 500


# Ruta para iniciar sesión.
@blue_print.route('/auth/login', methods=['POST'])
def iniciar_sesion():
    try:
        # Obtener el usuario.
        usuario = request.json.get('usuario')
        # Obtener la clave.
        clave = request.json.get('clave')

        if not usuario or not clave:
            return jsonify(respuesta='Campos inválidos'), 400

        # Consultar la base de datos.
        existe_usuario = Usuario.query.filter_by(usuario=usuario).first()

        if not existe_usuario:
            return jsonify(respuesta='Usuario no encontrado'), 404

        es_clave_valida = bcrypt.checkpw(
            clave.encode('utf-8'),
            existe_usuario.clave.encode('utf-8')
        )

        # Validamos que las claves sean iguales.
        if es_clave_valida:
            access_token = create_access_token(identity=usuario)
            return jsonify(access_token=access_token), 200
        return jsonify(respuesta='Usuario o clave incorrectos'), 404

    except Exception:
        return jsonify(respuesta='Error en la petición'), 500


""" Rutas protegidas por JWT. """


# Ruta - Crear película.
@blue_print.route('/api/peliculas', methods=['POST'])
@jwt_required()
def crear_pelicula():
    try:
        nombre = request.json['nombre']
        estreno = request.json['estreno']
        director = request.json['director']
        reparto = request.json['reparto']
        genero = request.json['genero']
        sinopsis = request.json['sinopsis']

        nueva_pelicula = Pelicula(
            nombre, estreno, director, reparto, genero, sinopsis
        )

        db.session.add(nueva_pelicula)
        db.session.commit()

        return jsonify(respuesta='Película almacenada con éxito'), 201
    except Exception:
        return jsonify(respuesta='Error en petición'), 500


# Ruta - Obtener películas.
@blue_print.route('/api/peliculas', methods=['GET'])
@jwt_required()
def obtener_peliculas():
    try:
        peliculas = Pelicula.query.all()
        respuesta = peliculas_schema.dump(peliculas)
        return peliculas_schema.jsonify(respuesta), 200
    except Exception:
        return jsonify(respuesta='Error en petición'), 500


# Ruta - Obtener película por ID.
@blue_print.route('/api/peliculas/<int:id>', methods=['GET'])
@jwt_required()
def obtener_pelicula_por_id(id):
    try:
        pelicula = Pelicula.query.get(id)
        return pelicula_schema.jsonify(pelicula), 200
    except Exception:
        return jsonify(respuesta='Error en petición'), 500


# Ruta - Actualizar película.
@blue_print.route('/api/peliculas/<int:id>', methods=['PUT'])
@jwt_required()
def actualizar_pelicula(id):
    try:
        pelicula = Pelicula.query.get(id)

        if not pelicula:
            return jsonify(respuesta='Película no encontrada'), 404

        pelicula.nombre = request.json['nombre']
        pelicula.estreno = request.json['estreno']
        pelicula.director = request.json['director']
        pelicula.reparto = request.json['reparto']
        pelicula.genero = request.json['genero']
        pelicula.sinopsis = request.json['sinopsis']

        db.session.commit()

        return jsonify(respuesta='Película modificada con éxito'), 200
    except Exception:
        return jsonify(respuesta='Error en petición'), 500


# Ruta - Eliminar película por ID.
@blue_print.route('/api/peliculas/<int:id>', methods=['DELETE'])
@jwt_required()
def eliminar_pelicula_por_id(id):
    try:
        pelicula = Pelicula.query.get(id)

        if not pelicula:
            return jsonify(respuesta='Película no encontrada'), 404

        db.session.delete(pelicula)
        db.session.commit()

        return jsonify(respuesta='Película eliminada con éxito'), 200
    except Exception:
        return jsonify(respuesta='Error en petición'), 500

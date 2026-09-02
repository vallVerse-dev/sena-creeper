from flask import Flask, jsonify, request
from flask_cors import CORS
import pymysql
import os

MYSQL_PASSWORD = "Nosenose123"

app = Flask(__name__)
CORS(app)

def get_db_connection():
    return pymysql.connect(
        host=os.environ.get('DB_HOST', 'db'),
        database=os.environ.get('DB_NAME', 'sena_creeper'),
        user=os.environ.get('DB_USER', 'user'),
        password=MYSQL_PASSWORD,
        cursorclass=pymysql.cursors.DictCursor
    )

@app.route('/api/usuarios', methods=['POST'])
def crear_usuario():
    data = request.get_json()
    nombre = data.get('nombre')
    email = data.get('email')
    if not nombre or not email:
        return jsonify({"error": "Faltan campos nombre o email"}), 400
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO usuarios (nombre, email) VALUES (%s, %s)", (nombre, email))
        conn.commit()
        return jsonify({"mensaje": "Usuario creado exitosamente"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

@app.route('/api/usuarios', methods=['GET'])
def listar_usuarios():
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM usuarios")
            usuarios = cur.fetchall()
        return jsonify(usuarios), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

@app.route('/api/usuarios/<int:id>', methods=['GET'])
def obtener_usuario(id):
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM usuarios WHERE id = %s", (id,))
            usuario = cur.fetchone()
        if usuario:
            return jsonify(usuario), 200
        return jsonify({"error": "Usuario no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

@app.route('/api/usuarios/<int:id>', methods=['PUT'])
def actualizar_usuario(id):
    data = request.get_json()
    nombre = data.get('nombre')
    email = data.get('email')
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            if nombre:
                cur.execute("UPDATE usuarios SET nombre = %s WHERE id = %s", (nombre, id))
            if email:
                cur.execute("UPDATE usuarios SET email = %s WHERE id = %s", (email, id))
        conn.commit()
        return jsonify({"mensaje": "Usuario actualizado"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

@app.route('/api/usuarios/<int:id>', methods=['DELETE'])
def eliminar_usuario(id):
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM usuarios WHERE id = %s", (id,))
        conn.commit()
        return jsonify({"mensaje": "Usuario eliminado"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

if __name__ == '__main__':
    app.run(host=os.environ.get('HOST', '127.0.0.1'), port=5050, debug=False)

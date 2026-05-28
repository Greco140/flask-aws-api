from flask import Flask, jsonify, request
from models import db, Alumno, Profesor
from validators import validate_alumno, validate_profesor
import aws_services
import config

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]        = config.SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = config.SQLALCHEMY_TRACK_MODIFICATIONS

db.init_app(app)

with app.app_context():
    db.create_all()


# ═══════════════════════════════════════════════
#  ALUMNOS
# ═══════════════════════════════════════════════

@app.route("/alumnos", methods=["GET"])
def get_alumnos():
    alumnos = Alumno.query.all()
    return jsonify([a.to_dict() for a in alumnos]), 200


@app.route("/alumnos/<int:id>", methods=["GET"])
def get_alumno(id):
    alumno = Alumno.query.get(id)
    if alumno is None:
        return jsonify({"error": "Alumno no encontrado"}), 404
    return jsonify(alumno.to_dict()), 200


@app.route("/alumnos", methods=["POST"])
def create_alumno():
    try:
        data = request.get_json(force=True, silent=True)
        if data is None:
            return jsonify({"error": "JSON invalido"}), 400

        errors = validate_alumno(data)
        if errors:
            return jsonify({"errors": errors}), 400

        alumno = Alumno(
            nombres   = str(data["nombres"]).strip(),
            apellidos = str(data["apellidos"]).strip(),
            matricula = str(data["matricula"]).strip(),
            promedio  = float(data["promedio"]),
            password  = str(data["password"]).strip(),
        )
        db.session.add(alumno)
        db.session.commit()
        return jsonify(alumno.to_dict()), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@app.route("/alumnos/<int:id>", methods=["PUT"])
def update_alumno(id):
    try:
        alumno = Alumno.query.get(id)
        if alumno is None:
            return jsonify({"error": "Alumno no encontrado"}), 404

        data = request.get_json(force=True, silent=True)
        if data is None:
            return jsonify({"error": "JSON invalido"}), 400

        errors = validate_alumno(data)
        if errors:
            return jsonify({"errors": errors}), 400

        alumno.nombres   = str(data["nombres"]).strip()
        alumno.apellidos = str(data["apellidos"]).strip()
        alumno.matricula = str(data["matricula"]).strip()
        alumno.promedio  = float(data["promedio"])
        alumno.password  = str(data["password"]).strip()
        db.session.commit()
        return jsonify(alumno.to_dict()), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@app.route("/alumnos/<int:id>", methods=["DELETE"])
def delete_alumno(id):
    try:
        alumno = Alumno.query.get(id)
        if alumno is None:
            return jsonify({"error": "Alumno no encontrado"}), 404
        db.session.delete(alumno)
        db.session.commit()
        return jsonify({"message": "Alumno eliminado correctamente"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# ── Foto de perfil ─────────────────────────────

@app.route("/alumnos/<int:id>/fotoPerfil", methods=["POST"])
def upload_foto_perfil(id):
    try:
        alumno = Alumno.query.get(id)
        if alumno is None:
            return jsonify({"error": "Alumno no encontrado"}), 404

        if "foto" not in request.files:
            return jsonify({"error": "Se requiere el campo 'foto'"}), 400

        foto = request.files["foto"]
        url  = aws_services.upload_foto_perfil(foto, id, foto.filename)

        alumno.fotoPerfilUrl = url
        db.session.commit()

        return jsonify({"fotoPerfilUrl": url}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# ── Email (SNS) ────────────────────────────────

@app.route("/alumnos/<int:id>/email", methods=["POST"])
def send_email(id):
    try:
        alumno = Alumno.query.get(id)
        if alumno is None:
            return jsonify({"error": "Alumno no encontrado"}), 404

        aws_services.send_email_notification(alumno)
        return jsonify({"message": "Notificacion enviada correctamente"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ── Sesiones (DynamoDB) ────────────────────────

@app.route("/alumnos/<int:id>/session/login", methods=["POST"])
def session_login(id):
    try:
        alumno = Alumno.query.get(id)
        if alumno is None:
            return jsonify({"error": "Alumno no encontrado"}), 404

        data = request.get_json(force=True, silent=True)
        if data is None or "password" not in data:
            return jsonify({"error": "Se requiere el campo 'password'"}), 400

        if str(data["password"]) != str(alumno.password):
            return jsonify({"error": "Contrasena incorrecta"}), 400

        session_string = aws_services.crear_sesion(id)
        return jsonify({"sessionString": session_string}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/alumnos/<int:id>/session/verify", methods=["POST"])
def session_verify(id):
    try:
        alumno = Alumno.query.get(id)
        if alumno is None:
            return jsonify({"error": "Alumno no encontrado"}), 404

        data = request.get_json(force=True, silent=True)
        if data is None or "sessionString" not in data:
            return jsonify({"error": "Se requiere el campo 'sessionString'"}), 400

        valida = aws_services.verificar_sesion(id, data["sessionString"])
        if not valida:
            return jsonify({"error": "Sesion invalida o inactiva"}), 400

        return jsonify({"message": "Sesion valida"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/alumnos/<int:id>/session/logout", methods=["POST"])
def session_logout(id):
    try:
        alumno = Alumno.query.get(id)
        if alumno is None:
            return jsonify({"error": "Alumno no encontrado"}), 404

        data = request.get_json(force=True, silent=True)
        if data is None or "sessionString" not in data:
            return jsonify({"error": "Se requiere el campo 'sessionString'"}), 400

        cerrada = aws_services.cerrar_sesion(id, data["sessionString"])
        if not cerrada:
            return jsonify({"error": "Sesion no encontrada"}), 404

        return jsonify({"message": "Sesion cerrada correctamente"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ═══════════════════════════════════════════════
#  PROFESORES
# ═══════════════════════════════════════════════

@app.route("/profesores", methods=["GET"])
def get_profesores():
    profesores = Profesor.query.all()
    return jsonify([p.to_dict() for p in profesores]), 200


@app.route("/profesores/<int:id>", methods=["GET"])
def get_profesor(id):
    profesor = Profesor.query.get(id)
    if profesor is None:
        return jsonify({"error": "Profesor no encontrado"}), 404
    return jsonify(profesor.to_dict()), 200


@app.route("/profesores", methods=["POST"])
def create_profesor():
    try:
        data = request.get_json(force=True, silent=True)
        if data is None:
            return jsonify({"error": "JSON invalido"}), 400

        errors = validate_profesor(data)
        if errors:
            return jsonify({"errors": errors}), 400

        profesor = Profesor(
            numeroEmpleado = str(data["numeroEmpleado"]).strip(),
            nombres        = str(data["nombres"]).strip(),
            apellidos      = str(data["apellidos"]).strip(),
            horasClase     = int(float(data["horasClase"])),
        )
        db.session.add(profesor)
        db.session.commit()
        return jsonify(profesor.to_dict()), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@app.route("/profesores/<int:id>", methods=["PUT"])
def update_profesor(id):
    try:
        profesor = Profesor.query.get(id)
        if profesor is None:
            return jsonify({"error": "Profesor no encontrado"}), 404

        data = request.get_json(force=True, silent=True)
        if data is None:
            return jsonify({"error": "JSON invalido"}), 400

        errors = validate_profesor(data)
        if errors:
            return jsonify({"errors": errors}), 400

        profesor.numeroEmpleado = str(data["numeroEmpleado"]).strip()
        profesor.nombres        = str(data["nombres"]).strip()
        profesor.apellidos      = str(data["apellidos"]).strip()
        profesor.horasClase     = int(float(data["horasClase"]))
        db.session.commit()
        return jsonify(profesor.to_dict()), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@app.route("/profesores/<int:id>", methods=["DELETE"])
def delete_profesor(id):
    try:
        profesor = Profesor.query.get(id)
        if profesor is None:
            return jsonify({"error": "Profesor no encontrado"}), 404
        db.session.delete(profesor)
        db.session.commit()
        return jsonify({"message": "Profesor eliminado correctamente"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# ─── Entry point ────────────────────────────────
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=False)

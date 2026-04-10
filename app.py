from flask import Flask, jsonify, request
from validators import validate_alumno, validate_profesor
import uuid

app = Flask(__name__)

# ─────────────────────────────────────────────
#  In-memory storage
# ─────────────────────────────────────────────
alumnos = []
profesores = []


# ═══════════════════════════════════════════════
#  ALUMNOS ENDPOINTS
# ═══════════════════════════════════════════════

@app.route("/alumnos", methods=["GET"])
def get_alumnos():
    return jsonify(alumnos), 200


@app.route("/alumnos/<string:id>", methods=["GET"])
def get_alumno(id):
    alumno = next((a for a in alumnos if a["id"] == id), None)
    if alumno is None:
        return jsonify({"error": "Alumno no encontrado"}), 404
    return jsonify(alumno), 200


@app.route("/alumnos", methods=["POST"])
def create_alumno():
    try:
        data = request.get_json(force=True, silent=True)
        if data is None:
            return jsonify({"error": "El cuerpo de la petición debe ser JSON válido"}), 400

        errors = validate_alumno(data)
        if errors:
            return jsonify({"errors": errors}), 400

        alumno = {
            "id":        str(uuid.uuid4()),
            "nombres":   data["nombres"].strip(),
            "apellidos": data["apellidos"].strip(),
            "matricula": data["matricula"].strip(),
            "promedio":  float(data["promedio"]),
        }
        alumnos.append(alumno)
        return jsonify(alumno), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/alumnos/<string:id>", methods=["PUT"])
def update_alumno(id):
    try:
        alumno = next((a for a in alumnos if a["id"] == id), None)
        if alumno is None:
            return jsonify({"error": "Alumno no encontrado"}), 404

        data = request.get_json(force=True, silent=True)
        if data is None:
            return jsonify({"error": "El cuerpo de la petición debe ser JSON válido"}), 400

        errors = validate_alumno(data)
        if errors:
            return jsonify({"errors": errors}), 400

        alumno["nombres"]   = data["nombres"].strip()
        alumno["apellidos"] = data["apellidos"].strip()
        alumno["matricula"] = data["matricula"].strip()
        alumno["promedio"]  = float(data["promedio"])

        return jsonify(alumno), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/alumnos/<string:id>", methods=["DELETE"])
def delete_alumno(id):
    global alumnos
    alumno = next((a for a in alumnos if a["id"] == id), None)
    if alumno is None:
        return jsonify({"error": "Alumno no encontrado"}), 404
    alumnos = [a for a in alumnos if a["id"] != id]
    return jsonify({"message": "Alumno eliminado correctamente"}), 200


# ═══════════════════════════════════════════════
#  PROFESORES ENDPOINTS
# ═══════════════════════════════════════════════

@app.route("/profesores", methods=["GET"])
def get_profesores():
    return jsonify(profesores), 200


@app.route("/profesores/<string:id>", methods=["GET"])
def get_profesor(id):
    profesor = next((p for p in profesores if p["id"] == id), None)
    if profesor is None:
        return jsonify({"error": "Profesor no encontrado"}), 404
    return jsonify(profesor), 200


@app.route("/profesores", methods=["POST"])
def create_profesor():
    try:
        data = request.get_json(force=True, silent=True)
        if data is None:
            return jsonify({"error": "El cuerpo de la petición debe ser JSON válido"}), 400

        errors = validate_profesor(data)
        if errors:
            return jsonify({"errors": errors}), 400

        profesor = {
            "id":             str(uuid.uuid4()),
            "numeroEmpleado": data["numeroEmpleado"].strip(),
            "nombres":        data["nombres"].strip(),
            "apellidos":      data["apellidos"].strip(),
            "horasClase":     int(data["horasClase"]),
        }
        profesores.append(profesor)
        return jsonify(profesor), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/profesores/<string:id>", methods=["PUT"])
def update_profesor(id):
    try:
        profesor = next((p for p in profesores if p["id"] == id), None)
        if profesor is None:
            return jsonify({"error": "Profesor no encontrado"}), 404

        data = request.get_json(force=True, silent=True)
        if data is None:
            return jsonify({"error": "El cuerpo de la petición debe ser JSON válido"}), 400

        errors = validate_profesor(data)
        if errors:
            return jsonify({"errors": errors}), 400

        profesor["numeroEmpleado"] = data["numeroEmpleado"].strip()
        profesor["nombres"]        = data["nombres"].strip()
        profesor["apellidos"]      = data["apellidos"].strip()
        profesor["horasClase"]     = int(data["horasClase"])

        return jsonify(profesor), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/profesores/<string:id>", methods=["DELETE"])
def delete_profesor(id):
    global profesores
    profesor = next((p for p in profesores if p["id"] == id), None)
    if profesor is None:
        return jsonify({"error": "Profesor no encontrado"}), 404
    profesores = [p for p in profesores if p["id"] != id]
    return jsonify({"message": "Profesor eliminado correctamente"}), 200


# ─────────────────────────────────────────────
#  Entry point
# ─────────────────────────────────────────────
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=False)

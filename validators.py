"""
validators.py
Validaciones de campos para Alumno y Profesor.
Reglas:
  - Ningún campo puede estar vacío o ausente
  - Los tipos de dato deben ser correctos
  - promedio  → numérico, entre 0 y 10
  - horasClase → entero positivo
"""


def _is_blank(value) -> bool:
    """Devuelve True si el valor es None o una cadena vacía/solo espacios."""
    if value is None:
        return True
    if isinstance(value, str) and value.strip() == "":
        return True
    return False


def _is_numeric(value) -> bool:
    """Acepta int, float, o string que represente un número."""
    if isinstance(value, (int, float)):
        return True
    if isinstance(value, str):
        try:
            float(value)
            return True
        except ValueError:
            return False
    return False


def _is_integer_like(value) -> bool:
    """Acepta int o string que represente un entero (sin decimales)."""
    if isinstance(value, bool):
        return False
    if isinstance(value, int):
        return True
    if isinstance(value, str):
        try:
            int(value)
            return True
        except ValueError:
            return False
    return False


# ─────────────────────────────────────────────
#  Alumno: id, nombres, apellidos, matricula, promedio
# ─────────────────────────────────────────────
def validate_alumno(data: dict) -> list:
    errors = []
    required_str_fields = ["nombres", "apellidos", "matricula"]

    for field in required_str_fields:
        if field not in data:
            errors.append(f"El campo '{field}' es obligatorio.")
        elif not isinstance(data[field], str):
            errors.append(f"El campo '{field}' debe ser texto (string).")
        elif _is_blank(data[field]):
            errors.append(f"El campo '{field}' no puede estar vacío.")

    # promedio
    if "promedio" not in data:
        errors.append("El campo 'promedio' es obligatorio.")
    elif not _is_numeric(data["promedio"]):
        errors.append("El campo 'promedio' debe ser un número.")
    else:
        promedio = float(data["promedio"])
        if promedio < 0 or promedio > 10:
            errors.append("El campo 'promedio' debe estar entre 0 y 10.")

    return errors


# ─────────────────────────────────────────────
#  Profesor: id, numeroEmpleado, nombres, apellidos, horasClase
# ─────────────────────────────────────────────
def validate_profesor(data: dict) -> list:
    errors = []
    required_str_fields = ["numeroEmpleado", "nombres", "apellidos"]

    for field in required_str_fields:
        if field not in data:
            errors.append(f"El campo '{field}' es obligatorio.")
        elif not isinstance(data[field], str):
            errors.append(f"El campo '{field}' debe ser texto (string).")
        elif _is_blank(data[field]):
            errors.append(f"El campo '{field}' no puede estar vacío.")

    # horasClase
    if "horasClase" not in data:
        errors.append("El campo 'horasClase' es obligatorio.")
    elif not _is_integer_like(data["horasClase"]):
        errors.append("El campo 'horasClase' debe ser un número entero.")
    else:
        horas = int(data["horasClase"])
        if horas <= 0:
            errors.append("El campo 'horasClase' debe ser mayor a 0.")

    return errors

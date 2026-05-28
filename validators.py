def _is_blank(value):
    if value is None:
        return True
    if isinstance(value, str) and value.strip() == "":
        return True
    return False

def _is_numeric(value):
    if isinstance(value, (int, float)):
        return True
    if isinstance(value, str):
        try:
            float(value)
            return True
        except ValueError:
            return False
    return False

def _is_integer_like(value):
    if isinstance(value, bool):
        return False
    if isinstance(value, (int, float)):
        return True
    if isinstance(value, str):
        try:
            float(value)
            return True
        except ValueError:
            return False
    return False


def validate_alumno(data):
    errors = []

    for field in ["nombres", "apellidos", "matricula", "password"]:
        if field not in data:
            errors.append(f"El campo '{field}' es obligatorio.")
        elif data[field] is None:
            errors.append(f"El campo '{field}' no puede ser nulo.")
        elif isinstance(data[field], str) and data[field].strip() == "":
            errors.append(f"El campo '{field}' no puede estar vacio.")

    if "promedio" not in data:
        errors.append("El campo 'promedio' es obligatorio.")
    elif not _is_numeric(data["promedio"]):
        errors.append("El campo 'promedio' debe ser un numero.")
    else:
        if float(data["promedio"]) < 0 or float(data["promedio"]) > 10:
            errors.append("El campo 'promedio' debe estar entre 0 y 10.")

    return errors


def validate_profesor(data):
    errors = []

    for field in ["numeroEmpleado", "nombres", "apellidos"]:
        if field not in data:
            errors.append(f"El campo '{field}' es obligatorio.")
        elif data[field] is None:
            errors.append(f"El campo '{field}' no puede ser nulo.")
        elif isinstance(data[field], str) and data[field].strip() == "":
            errors.append(f"El campo '{field}' no puede estar vacio.")

    if "horasClase" not in data:
        errors.append("El campo 'horasClase' es obligatorio.")
    elif not _is_integer_like(data["horasClase"]):
        errors.append("El campo 'horasClase' debe ser un numero entero.")
    else:
        if int(float(data["horasClase"])) < 0:
            errors.append("El campo 'horasClase' no puede ser negativo.")

    return errors

# Flask REST API — AWS Cloud Foundations

API REST con Flask (Python) para las entidades **Alumno** y **Profesor**.
Almacenamiento en memoria (sin base de datos).

---

## Entidades

### Alumno
| Campo      | Tipo    | Reglas                     |
|------------|---------|----------------------------|
| id         | string  | Auto-generado (UUID)       |
| nombres    | string  | Requerido, no vacío        |
| apellidos  | string  | Requerido, no vacío        |
| matricula  | string  | Requerido, no vacío        |
| promedio   | float   | Requerido, entre 0 y 10   |

### Profesor
| Campo          | Tipo    | Reglas                  |
|----------------|---------|-------------------------|
| id             | string  | Auto-generado (UUID)    |
| numeroEmpleado | string  | Requerido, no vacío     |
| nombres        | string  | Requerido, no vacío     |
| apellidos      | string  | Requerido, no vacío     |
| horasClase     | int     | Requerido, entero > 0   |

---

## Endpoints

| Método | Ruta                  | Descripción               |
|--------|-----------------------|---------------------------|
| GET    | /alumnos              | Listar todos los alumnos  |
| GET    | /alumnos/{id}         | Obtener alumno por ID     |
| POST   | /alumnos              | Crear alumno              |
| PUT    | /alumnos/{id}         | Actualizar alumno         |
| DELETE | /alumnos/{id}         | Eliminar alumno           |
| GET    | /profesores           | Listar todos los profes   |
| GET    | /profesores/{id}      | Obtener profesor por ID   |
| POST   | /profesores           | Crear profesor            |
| PUT    | /profesores/{id}      | Actualizar profesor       |
| DELETE | /profesores/{id}      | Eliminar profesor         |

---

## Correr localmente

```bash
# 1. Clonar el repositorio
git clone https://github.com/Greco140/flask-aws-api.git
cd flask-aws-api

# 2. Crear entorno virtual
python3 -m venv venv
source venv/bin/activate        # Linux / Mac
# venv\Scripts\activate         # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Levantar en puerto 5000 (desarrollo)
python app.py
```

La API quedará disponible en `http://localhost:80`.

---

## Despliegue en EC2 (Amazon Linux 2023)

```bash
# En la instancia EC2 (como ec2-user):
sudo dnf update -y
sudo dnf install python3 python3-pip git -y

git clone https://github.com/Greco140/flask-aws-api.git
cd flask-aws-api

pip3 install -r requirements.txt

# Levantar en puerto 80 (requiere sudo)
sudo python3 app.py
```

---

## Códigos HTTP utilizados

| Código | Significado             |
|--------|-------------------------|
| 200    | OK                      |
| 201    | Created                 |
| 400    | Bad Request (validación)|
| 404    | Not Found               |
| 500    | Internal Server Error   |

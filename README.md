# Flask REST API v2 — AWS Cloud Foundations (Segunda Entrega)

API REST con Flask + SQLAlchemy + RDS + S3 + SNS + DynamoDB.

---

## Nuevos campos y endpoints

### Alumno
| Campo         | Tipo    | Notas                        |
|---------------|---------|------------------------------|
| id            | int     | Auto-generado por RDS        |
| nombres       | string  | Requerido                    |
| apellidos     | string  | Requerido                    |
| matricula     | string  | Requerido                    |
| promedio      | float   | 0–10                         |
| password      | string  | Requerido                    |
| fotoPerfilUrl | string  | URL pública de S3 (opcional) |

### Endpoints nuevos
| Método | Ruta                           | Descripción                  |
|--------|--------------------------------|------------------------------|
| POST   | /alumnos/{id}/fotoPerfil       | Sube imagen a S3             |
| POST   | /alumnos/{id}/email            | Envía notificación por SNS   |
| POST   | /alumnos/{id}/session/login    | Crea sesión en DynamoDB      |
| POST   | /alumnos/{id}/session/verify   | Verifica sesión activa       |
| POST   | /alumnos/{id}/session/logout   | Cierra sesión                |

---

## Despliegue en EC2

```bash
# 1. Clonar repositorio
git clone https://github.com/Greco140/flask-aws-api.git
cd flask-aws-api

# 2. Instalar dependencias
sudo pip3 install -r requirements.txt

# 3. Configurar variables de entorno
nano setup_env.sh   # Llenar con tus credenciales
source setup_env.sh

# 4. Levantar app
sudo -E python3 app.py
```

> ⚠️ Usar `sudo -E` para que las variables de entorno pasen al proceso con sudo.

---

## Variables de entorno requeridas

| Variable              | Descripción                          |
|-----------------------|--------------------------------------|
| DB_HOST               | Endpoint de RDS                      |
| DB_NAME               | Nombre de la base de datos           |
| DB_USER               | Usuario de RDS                       |
| DB_PASSWORD           | Contraseña de RDS                    |
| AWS_ACCESS_KEY_ID     | Del botón AWS Details en el lab      |
| AWS_SECRET_ACCESS_KEY | Del botón AWS Details en el lab      |
| AWS_SESSION_TOKEN     | Del botón AWS Details en el lab      |
| AWS_REGION            | us-east-1                            |
| S3_BUCKET_NAME        | Nombre del bucket S3                 |
| SNS_TOPIC_ARN         | ARN del topic SNS                    |
| DYNAMODB_TABLE        | sesiones-alumnos                     |

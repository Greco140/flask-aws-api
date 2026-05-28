import boto3
import uuid
import time
import secrets
import config


def _get_client(service):
    return boto3.client(
        service,
        region_name=config.AWS_REGION,
        aws_access_key_id=config.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY,
        aws_session_token=config.AWS_SESSION_TOKEN if config.AWS_SESSION_TOKEN else None,
    )


def _get_resource(service):
    return boto3.resource(
        service,
        region_name=config.AWS_REGION,
        aws_access_key_id=config.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY,
        aws_session_token=config.AWS_SESSION_TOKEN if config.AWS_SESSION_TOKEN else None,
    )


# ═══════════════════════════════════════════════
#  S3
# ═══════════════════════════════════════════════

def upload_foto_perfil(file_obj, alumno_id, filename):
    """
    Sube una imagen a S3 con ACL público.
    Devuelve la URL pública del archivo.
    """
    s3 = _get_client("s3")
    extension = filename.rsplit(".", 1)[-1] if "." in filename else "jpg"
    key = f"fotos-perfil/{alumno_id}/{uuid.uuid4()}.{extension}"

    s3.upload_fileobj(
        file_obj,
        config.S3_BUCKET_NAME,
        key,
        ExtraArgs={
            "ACL": "public-read",
            "ContentType": file_obj.content_type if hasattr(file_obj, "content_type") else "image/jpeg",
        },
    )

    url = f"https://{config.S3_BUCKET_NAME}.s3.amazonaws.com/{key}"
    return url


# ═══════════════════════════════════════════════
#  SNS
# ═══════════════════════════════════════════════

def send_email_notification(alumno):
    """
    Publica un mensaje en el topic SNS con la info del alumno.
    """
    sns = _get_client("sns")

    mensaje = (
        f"Notificación de calificaciones - SICEI\n\n"
        f"Nombre:    {alumno.nombres} {alumno.apellidos}\n"
        f"Matrícula: {alumno.matricula}\n"
        f"Promedio:  {alumno.promedio}\n"
    )

    sns.publish(
        TopicArn=config.SNS_TOPIC_ARN,
        Subject=f"Calificaciones de {alumno.nombres} {alumno.apellidos}",
        Message=mensaje,
    )


# ═══════════════════════════════════════════════
#  DynamoDB — sesiones-alumnos
# ═══════════════════════════════════════════════

def _get_table():
    dynamodb = _get_resource("dynamodb")
    return dynamodb.Table(config.DYNAMODB_TABLE)


def crear_sesion(alumno_id):
    """
    Crea una nueva sesión en DynamoDB.
    Devuelve el sessionString generado.
    """
    table = _get_table()
    session_id     = str(uuid.uuid4())
    session_string = secrets.token_hex(64)   # 128 chars hex
    fecha          = int(time.time())

    table.put_item(Item={
        "id":            session_id,
        "fecha":         fecha,
        "alumnoId":      alumno_id,
        "active":        True,
        "sessionString": session_string,
    })

    return session_string


def verificar_sesion(alumno_id, session_string):
    """
    Verifica si existe una sesión activa con el sessionString dado.
    Devuelve True si es válida y activa, False en otro caso.
    """
    table = _get_table()

    response = table.scan(
        FilterExpression="alumnoId = :aid AND sessionString = :ss AND #act = :true",
        ExpressionAttributeNames={"#act": "active"},
        ExpressionAttributeValues={
            ":aid": alumno_id,
            ":ss":  session_string,
            ":true": True,
        },
    )

    return len(response.get("Items", [])) > 0


def cerrar_sesion(alumno_id, session_string):
    """
    Pone active = false en la sesión correspondiente.
    Devuelve True si encontró y actualizó la sesión.
    """
    table = _get_table()

    response = table.scan(
        FilterExpression="alumnoId = :aid AND sessionString = :ss",
        ExpressionAttributeValues={
            ":aid": alumno_id,
            ":ss":  session_string,
        },
    )

    items = response.get("Items", [])
    if not items:
        return False

    for item in items:
        table.update_item(
            Key={"id": item["id"]},
            UpdateExpression="SET #act = :false",
            ExpressionAttributeNames={"#act": "active"},
            ExpressionAttributeValues={":false": False},
        )

    return True

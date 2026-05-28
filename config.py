import os

# ─── Base de datos (RDS MySQL) ───────────────────────────────
DB_HOST     = os.environ.get("DB_HOST", "localhost")
DB_PORT     = os.environ.get("DB_PORT", "3306")
DB_NAME     = os.environ.get("DB_NAME", "sicei")
DB_USER     = os.environ.get("DB_USER", "admin")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "password")

SQLALCHEMY_DATABASE_URI = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
SQLALCHEMY_TRACK_MODIFICATIONS = False

# ─── AWS ────────────────────────────────────────────────────
AWS_ACCESS_KEY_ID     = os.environ.get("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY", "")
AWS_SESSION_TOKEN     = os.environ.get("AWS_SESSION_TOKEN", "")
AWS_REGION            = os.environ.get("AWS_REGION", "us-east-1")

# ─── S3 ─────────────────────────────────────────────────────
S3_BUCKET_NAME = os.environ.get("S3_BUCKET_NAME", "sicei-fotos-perfil")

# ─── SNS ────────────────────────────────────────────────────
SNS_TOPIC_ARN = os.environ.get("SNS_TOPIC_ARN", "")

# ─── DynamoDB ───────────────────────────────────────────────
DYNAMODB_TABLE = os.environ.get("DYNAMODB_TABLE", "sesiones-alumnos")

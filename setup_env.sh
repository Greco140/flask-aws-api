#!/bin/bash
# setup_env.sh
# Ejecutar con: source setup_env.sh
# Llena estos valores con los datos de tu lab de AWS y RDS

# ─── Base de datos RDS ───────────────────────────────────────
export DB_HOST="TU-ENDPOINT-RDS.rds.amazonaws.com"
export DB_PORT="3306"
export DB_NAME="sicei"
export DB_USER="admin"
export DB_PASSWORD="TU-PASSWORD-RDS"

# ─── AWS Credentials (del botón AWS Details en el lab) ──────
export AWS_ACCESS_KEY_ID="TU-ACCESS-KEY"
export AWS_SECRET_ACCESS_KEY="TU-SECRET-KEY"
export AWS_SESSION_TOKEN="TU-SESSION-TOKEN"
export AWS_REGION="us-east-1"

# ─── S3 ─────────────────────────────────────────────────────
export S3_BUCKET_NAME="sicei-fotos-perfil"

# ─── SNS ────────────────────────────────────────────────────
export SNS_TOPIC_ARN="arn:aws:sns:us-east-1:TU-ACCOUNT-ID:sicei-notificaciones"

# ─── DynamoDB ───────────────────────────────────────────────
export DYNAMODB_TABLE="sesiones-alumnos"

echo "Variables de entorno configuradas correctamente."

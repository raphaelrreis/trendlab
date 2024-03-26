#!/bin/bash

# Substituir os valores das variáveis abaixo conforme sua configuração local e da conta AWS
AWS_REGION="us-east-1"
SECRET_NAME="dev/sangiorgio-api/secrets"

# Configurações locais para PostgreSQL em container
DB_HOST="localhost"
DB_PORT="5432"
DB_USERNAME="sangiorgio_user"
DB_PASSWORD="root"

# Configurações AWS e SQS (ATENCAO:Substitua pelos seus valores reais)
AWS_ACCESS_KEY="sua_chave_de_acesso"
AWS_SECRET_KEY="sua_chave_secreta"
SQS_PARTIAL_PAYMENTS_URL="url_da_sua_fila_de_pagamentos_parciais"
SQS_FULL_PAYMENTS_URL="url_da_sua_fila_de_pagamentos_completos"
SQS_EXCESS_PAYMENTS_URL="url_da_sua_fila_de_excessos_de_pagamento"

# Configuração das variáveis de ambiente locais
export DB_HOST=$DB_HOST
export DB_PORT=$DB_PORT
export DB_USERNAME=$DB_USERNAME
export DB_PASSWORD=$DB_PASSWORD
export AWS_REGION=$AWS_REGION
export AWS_ACCESS_KEY=$AWS_ACCESS_KEY
export AWS_SECRET_KEY=$AWS_SECRET_KEY
export SQS_PARTIAL_PAYMENTS_URL=$SQS_PARTIAL_PAYMENTS_URL
export SQS_FULL_PAYMENTS_URL=$SQS_FULL_PAYMENTS_URL
export SQS_EXCESS_PAYMENTS_URL=$SQS_EXCESS_PAYMENTS_URL

# Preparando a string do secret para AWS Secrets Manager
SECRET_STRING=$(cat <<EOF
{
  "DB_HOST": "$DB_HOST",
  "DB_PORT": "$DB_PORT",
  "DB_USERNAME": "$DB_USERNAME",
  "DB_PASSWORD": "$DB_PASSWORD",
  "AWS_ACCESS_KEY": "$AWS_ACCESS_KEY",
  "AWS_SECRET_KEY": "$AWS_SECRET_KEY",
  "SQS_PARTIAL_PAYMENTS_URL": "$SQS_PARTIAL_PAYMENTS_URL",
  "SQS_FULL_PAYMENTS_URL": "$SQS_FULL_PAYMENTS_URL",
  "SQS_EXCESS_PAYMENTS_URL": "$SQS_EXCESS_PAYMENTS_URL"
}
EOF
)

# Atualizar o segredo no AWS Secrets Manager
aws secretsmanager create-secret --name $SECRET_NAME \
                                 --secret-string "$SECRET_STRING" \
                                 --region $AWS_REGION || \
aws secretsmanager update-secret --secret-id $SECRET_NAME \
                                 --secret-string "$SECRET_STRING" \
                                 --region $AWS_REGION

echo "Configuração local e AWS Secrets Manager concluída."

#!/bin/bash

echo "Configurando permissões de execução para o Gradle Wrapper..."
chmod +x ./gradlew

echo "Configurando permissões de execução para o script..."
chmod +x start.sh

echo "Permissões configuradas com sucesso."

echo "Subindo o serviço de banco de dados..."
docker-compose up -d db

if [ $? -eq 0 ]; then
    echo "Serviço de banco de dados subiu com sucesso."
else
    echo "Falha ao subir o serviço de banco de dados."
    exit 1
fi

echo "Iniciando a aplicação Spring Boot..."
./gradlew bootRun

echo "Aplicação e serviços estão rodando."

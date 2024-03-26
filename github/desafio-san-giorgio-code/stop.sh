#!/bin/bash

chmod +x stop.sh

echo "Parando o serviço de banco de dados e removendo o container..."
docker-compose down

echo "Serviços parados e containers removidos."

@echo off
SETLOCAL EnableDelayedExpansion


SET POSTGRES_DB=sangiorgio_db
SET POSTGRES_USER=sangiorgio_user
SET POSTGRES_PASSWORD=root

echo Subindo o serviço de banco de dados...
docker-compose up -d db

IF %ERRORLEVEL% NEQ 0 (
    echo Falha ao subir o serviço de banco de dados.
    exit /b 1
)

echo Iniciando a aplicação Spring Boot...
call gradlew bootRun

echo Aplicação e serviços estão rodando.

:end
@echo on
ENDLOCAL

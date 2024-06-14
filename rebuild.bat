@echo off

if "%1" == "" (
    echo Usage: %0 [container_name^|all]
    exit /b 1
)

if "%1" == "all" (
    docker-compose stop backend frontend
    docker-compose down backend frontend
    docker-compose up --build -d backend frontend
    exit /b 0
)

set "container_name=%1"


findstr /C:"container_name: %container_name%" docker-compose.yml >nul
if %errorlevel% neq 0 (
    echo Container '%container_name%' not found in docker-compose.yml
    exit /b 1
)

docker-compose stop %container_name%
docker-compose down %container_name%
docker-compose up --build -d %container_name%
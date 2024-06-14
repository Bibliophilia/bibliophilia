@echo off

for /f "tokens=*" %%i in ('docker ps -aq') do (
    docker stop %%i >nul
    docker rm %%i >nul
)
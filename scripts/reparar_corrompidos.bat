@echo off
:: Verifica se está sendo executado como administrador
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo Reexecutando como administrador...
    powershell -Command "Start-Process '%~f0' -Verb runAs"
    exit /b
)

title LIMPEZA DE CORROMPIDOS
color 0A

echo =====================================
echo    LIMPEZA DE CORROMPIDOS
echo =====================================
echo.
echo.

sfc /scannow

echo.
echo Verificação concluída.
pause

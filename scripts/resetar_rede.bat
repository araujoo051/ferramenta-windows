@echo off
title Reset de Rede - VPN FortiClient
color 0A

echo [0] Verificando permissões de administrador...
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo [1] Solicitando permissao de administrador...
    PowerShell -Command "Start-Process -FilePath '%~f0' -Verb RunAs"
    exit /b
)

echo [10] Acesso de administrador concedido.

echo [20] Limpando cache DNS...
ipconfig /flushdns

echo [40] Liberando IP atual...
ipconfig /release

echo [50] Renovando IP...
ipconfig /renew

echo [70] Resetando Winsock...
netsh winsock reset

echo [85] Resetando a pilha de IP...
netsh int ip reset

echo [100] Reset de rede concluído com sucesso.
echo Reinicie o computador para aplicar as alterações.

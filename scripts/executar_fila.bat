@echo off
title Manutencao Completa do Windows
color 0a

echo ======================================
echo     INICIANDO MANUTENCAO COMPLETA
echo ======================================
echo.

echo [10] Limpando Disco...
call "%~dp0\limpeza_disco.bat"

echo [30] Limpando Arquivos Temporarios...
call "%~dp0\limpeza_temps.bat"

echo [60] Reparando Arquivos Corrompidos...
call "%~dp0\reparar_corrompidos.bat"

echo [80] Resetando Rede...
call "%~dp0\resetar_rede.bat"

echo [100] Testando Rede...
call "%~dp0\teste_rede.bat"

echo.
echo ======================================
echo  Todas as tarefas foram executadas!
echo ======================================
echo.
pause
exit

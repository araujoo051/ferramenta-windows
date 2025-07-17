@echo off
echo [0] Iniciando limpeza...
timeout /t 1 >nul

echo [20] Limpando %TEMP%
del /q /f /s "%TEMP%\*" >nul 2>&1
timeout /t 1 >nul

echo [50] Limpando C:\Windows\Temp
del /q /f /s "C:\Windows\Temp\*" >nul 2>&1
timeout /t 1 >nul

echo [100] Limpeza concluída.

@echo off
echo [0] Iniciando limpeza de sistema...

echo [10] Limpando arquivos temporários do usuário...

:: Remove arquivos, exceto da subpasta _MEI*
for %%f in ("%TEMP%\*.*") do (
    del /f /q "%%f" >nul 2>&1
)

:: Remove subpastas, exceto as que começam com _MEI
for /d %%d in ("%TEMP%\*") do (
    echo %%~nxd | findstr /b /i "_MEI" >nul
    if errorlevel 1 rd /s /q "%%d" >nul 2>&1
)

echo [20] Limpeza TEMP concluída.

echo [40] Limpando Downloads do usuário...
del /q /f "%USERPROFILE%\Downloads\*" >nul 2>&1
echo [60] Downloads limpos.

echo [70] Esvaziando lixeira do usuário...
PowerShell -Command "Clear-RecycleBin -Force -ErrorAction SilentlyContinue"
echo [90] Lixeira limpa.

echo [100] Limpeza finalizada.

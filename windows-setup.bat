@echo off
REM ============================================================
REM  Curso Python con Pokemon - Instalador para Windows
REM
REM  HAZ DOBLE CLIC EN ESTE FICHERO.
REM
REM  Pedira permisos de administrador (necesarios para instalar
REM  WSL2 + Ubuntu) y lanzara el resto del proceso.
REM ============================================================
echo.
echo  Lanzando el instalador (acepta el aviso de administrador)...
echo.
powershell -NoProfile -ExecutionPolicy Bypass -Command "Start-Process powershell -Verb RunAs -ArgumentList '-NoProfile -ExecutionPolicy Bypass -File \"%~dp0scripts\windows-setup.ps1\"'"
echo.
echo  Si se abrio otra ventana azul, sigue ahi las instrucciones.
echo  Ya puedes cerrar esta.
echo.
pause

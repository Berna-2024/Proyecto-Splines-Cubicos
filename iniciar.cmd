@echo off
setlocal
cd /d "%~dp0"
where py >nul 2>&1
if errorlevel 1 (
    python spline_cubico.py
) else (
    py -3 spline_cubico.py
)
if errorlevel 1 (
    echo.
    echo No se pudo iniciar. Comprueba que Python 3.10 o posterior incluya Tcl/Tk.
    pause
)

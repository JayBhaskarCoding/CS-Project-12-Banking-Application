@echo off
title Banking App Launcher
color 0B

echo =======================================================
echo        Bank Application - Initial Setup
echo =======================================================
echo.
echo Checking and installing required python libraries...
echo (If they are already installed the program will run instantly)
echo.

pip install customtkinter mysql-connector-python pillow >nul 2>&1
color 0B

echo.
echo ================================================================================================
echo                                    Libraries are ready! 
echo.
echo     IMPORTANT: Please Make Sure MySQL is running in XAMPP or any other software you're using
echo ================================================================================================
echo.
echo Launching the application...

python database.py
python main.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo =======================================================
    echo ERROR: The application crashed or failed to start.
    echo Please read the error message above.
    echo =======================================================
    pause
)


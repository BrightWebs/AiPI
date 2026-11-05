@echo off
cd /d "%~dp0"
py -3 AIPI_Bridge_Assistant.py
if errorlevel 1 (
  echo.
  echo Could not launch the app. Install Python 3 from https://www.python.org/downloads/windows/
  pause
)

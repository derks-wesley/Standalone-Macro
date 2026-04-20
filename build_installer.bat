@echo off
setlocal

REM Build Windows executable + installer
where py >nul 2>nul
if errorlevel 1 (
  echo [ERROR] Python launcher (py.exe) niet gevonden.
  exit /b 1
)

if not exist .venv (
  py -m venv .venv
)

call .venv\Scripts\activate.bat
if errorlevel 1 exit /b 1

python -m pip install --upgrade pip
pip install -r requirements.txt pyinstaller
if errorlevel 1 exit /b 1

pyinstaller --noconfirm --clean --windowed --name StandaloneMacro macro_app.py
if errorlevel 1 exit /b 1

set ISCC_PATH=C:\Program Files (x86)\Inno Setup 6\ISCC.exe
if not exist "%ISCC_PATH%" (
  echo [WARNING] Inno Setup niet gevonden. EXE staat in dist\StandaloneMacro\
  exit /b 0
)

"%ISCC_PATH%" installer\StandaloneMacro.iss
if errorlevel 1 exit /b 1

echo Klaar. Installer staat in installer\output\
endlocal

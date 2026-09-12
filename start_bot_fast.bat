@echo off
rem ============================================================
rem  start_bot_fast.bat - Run the bot on Windows (fast mode)
rem  NO library installation - libraries are already installed
rem  Uses .venv python if present, otherwise system python
rem  Ctrl+C     = real stop (no hidden restart)
rem  Before start, any leftover bot instance is terminated
rem  automatically (prevents Telegram Conflict error)
rem ============================================================
setlocal EnableExtensions
cd /d "%~dp0"

echo ==============================================
echo    Telegram Bot - Fast Start (no installs)
echo ==============================================
echo.

rem ---------- 1) find a python launcher ----------
set "PY="
py -3 -V >nul 2>&1 && set "PY=py -3"
if not defined PY (
    python -V >nul 2>&1 && set "PY=python"
)
if not defined PY goto :nopython

rem ---------- 2) pick interpreter ----------
rem prefer the existing virtual environment (libs live there)
if exist ".venv\Scripts\python.exe" goto :usevenv

rem resolve the REAL python.exe full path from the launcher
rem (full path = one token = safe to quote even with spaces)
set "VPY="
for /f "tokens=*" %%i in ('%PY% -c "import sys; print(sys.executable)"') do set "VPY=%%i"
if not defined VPY goto :nopython
echo [1/4] Using system python
goto :vercheck

:usevenv
set "VPY=%~dp0.venv\Scripts\python.exe"
echo [1/4] Using virtual environment python

:vercheck
"%VPY%" -V > "%TEMP%\bot_ver.txt" 2>&1
set /p PYVER=<"%TEMP%\bot_ver.txt"
echo       %PYVER%

rem quick sanity check: the bot libraries are importable
"%VPY%" -c "import aiogram, aiosqlite, dotenv" >nul 2>&1
if errorlevel 1 goto :nolibs
echo [2/4] Libraries OK

rem ---------- 3) .env ----------
if not exist ".env" (
    if exist ".env.example" (
        copy /y ".env.example" ".env" >nul
    )
)

rem generate empty secret keys automatically via helper
"%VPY%" "_env_setup.py" >nul 2>&1

set "NEEDSETUP=0"
findstr /C:"AA_your_bot_token_here" ".env" >nul 2>&1 && set "NEEDSETUP=1"
findstr /C:"ADMIN_USER_ID=123456789" ".env" >nul 2>&1 && set "NEEDSETUP=1"

if not "%NEEDSETUP%"=="1" goto :envready

echo [3/4] One manual step - only once ever:
echo       Notepad will open .env - edit ONLY these 2 lines:
echo         TELEGRAM_BOT_TOKEN = your token from @BotFather
echo         ADMIN_USER_ID      = your Telegram number (from @userinfobot)
echo       Then save with Ctrl+S and close Notepad.
echo.
notepad .env

findstr /C:"AA_your_bot_token_here" ".env" >nul 2>&1
if not errorlevel 1 goto :envbad
findstr /C:"ADMIN_USER_ID=123456789" ".env" >nul 2>&1
if not errorlevel 1 goto :envbad
echo [3/4] Settings ready
goto :runstage

:envbad
echo [X] Values are still default - edit .env then run this file again.
pause
exit /b 1

:envready
echo [3/4] Settings ready

rem ---------- 3b) kill leftover bot instances ----------
rem (two instances with one token = Telegram Conflict error)
echo Checking for leftover bot instances...
powershell -NoProfile -Command "Get-CimInstance Win32_Process -Filter 'Name like ''python%%''' | Where-Object { $_.CommandLine -like '*bot.py*' } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force }" >nul 2>&1
timeout /t 4 /nobreak >nul

rem ---------- 4) run bot ----------
echo [4/4] Starting bot... To stop: press Ctrl+C or close this window
echo.
set /a RESTARTS=0

:runloop
"%VPY%" bot.py
set "RC=%errorlevel%"
if "%RC%"=="0" goto :stoppedclean
set /a RESTARTS+=1
echo.
echo [%date% %time%] Bot crashed (code %RC%) - restarting in 5 seconds...
if %RESTARTS% GEQ 5 (
    echo Bot crashed 5 times in a row - check the errors above.
    echo Press any key to try again, or close this window to stop.
    pause >nul
    set /a RESTARTS=0
)
timeout /t 5 /nobreak >nul
goto :runloop

:stoppedclean
echo.
echo Bot stopped cleanly (you pressed Ctrl+C). You can close this window.
pause
exit /b 0

:nopython
echo [X] Python not found.
echo     Install Python 3.11+ from python.org
echo     and enable "Add python.exe to PATH",
echo     then run this file again.
echo.
pause
exit /b 1

:nolibs
echo [X] Bot libraries not found in this python:
echo       %PYVER%
echo     Fix - choose ONE:
echo       1) run start_bot.bat once (it creates .venv and installs)
echo       2) or install manually into this python:
echo          "%VPY%" -m pip install -r requirements.txt
echo.
pause
exit /b 1

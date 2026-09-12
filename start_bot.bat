@echo off
rem ============================================================
rem  start_bot.bat - Run the bot on Windows fully automatically
rem  First run : venv + libraries + .env keys + start
rem  Later runs: start directly (auto-restart on crash only)
rem  Ctrl+C    = real stop (no hidden restart)
rem  Before start, any leftover bot instance is terminated
rem  automatically (prevents Telegram Conflict error)
rem ============================================================
setlocal EnableExtensions
cd /d "%~dp0"

echo ==============================================
echo    Telegram Bot - Auto Setup and Run
echo ==============================================
echo.

rem ---------- 1) find python ----------
set "PY="
py -3 -V >nul 2>&1 && set "PY=py -3"
if not defined PY (
    python -V >nul 2>&1 && set "PY=python"
)
if not defined PY (
    echo [X] Python not found.
    echo     Install Python 3.11+ from python.org
    echo     and enable "Add python.exe to PATH",
    echo     then run this file again.
    echo.
    pause
    exit /b 1
)
for /f "tokens=*" %%v in ('%PY% -V 2^>^&1') do set "PYVER=%%v"
echo [1/5] Python: %PYVER%

rem ---------- 2) virtual environment ----------
if not exist ".venv\Scripts\python.exe" (
    echo [2/5] First run: creating virtual environment...
    %PY% -m venv .venv
    if errorlevel 1 goto :venvfail
) else (
    echo [2/5] Virtual environment OK
)
set "VPY=%~dp0.venv\Scripts\python.exe"

rem ---------- 3) libraries ----------
if not exist ".venv\installed.ok" (
    echo [3/5] First run: installing libraries - takes a few minutes...
    "%VPY%" -m pip install --upgrade pip --quiet
    "%VPY%" -m pip install -r requirements.txt
    if errorlevel 1 (
        echo [X] Library install failed - check internet and run again.
        pause
        exit /b 1
    )
    type nul > ".venv\installed.ok"
) else (
    echo [3/5] Libraries OK
)

rem ---------- 4) .env ----------
if not exist ".env" (
    copy /y ".env.example" ".env" >nul
)

rem generate empty secret keys automatically via helper
"%VPY%" "_env_setup.py" >nul 2>&1

set "NEEDSETUP=0"
findstr /C:"AA_your_bot_token_here" ".env" >nul 2>&1 && set "NEEDSETUP=1"
findstr /C:"ADMIN_USER_ID=123456789" ".env" >nul 2>&1 && set "NEEDSETUP=1"

if not "%NEEDSETUP%"=="1" goto :envready

echo [4/5] One manual step - only once ever:
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
echo [4/5] Settings ready
goto :runstage

:envbad
echo [X] Values are still default - edit .env then run this file again.
pause
exit /b 1

:envready
echo [4/5] Settings ready

rem ---------- 4b) kill leftover bot instances ----------
rem (two instances with one token = Telegram Conflict error)
echo Checking for leftover bot instances...
powershell -NoProfile -Command "Get-CimInstance Win32_Process -Filter 'Name like ''python%%''' | Where-Object { $_.CommandLine -like '*bot.py*' } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force }" >nul 2>&1
timeout /t 4 /nobreak >nul

rem ---------- 5) run bot ----------
echo [5/5] Starting bot... To stop: press Ctrl+C or close this window
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

:venvfail
echo [X] Failed to create virtual environment.
pause
exit /b 1

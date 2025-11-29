@echo off
REM Batch script to set up MongoDB on D drive
REM Run this script as Administrator

echo Setting up MongoDB on D drive...

REM Check if D drive exists
if not exist D:\ (
    echo ERROR: D drive not found!
    pause
    exit /b 1
)

REM Create MongoDB directories on D drive
echo.
echo Creating directories on D drive...
if not exist "D:\mongodb\data" mkdir "D:\mongodb\data"
if not exist "D:\mongodb\log" mkdir "D:\mongodb\log"

echo.
echo Directories created:
echo   D:\mongodb\data
echo   D:\mongodb\log

REM Copy configuration file if it exists
if exist "mongod.conf" (
    copy /Y "mongod.conf" "D:\mongodb\mongod.conf" >nul
    echo.
    echo Configuration file copied to D:\mongodb\mongod.conf
)

echo.
echo MongoDB setup complete!
echo.
echo Next steps:
echo   1. Make sure MongoDB is installed
echo   2. Update your MongoDB service to use the new config:
echo      mongod --config "D:\mongodb\mongod.conf" --install
echo   3. Start the MongoDB service:
echo      net start MongoDB
echo.
echo Connection URI: mongodb://127.0.0.1:27017/
echo.
pause


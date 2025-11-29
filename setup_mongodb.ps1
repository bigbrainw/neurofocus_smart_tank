# PowerShell script to set up MongoDB on D drive
# Run this script as Administrator

Write-Host "Setting up MongoDB on D drive..." -ForegroundColor Green

# Check if running as Administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Host "ERROR: This script must be run as Administrator!" -ForegroundColor Red
    Write-Host "Right-click PowerShell and select 'Run as Administrator'" -ForegroundColor Yellow
    exit 1
}

# MongoDB directories on D drive
$mongodbBase = "D:\mongodb"
$dataDir = "$mongodbBase\data"
$logDir = "$mongodbBase\log"
$configFile = "$mongodbBase\mongod.conf"

# Create directories
Write-Host "`nCreating directories on D drive..." -ForegroundColor Cyan
if (-not (Test-Path $dataDir)) {
    New-Item -ItemType Directory -Path $dataDir -Force | Out-Null
    Write-Host "  Created: $dataDir" -ForegroundColor Green
} else {
    Write-Host "  Already exists: $dataDir" -ForegroundColor Yellow
}

if (-not (Test-Path $logDir)) {
    New-Item -ItemType Directory -Path $logDir -Force | Out-Null
    Write-Host "  Created: $logDir" -ForegroundColor Green
} else {
    Write-Host "  Already exists: $logDir" -ForegroundColor Yellow
}

# Copy configuration file
Write-Host "`nSetting up MongoDB configuration..." -ForegroundColor Cyan
if (Test-Path "mongod.conf") {
    Copy-Item "mongod.conf" -Destination $configFile -Force
    Write-Host "  Configuration file copied to: $configFile" -ForegroundColor Green
} else {
    Write-Host "  WARNING: mongod.conf not found in current directory" -ForegroundColor Yellow
}

# Check if MongoDB is installed
Write-Host "`nChecking MongoDB installation..." -ForegroundColor Cyan
$mongodbPath = Get-Command mongod -ErrorAction SilentlyContinue
if ($mongodbPath) {
    $mongodbBin = Split-Path $mongodbPath.Source -Parent
    Write-Host "  MongoDB found at: $mongodbBin" -ForegroundColor Green
    
    # Check if MongoDB service exists
    $service = Get-Service -Name "MongoDB" -ErrorAction SilentlyContinue
    if ($service) {
        Write-Host "`nMongoDB service found. Stopping service..." -ForegroundColor Cyan
        Stop-Service -Name "MongoDB" -Force -ErrorAction SilentlyContinue
        
        Write-Host "`nTo update MongoDB service to use D drive:" -ForegroundColor Yellow
        Write-Host "  1. Run: sc delete MongoDB" -ForegroundColor White
        Write-Host "  2. Run: mongod --config `"$configFile`" --install" -ForegroundColor White
        Write-Host "  3. Run: Start-Service MongoDB" -ForegroundColor White
    } else {
        Write-Host "`nInstalling MongoDB as Windows Service..." -ForegroundColor Cyan
        & mongod --config $configFile --install
        if ($LASTEXITCODE -eq 0) {
            Write-Host "  MongoDB service installed successfully!" -ForegroundColor Green
            Write-Host "`nStarting MongoDB service..." -ForegroundColor Cyan
            Start-Service -Name "MongoDB"
            Write-Host "  MongoDB service started!" -ForegroundColor Green
        } else {
            Write-Host "  ERROR: Failed to install MongoDB service" -ForegroundColor Red
        }
    }
} else {
    Write-Host "  MongoDB not found in PATH" -ForegroundColor Red
    Write-Host "`nPlease install MongoDB first:" -ForegroundColor Yellow
    Write-Host "  1. Download from: https://www.mongodb.com/try/download/community" -ForegroundColor White
    Write-Host "  2. Install MongoDB Community Edition" -ForegroundColor White
    Write-Host "  3. Add MongoDB bin directory to PATH" -ForegroundColor White
    Write-Host "  4. Run this script again" -ForegroundColor White
}

Write-Host "`nSetup complete!" -ForegroundColor Green
Write-Host "`nMongoDB Configuration:" -ForegroundColor Cyan
Write-Host "  Data directory: $dataDir" -ForegroundColor White
Write-Host "  Log directory: $logDir" -ForegroundColor White
Write-Host "  Config file: $configFile" -ForegroundColor White
Write-Host "  Connection URI: mongodb://127.0.0.1:27017/" -ForegroundColor White


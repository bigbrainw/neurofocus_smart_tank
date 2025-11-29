# MongoDB Setup on D Drive

This guide will help you set up MongoDB to store data on your D drive.

## Prerequisites

- Windows operating system
- Administrator privileges
- MongoDB Community Edition installed
- D drive available on your system

## Quick Setup

### Option 1: PowerShell Script (Recommended)

1. Open PowerShell as Administrator:
   - Right-click on PowerShell
   - Select "Run as Administrator"

2. Navigate to the project directory:
   ```powershell
   cd C:\Users\elija\Program\neurofocus_smart_tank
   ```

3. Run the setup script:
   ```powershell
   .\setup_mongodb.ps1
   ```

The script will:
- Create necessary directories on D drive (`D:\mongodb\data` and `D:\mongodb\log`)
- Copy the MongoDB configuration file
- Install MongoDB as a Windows service (if MongoDB is installed)
- Start the MongoDB service

### Option 2: Batch Script

1. Open Command Prompt as Administrator

2. Navigate to the project directory:
   ```cmd
   cd C:\Users\elija\Program\neurofocus_smart_tank
   ```

3. Run the batch script:
   ```cmd
   setup_mongodb.bat
   ```

### Option 3: Manual Setup

1. **Create directories on D drive:**
   ```cmd
   mkdir D:\mongodb\data
   mkdir D:\mongodb\log
   ```

2. **Copy the configuration file:**
   ```cmd
   copy mongod.conf D:\mongodb\mongod.conf
   ```

3. **Install MongoDB service:**
   ```cmd
   mongod --config D:\mongodb\mongod.conf --install
   ```

4. **Start MongoDB service:**
   ```cmd
   net start MongoDB
   ```

## Verify Installation

1. **Check if MongoDB is running:**
   ```powershell
   Get-Service MongoDB
   ```

2. **Test connection:**
   ```cmd
   mongosh mongodb://127.0.0.1:27017/
   ```

3. **Check data directory:**
   ```powershell
   dir D:\mongodb\data
   ```

## Configuration Details

The MongoDB configuration (`mongod.conf`) is set to:
- **Data directory**: `D:\mongodb\data`
- **Log directory**: `D:\mongodb\log`
- **Port**: `27017`
- **Bind IP**: `127.0.0.1` (localhost only)

## Troubleshooting

### MongoDB Service Won't Start

1. Check the log file:
   ```powershell
   Get-Content D:\mongodb\log\mongod.log -Tail 50
   ```

2. Verify directories exist and have proper permissions:
   ```powershell
   Test-Path D:\mongodb\data
   Test-Path D:\mongodb\log
   ```

3. Check if port 27017 is available:
   ```powershell
   netstat -an | findstr 27017
   ```

### Permission Issues

If you encounter permission errors:
1. Right-click on `D:\mongodb` folder
2. Select "Properties" → "Security"
3. Click "Edit" and add your user with "Full control"
4. Apply to all subfolders

### MongoDB Not Found

If the script says MongoDB is not found:
1. Download MongoDB Community Edition: https://www.mongodb.com/try/download/community
2. Install MongoDB
3. Add MongoDB bin directory to PATH:
   - Usually: `C:\Program Files\MongoDB\Server\7.0\bin`
   - Add to System Environment Variables → Path
4. Restart PowerShell/Command Prompt
5. Run the setup script again

## Starting/Stopping MongoDB

### Start MongoDB Service:
```powershell
Start-Service MongoDB
```

### Stop MongoDB Service:
```powershell
Stop-Service MongoDB
```

### Restart MongoDB Service:
```powershell
Restart-Service MongoDB
```

## Uninstalling MongoDB Service

If you need to remove the MongoDB service:
```cmd
sc delete MongoDB
```

## Connection String

Once MongoDB is running, use this connection string in your `.env` file:
```
MONGODB_URI=mongodb://127.0.0.1:27017/
```

## Next Steps

After MongoDB is set up:
1. Update your `.env` file with the MongoDB connection string
2. Run `python test_server.py` to verify the connection
3. Start using the MCP server!


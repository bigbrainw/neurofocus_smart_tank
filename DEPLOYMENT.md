# Deployment Guide for Dedalus Labs

This guide will help you deploy the NeuroFocus Smart Tank MCP server on Dedalus Labs.

## Prerequisites

1. A GitHub account
2. A MongoDB instance (MongoDB Atlas recommended for cloud hosting)
3. A Dedalus Labs account

## Step 1: Prepare Your MongoDB Database

1. Create a MongoDB instance:
   - Option A: Use MongoDB Atlas (cloud): https://www.mongodb.com/cloud/atlas
   - Option B: Use a local MongoDB instance
   - Option C: Use any MongoDB hosting service

2. Get your MongoDB connection string:
   - Format: `mongodb://username:password@host:port/` or
   - Format: `mongodb+srv://username:password@cluster.mongodb.net/` (for Atlas)

## Step 2: Push Code to GitHub

1. Initialize git repository (if not already done):
```bash
git init
git add .
git commit -m "Initial commit: MCP server for MongoDB"
```

2. Create a new repository on GitHub

3. Push your code:
```bash
git remote add origin https://github.com/yourusername/neurofocus-smart-tank.git
git branch -M main
git push -u origin main
```

## Step 3: Deploy on Dedalus Labs

1. Log in to Dedalus Labs: https://www.dedaluslabs.ai/

2. Connect your GitHub repository:
   - Click "New Deployment" or "Connect Repository"
   - Select your `neurofocus-smart-tank` repository
   - Authorize GitHub access if prompted

3. Configure environment variables:
   - `MONGODB_URI`: Your MongoDB connection string
   - `MONGODB_DATABASE`: Database name (default: `neurofocus_db`)

4. Deploy:
   - Review the configuration
   - Click "Deploy"
   - Wait for the deployment to complete

5. Get your MCP endpoint:
   - Once deployed, Dedalus Labs will provide you with an MCP endpoint URL
   - Save this URL for connecting your AI clients

## Step 4: Connect to AI Clients

### Claude Desktop

1. Open Claude Desktop settings
2. Add MCP server configuration:
```json
{
  "mcpServers": {
    "neurofocus-smart-tank": {
      "url": "your-dedalus-labs-endpoint-url",
      "transport": "sse"
    }
  }
}
```

### VS Code with MCP Extension

1. Install the MCP extension
2. Configure the server endpoint in settings
3. Use the provided endpoint URL from Dedalus Labs

## Troubleshooting

### Connection Issues
- Verify MongoDB connection string is correct
- Check if MongoDB allows connections from Dedalus Labs IPs
- For MongoDB Atlas, ensure your IP is whitelisted or use 0.0.0.0/0

### Deployment Failures
- Check logs in Dedalus Labs dashboard
- Verify all environment variables are set
- Ensure Python 3.11 is available (check `dedalus.yaml`)

### File Upload Issues
- Verify file paths are accessible
- Check file size limits (GridFS handles large files)
- Ensure file types are supported (PDF, JSON, DOCX)

## Monitoring

- Use Dedalus Labs dashboard to monitor:
  - Server health
  - Request logs
  - Resource usage
  - Error rates

## Updates

To update your deployment:
1. Push changes to GitHub
2. Dedalus Labs will automatically redeploy (if auto-deploy is enabled)
3. Or manually trigger redeployment from the dashboard


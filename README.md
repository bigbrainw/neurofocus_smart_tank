# NeuroFocus Smart Tank - MCP Server

An MCP (Model Context Protocol) server that stores and retrieves data from MongoDB, supporting multiple data types including PDF, JSON, and Word documents.

## Features

- **MongoDB Integration**: Store and retrieve data from MongoDB
- **Multiple File Types**: Support for PDF, JSON, and Word (.docx) documents
- **GridFS Support**: Handle large files efficiently using MongoDB GridFS
- **MCP Protocol**: Full MCP server implementation for AI client interactions
- **Content Extraction**: Automatically extracts text and metadata from documents
- **Search Capabilities**: Full-text search across document content and metadata

## Quick Start

### Local Development

1. **Set up MongoDB on D drive** (Windows):
   ```powershell
   # Run PowerShell as Administrator
   .\setup_mongodb.ps1
   ```
   Or use the batch script:
   ```cmd
   # Run Command Prompt as Administrator
   setup_mongodb.bat
   ```
   
   This will:
   - Create `D:\mongodb\data` for database files
   - Create `D:\mongodb\log` for log files
   - Configure MongoDB to use D drive

2. **Start MongoDB** (if not running as a service):
   ```bash
   mongod --config D:\mongodb\mongod.conf
   ```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
# On Windows PowerShell:
Copy-Item env.example .env
# Edit .env with your MongoDB connection string (default: mongodb://127.0.0.1:27017/)
```

5. Run the server:
```bash
python server.py
```

### Testing

Run the test script to verify functionality:
```bash
python test_server.py
```

## Deployment on Dedalus Labs

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions.

Quick steps:
1. Push this repository to GitHub
2. Connect your repository to Dedalus Labs
3. Set the required environment variables in Dedalus Labs dashboard
4. Deploy the server

## Environment Variables

- `MONGODB_URI`: MongoDB connection string (required)
  - Example: `mongodb://localhost:27017/`
  - Example (Atlas): `mongodb+srv://user:pass@cluster.mongodb.net/`
- `MONGODB_DATABASE`: Database name (default: `neurofocus_db`)
- `PORT`: Server port (default: 8000)

## MCP Tools

The server provides the following MCP tools:

### `store_document`
Store a document (PDF, JSON, or Word) in MongoDB.

**Parameters:**
- `file_path` (required): Path to the file to store
- `metadata` (optional): Additional metadata to store with the document

**Returns:** Document ID and metadata

### `retrieve_document`
Retrieve a document by ID from MongoDB.

**Parameters:**
- `document_id` (required): The MongoDB document ID
- `include_content` (optional): Whether to include file content (default: true)

**Returns:** Document metadata and content

### `search_documents`
Search documents by metadata or content.

**Parameters:**
- `query` (optional): Search query string
- `file_type` (optional): Filter by file type (pdf, json, docx)
- `limit` (optional): Maximum number of results (default: 10)

**Returns:** List of matching documents

### `delete_document`
Delete a document by ID from MongoDB.

**Parameters:**
- `document_id` (required): The MongoDB document ID to delete

**Returns:** Success confirmation

### `list_documents`
List all documents with optional filtering.

**Parameters:**
- `file_type` (optional): Filter by file type
- `limit` (optional): Maximum number of results (default: 50)
- `skip` (optional): Number of results to skip (default: 0)

**Returns:** List of documents with pagination info

## Supported File Types

- **PDF** (`.pdf`): Extracts text content and PDF metadata
- **JSON** (`.json`): Parses JSON and extracts structured data
- **Word Documents** (`.docx`, `.doc`): Extracts text from paragraphs and tables, plus document properties

## Project Structure

```
.
├── server.py              # Main MCP server implementation
├── file_handlers.py       # File type handlers (PDF, JSON, Word)
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker configuration
├── dedalus.yaml          # Dedalus Labs deployment config
├── mongod.conf           # MongoDB configuration (D drive)
├── setup_mongodb.ps1     # PowerShell setup script for MongoDB
├── setup_mongodb.bat     # Batch setup script for MongoDB
├── test_server.py        # Test script
├── example_usage.py      # Usage examples
├── README.md             # This file
├── DEPLOYMENT.md         # Deployment guide
└── MONGODB_SETUP.md      # MongoDB setup guide
```

## License

MIT License - feel free to use and modify as needed.


#!/usr/bin/env python3
"""
MCP Server for MongoDB with support for multiple file types.
"""
import asyncio
import os
import json
from typing import Any, Optional
from dotenv import load_dotenv
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
from pymongo import MongoClient
from gridfs import GridFS
from bson import ObjectId

from file_handlers import PDFHandler, JSONHandler, WordHandler

# Load environment variables
load_dotenv()

# MongoDB configuration
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
MONGODB_DATABASE = os.getenv("MONGODB_DATABASE", "neurofocus_db")

# Initialize MongoDB client
client = MongoClient(MONGODB_URI)
db = client[MONGODB_DATABASE]
fs = GridFS(db)

# File handlers
file_handlers = {
    "pdf": PDFHandler(),
    "json": JSONHandler(),
    "docx": WordHandler(),
    "doc": WordHandler(),
}

# Initialize MCP server
server = Server("neurofocus-smart-tank")


@server.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools."""
    return [
        Tool(
            name="store_document",
            description="Store a document (PDF, JSON, or Word) in MongoDB. Returns the document ID.",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Path to the file to store"
                    },
                    "metadata": {
                        "type": "object",
                        "description": "Optional metadata to store with the document",
                        "additionalProperties": True
                    }
                },
                "required": ["file_path"]
            }
        ),
        Tool(
            name="retrieve_document",
            description="Retrieve a document by ID from MongoDB.",
            inputSchema={
                "type": "object",
                "properties": {
                    "document_id": {
                        "type": "string",
                        "description": "The MongoDB document ID"
                    },
                    "include_content": {
                        "type": "boolean",
                        "description": "Whether to include file content in response",
                        "default": True
                    }
                },
                "required": ["document_id"]
            }
        ),
        Tool(
            name="search_documents",
            description="Search documents by metadata or content.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query (searches in metadata and content)"
                    },
                    "file_type": {
                        "type": "string",
                        "description": "Filter by file type (pdf, json, docx)",
                        "enum": ["pdf", "json", "docx", "doc"]
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of results",
                        "default": 10
                    }
                }
            }
        ),
        Tool(
            name="delete_document",
            description="Delete a document by ID from MongoDB.",
            inputSchema={
                "type": "object",
                "properties": {
                    "document_id": {
                        "type": "string",
                        "description": "The MongoDB document ID to delete"
                    }
                },
                "required": ["document_id"]
            }
        ),
        Tool(
            name="list_documents",
            description="List all documents with optional filtering.",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_type": {
                        "type": "string",
                        "description": "Filter by file type",
                        "enum": ["pdf", "json", "docx", "doc"]
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of results",
                        "default": 50
                    },
                    "skip": {
                        "type": "integer",
                        "description": "Number of results to skip",
                        "default": 0
                    }
                }
            }
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    """Handle tool calls."""
    try:
        if name == "store_document":
            result = await store_document(arguments.get("file_path"), arguments.get("metadata"))
        elif name == "retrieve_document":
            result = await retrieve_document(
                arguments.get("document_id"),
                arguments.get("include_content", True)
            )
        elif name == "search_documents":
            result = await search_documents(
                arguments.get("query", ""),
                arguments.get("file_type"),
                arguments.get("limit", 10)
            )
        elif name == "delete_document":
            result = await delete_document(arguments.get("document_id"))
        elif name == "list_documents":
            result = await list_documents(
                arguments.get("file_type"),
                arguments.get("limit", 50),
                arguments.get("skip", 0)
            )
        else:
            result = {"error": f"Unknown tool: {name}"}
        
        return [TextContent(type="text", text=json.dumps(result, indent=2, default=str))]
    except Exception as e:
        return [TextContent(type="text", text=json.dumps({"error": str(e)}, indent=2))]


async def store_document(file_path: str, metadata: Optional[dict] = None) -> dict:
    """Store a document in MongoDB."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    # Determine file type
    file_ext = os.path.splitext(file_path)[1].lower().lstrip(".")
    if file_ext not in file_handlers:
        raise ValueError(f"Unsupported file type: {file_ext}")
    
    handler = file_handlers[file_ext]
    
    # Read and process file
    with open(file_path, "rb") as f:
        file_data = f.read()
    
    # Extract content and metadata using handler
    content_data = handler.extract_content(file_data)
    
    # Prepare document metadata
    doc_metadata = {
        "filename": os.path.basename(file_path),
        "file_type": file_ext,
        "file_size": len(file_data),
        **(metadata or {}),
        **content_data.get("metadata", {})
    }
    
    # Store file in GridFS
    file_id = fs.put(file_data, filename=os.path.basename(file_path), metadata=doc_metadata)
    
    # Store document metadata in collection
    document = {
        "_id": str(file_id),
        "gridfs_id": file_id,
        "filename": os.path.basename(file_path),
        "file_type": file_ext,
        "file_size": len(file_data),
        "metadata": doc_metadata,
        "content_preview": content_data.get("content_preview", ""),
        "extracted_text": content_data.get("extracted_text", "")
    }
    
    db.documents.insert_one(document)
    
    return {
        "success": True,
        "document_id": str(file_id),
        "filename": os.path.basename(file_path),
        "file_type": file_ext,
        "metadata": doc_metadata
    }


async def retrieve_document(document_id: str, include_content: bool = True) -> dict:
    """Retrieve a document by ID."""
    try:
        object_id = ObjectId(document_id)
    except Exception:
        raise ValueError(f"Invalid document ID: {document_id}")
    
    # Get document metadata
    doc = db.documents.find_one({"_id": document_id})
    if not doc:
        raise ValueError(f"Document not found: {document_id}")
    
    result = {
        "document_id": document_id,
        "filename": doc.get("filename"),
        "file_type": doc.get("file_type"),
        "file_size": doc.get("file_size"),
        "metadata": doc.get("metadata", {}),
        "content_preview": doc.get("content_preview", ""),
        "extracted_text": doc.get("extracted_text", "")
    }
    
    if include_content:
        # Retrieve file from GridFS
        grid_file = fs.get(object_id)
        result["file_content_base64"] = grid_file.read().hex()  # Store as hex for JSON serialization
    
    return result


async def search_documents(query: str, file_type: Optional[str] = None, limit: int = 10) -> dict:
    """Search documents by metadata or content."""
    search_filter = {}
    
    if file_type:
        search_filter["file_type"] = file_type
    
    if query:
        search_filter["$or"] = [
            {"filename": {"$regex": query, "$options": "i"}},
            {"extracted_text": {"$regex": query, "$options": "i"}},
            {"content_preview": {"$regex": query, "$options": "i"}},
            {"metadata": {"$regex": query, "$options": "i"}}
        ]
    
    documents = list(db.documents.find(search_filter).limit(limit))
    
    results = []
    for doc in documents:
        results.append({
            "document_id": doc["_id"],
            "filename": doc.get("filename"),
            "file_type": doc.get("file_type"),
            "file_size": doc.get("file_size"),
            "content_preview": doc.get("content_preview", "")[:200]  # First 200 chars
        })
    
    return {
        "count": len(results),
        "results": results
    }


async def delete_document(document_id: str) -> dict:
    """Delete a document by ID."""
    try:
        object_id = ObjectId(document_id)
    except Exception:
        raise ValueError(f"Invalid document ID: {document_id}")
    
    # Delete from GridFS
    fs.delete(object_id)
    
    # Delete from documents collection
    result = db.documents.delete_one({"_id": document_id})
    
    if result.deleted_count == 0:
        raise ValueError(f"Document not found: {document_id}")
    
    return {
        "success": True,
        "document_id": document_id,
        "message": "Document deleted successfully"
    }


async def list_documents(file_type: Optional[str] = None, limit: int = 50, skip: int = 0) -> dict:
    """List all documents with optional filtering."""
    filter_query = {}
    if file_type:
        filter_query["file_type"] = file_type
    
    documents = list(db.documents.find(filter_query).skip(skip).limit(limit))
    total = db.documents.count_documents(filter_query)
    
    results = []
    for doc in documents:
        results.append({
            "document_id": doc["_id"],
            "filename": doc.get("filename"),
            "file_type": doc.get("file_type"),
            "file_size": doc.get("file_size"),
            "metadata": doc.get("metadata", {})
        })
    
    return {
        "total": total,
        "count": len(results),
        "skip": skip,
        "limit": limit,
        "results": results
    }


async def main():
    """Main entry point."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())


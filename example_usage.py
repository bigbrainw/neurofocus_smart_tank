"""
Example usage of the MCP server tools.
This demonstrates how to interact with the server programmatically.
"""
import asyncio
import json
from server import (
    store_document,
    retrieve_document,
    search_documents,
    list_documents,
    delete_document
)


async def example_usage():
    """Example usage of the MCP server."""
    
    print("=== NeuroFocus Smart Tank MCP Server - Example Usage ===\n")
    
    # Example 1: Store a JSON document
    print("1. Storing a JSON document...")
    json_data = {
        "name": "Example Document",
        "type": "example",
        "data": {
            "key1": "value1",
            "key2": 42,
            "nested": {
                "field": "nested_value"
            }
        }
    }
    
    # Create a temporary JSON file
    temp_json_file = "example_doc.json"
    with open(temp_json_file, "w") as f:
        json.dump(json_data, f, indent=2)
    
    try:
        result = await store_document(temp_json_file, {"category": "examples"})
        doc_id = result["document_id"]
        print(f"   ✓ Stored document with ID: {doc_id}\n")
        
        # Example 2: Retrieve the document
        print("2. Retrieving the document...")
        retrieved = await retrieve_document(doc_id, include_content=False)
        print(f"   ✓ Retrieved: {retrieved['filename']}")
        print(f"   File type: {retrieved['file_type']}")
        print(f"   File size: {retrieved['file_size']} bytes")
        print(f"   Content preview: {retrieved['content_preview'][:100]}...\n")
        
        # Example 3: Search for documents
        print("3. Searching for documents...")
        search_results = await search_documents("example", limit=5)
        print(f"   ✓ Found {search_results['count']} matching documents")
        for doc in search_results['results']:
            print(f"   - {doc['filename']} ({doc['file_type']})")
        print()
        
        # Example 4: List all documents
        print("4. Listing all documents...")
        all_docs = await list_documents(limit=10)
        print(f"   ✓ Total documents: {all_docs['total']}")
        print(f"   Showing {all_docs['count']} documents:")
        for doc in all_docs['results']:
            print(f"   - {doc['filename']} (ID: {doc['document_id'][:8]}...)")
        print()
        
        # Example 5: Delete the document
        print("5. Deleting the document...")
        delete_result = await delete_document(doc_id)
        print(f"   ✓ {delete_result['message']}\n")
        
        print("=== All examples completed successfully! ===")
        
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Cleanup
        import os
        if os.path.exists(temp_json_file):
            os.remove(temp_json_file)


if __name__ == "__main__":
    asyncio.run(example_usage())


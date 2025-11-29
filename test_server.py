"""
Simple test script to verify the MCP server functionality.
"""
import asyncio
import json
import os
from server import store_document, retrieve_document, list_documents, search_documents

async def test_server():
    """Test basic server functionality."""
    print("Testing MCP Server...")
    
    # Test 1: Create a test JSON file
    test_json = {
        "name": "Test Document",
        "type": "test",
        "data": {"key": "value", "number": 42}
    }
    
    test_file = "test_document.json"
    with open(test_file, "w") as f:
        json.dump(test_json, f, indent=2)
    
    try:
        # Test storing document
        print("\n1. Testing store_document...")
        result = await store_document(test_file, {"test": True})
        print(f"   ✓ Stored document: {result['document_id']}")
        doc_id = result['document_id']
        
        # Test retrieving document
        print("\n2. Testing retrieve_document...")
        retrieved = await retrieve_document(doc_id, include_content=False)
        print(f"   ✓ Retrieved document: {retrieved['filename']}")
        
        # Test listing documents
        print("\n3. Testing list_documents...")
        listed = await list_documents(limit=10)
        print(f"   ✓ Found {listed['count']} documents")
        
        # Test searching documents
        print("\n4. Testing search_documents...")
        search_results = await search_documents("test", limit=5)
        print(f"   ✓ Found {search_results['count']} matching documents")
        
        print("\n✓ All tests passed!")
        
    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Cleanup
        if os.path.exists(test_file):
            os.remove(test_file)

if __name__ == "__main__":
    asyncio.run(test_server())


#!/usr/bin/env python3
"""
ChromaDB FastAPI - Sample Payloads and Examples
Copy and paste these examples to test the API endpoints
"""

import requests
import json

# Configuration
BASE_URL = "http://localhost:10000"  # Change to your deployed URL
API_KEY = "sk-chromadb-1234567890abcdef-abcdef1234567890"  # Your API key

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# =============================================================================
# 1. HEALTH CHECK (No authentication required)
# =============================================================================
def health_check():
    """Test if the API is running"""
    response = requests.get(f"{BASE_URL}/health")
    print("Health Check:")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.json()

# =============================================================================
# 2. ADD DOCUMENT
# =============================================================================
def add_document_examples():
    """Examples for adding documents"""
    
    # Example 1: Add document with custom ID
    payload1 = {
        "id": "doc-001",
        "text": "This is a document about machine learning and artificial intelligence. It covers neural networks, deep learning, and natural language processing."
    }
    
    response1 = requests.post(f"{BASE_URL}/add", headers=headers, json=payload1)
    print("Add Document (with ID):")
    print(f"Status: {response1.status_code}")
    print(f"Response: {response1.json()}")
    
    # Example 2: Add document without ID (auto-generated)
    payload2 = {
        "text": "This document discusses web development with FastAPI and Python. It includes REST API design, database integration, and deployment strategies."
    }
    
    response2 = requests.post(f"{BASE_URL}/add", headers=headers, json=payload2)
    print("\nAdd Document (auto ID):")
    print(f"Status: {response2.status_code}")
    print(f"Response: {response2.json()}")
    
    return response1.json(), response2.json()

# =============================================================================
# 3. GET DOCUMENT
# =============================================================================
def get_document_example(doc_id: str):
    """Get a document by ID"""
    response = requests.get(f"{BASE_URL}/get/{doc_id}", headers=headers)
    print(f"Get Document (ID: {doc_id}):")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.json()

# =============================================================================
# 4. UPDATE DOCUMENT
# =============================================================================
def update_document_example(doc_id: str):
    """Update a document"""
    payload = {
        "id": doc_id,
        "text": "This is an UPDATED document about machine learning and AI. It now includes information about large language models and transformer architectures."
    }
    
    response = requests.put(f"{BASE_URL}/update", headers=headers, json=payload)
    print(f"Update Document (ID: {doc_id}):")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.json()

# =============================================================================
# 5. SEARCH DOCUMENTS
# =============================================================================
def search_documents_examples():
    """Examples for searching documents"""
    
    # Example 1: Basic search
    params1 = {"query": "machine learning", "limit": 5}
    response1 = requests.get(f"{BASE_URL}/search", headers=headers, params=params1)
    print("Search Documents (machine learning):")
    print(f"Status: {response1.status_code}")
    print(f"Response: {response1.json()}")
    
    # Example 2: Search with different query
    params2 = {"query": "web development", "limit": 10}
    response2 = requests.get(f"{BASE_URL}/search", headers=headers, params=params2)
    print("\nSearch Documents (web development):")
    print(f"Status: {response2.status_code}")
    print(f"Response: {response2.json()}")
    
    return response1.json(), response2.json()

# =============================================================================
# 6. DELETE DOCUMENT
# =============================================================================
def delete_document_example(doc_id: str):
    """Delete a document"""
    response = requests.delete(f"{BASE_URL}/delete/{doc_id}", headers=headers)
    print(f"Delete Document (ID: {doc_id}):")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.json()

# =============================================================================
# 7. COMPLETE CRUD WORKFLOW
# =============================================================================
def complete_crud_workflow():
    """Run a complete CRUD workflow example"""
    print("🚀 Starting Complete CRUD Workflow")
    print("="*50)
    
    # Step 1: Health check
    print("\n1️⃣ Health Check:")
    health_check()
    
    # Step 2: Add documents
    print("\n2️⃣ Adding Documents:")
    doc1, doc2 = add_document_examples()
    
    # Step 3: Get documents
    print("\n3️⃣ Getting Documents:")
    if doc1.get("id"):
        get_document_example(doc1["id"])
    if doc2.get("id"):
        get_document_example(doc2["id"])
    
    # Step 4: Update document
    print("\n4️⃣ Updating Document:")
    if doc1.get("id"):
        update_document_example(doc1["id"])
    
    # Step 5: Search documents
    print("\n5️⃣ Searching Documents:")
    search_documents_examples()
    
    # Step 6: Delete documents
    print("\n6️⃣ Deleting Documents:")
    if doc1.get("id"):
        delete_document_example(doc1["id"])
    if doc2.get("id"):
        delete_document_example(doc2["id"])
    
    print("\n✅ CRUD Workflow Complete!")

# =============================================================================
# 8. CURL EQUIVALENTS
# =============================================================================
def print_curl_examples():
    """Print curl command equivalents"""
    print("\n🔧 CURL Command Equivalents:")
    print("="*50)
    
    print("\n1. Health Check:")
    print(f"curl {BASE_URL}/health")
    
    print("\n2. Add Document:")
    print(f'''curl -X POST "{BASE_URL}/add" \\
  -H "Authorization: Bearer {API_KEY}" \\
  -H "Content-Type: application/json" \\
  -d '{{"text": "Sample document text"}}' ''')
    
    print("\n3. Get Document:")
    print(f'''curl -X GET "{BASE_URL}/get/doc-001" \\
  -H "Authorization: Bearer {API_KEY}" ''')
    
    print("\n4. Update Document:")
    print(f'''curl -X PUT "{BASE_URL}/update" \\
  -H "Authorization: Bearer {API_KEY}" \\
  -H "Content-Type: application/json" \\
  -d '{{"id": "doc-001", "text": "Updated text"}}' ''')
    
    print("\n5. Search Documents:")
    print(f'''curl -X GET "{BASE_URL}/search?query=machine%20learning&limit=5" \\
  -H "Authorization: Bearer {API_KEY}" ''')
    
    print("\n6. Delete Document:")
    print(f'''curl -X DELETE "{BASE_URL}/delete/doc-001" \\
  -H "Authorization: Bearer {API_KEY}" ''')

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--curl":
            print_curl_examples()
        elif sys.argv[1] == "--workflow":
            complete_crud_workflow()
        else:
            print("Usage:")
            print("python api_payloads.py --workflow  # Run complete CRUD workflow")
            print("python api_payloads.py --curl      # Show curl examples")
    else:
        print("ChromaDB FastAPI - Sample Payloads")
        print("="*40)
        print("Available functions:")
        print("- health_check()")
        print("- add_document_examples()")
        print("- get_document_example(doc_id)")
        print("- update_document_example(doc_id)")
        print("- search_documents_examples()")
        print("- delete_document_example(doc_id)")
        print("- complete_crud_workflow()")
        print("\nRun with --workflow to test all operations")
        print("Run with --curl to see curl command examples")

#!/usr/bin/env python3
"""
ChromaDB FastAPI - Complete CRUD Payload Examples
Copy and paste these examples to test individual operations
"""

import requests
import json
import os
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
API_KEY = os.getenv('API_KEY', 'cSC3pej89xYEBKlFjHFs6I3wfyQmAh0n')

# Configuration
BASE_URL = "http://127.0.0.1:8000"

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
# 2. ADD DOCUMENT - Multiple Examples
# =============================================================================
def add_document_with_id():
    """Add document with custom ID"""
    payload = {
        "id": "ml-doc-001",
        "text": "Machine learning is a subset of artificial intelligence that focuses on algorithms and statistical models. It enables computers to learn and make decisions from data without being explicitly programmed."
    }
    
    response = requests.post(f"{BASE_URL}/add", headers=headers, json=payload)
    print("Add Document (with ID):")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.json()

def add_document_auto_id():
    """Add document with auto-generated ID"""
    payload = {
        "text": "Deep learning uses artificial neural networks with multiple layers to model and understand complex patterns in data. It's particularly effective for image recognition and speech processing."
    }
    
    response = requests.post(f"{BASE_URL}/add", headers=headers, json=payload)
    print("Add Document (auto ID):")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.json()

def add_multiple_documents():
    """Add multiple documents for testing"""
    documents = [
        {
            "id": "ai-doc-001",
            "text": "Artificial intelligence encompasses machine learning, deep learning, neural networks, and natural language processing. AI systems can perform tasks that typically require human intelligence."
        },
        {
            "id": "web-doc-002",
            "text": "FastAPI is a modern, fast web framework for building APIs with Python. It provides automatic API documentation, type hints, and high performance for web applications."
        },
        {
            "text": "Natural language processing (NLP) combines computational linguistics with machine learning to help computers understand, interpret, and manipulate human language."
        },
        {
            "id": "data-doc-004",
            "text": "Data science combines statistics, programming, and domain expertise to extract insights from data. It involves data collection, cleaning, analysis, and visualization."
        }
    ]
    
    results = []
    for i, doc in enumerate(documents, 1):
        print(f"\nAdding Document {i}:")
        response = requests.post(f"{BASE_URL}/add", headers=headers, json=doc)
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Response: {result}")
        results.append(result)
    
    return results

# =============================================================================
# 3. GET DOCUMENT
# =============================================================================
def get_document(doc_id):
    """Get a document by ID"""
    response = requests.get(f"{BASE_URL}/get/{doc_id}", headers=headers)
    print(f"Get Document (ID: {doc_id}):")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.json()

# =============================================================================
# 4. UPDATE DOCUMENT
# =============================================================================
def update_document(doc_id, new_text):
    """Update a document"""
    payload = {
        "id": doc_id,
        "text": new_text
    }
    
    response = requests.put(f"{BASE_URL}/update", headers=headers, json=payload)
    print(f"Update Document (ID: {doc_id}):")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.json()

# =============================================================================
# 5. SEMANTIC SEARCH - Multiple Examples
# =============================================================================
def search_machine_learning():
    """Search for machine learning related content"""
    params = {"query": "machine learning algorithms", "limit": 5}
    response = requests.get(f"{BASE_URL}/search", headers=headers, params=params)
    print("Search: 'machine learning algorithms'")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.json()

def search_artificial_intelligence():
    """Search for AI related content"""
    params = {"query": "artificial intelligence systems", "limit": 5}
    response = requests.get(f"{BASE_URL}/search", headers=headers, params=params)
    print("Search: 'artificial intelligence systems'")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.json()

def search_web_development():
    """Search for web development content"""
    params = {"query": "web development APIs", "limit": 5}
    response = requests.get(f"{BASE_URL}/search", headers=headers, params=params)
    print("Search: 'web development APIs'")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.json()

def search_natural_language():
    """Search for NLP content"""
    params = {"query": "natural language processing", "limit": 5}
    response = requests.get(f"{BASE_URL}/search", headers=headers, params=params)
    print("Search: 'natural language processing'")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.json()

def search_data_science():
    """Search for data science content"""
    params = {"query": "data science analytics", "limit": 5}
    response = requests.get(f"{BASE_URL}/search", headers=headers, params=params)
    print("Search: 'data science analytics'")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.json()

# =============================================================================
# 6. DELETE DOCUMENT
# =============================================================================
def delete_document(doc_id):
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
    """Run a complete CRUD workflow"""
    print("🚀 Starting Complete CRUD Workflow")
    print("="*50)
    
    # Step 1: Health check
    print("\n1️⃣ Health Check:")
    health_check()
    
    # Step 2: Add documents
    print("\n2️⃣ Adding Documents:")
    added_docs = add_multiple_documents()
    
    # Step 3: Get documents
    print("\n3️⃣ Getting Documents:")
    for doc in added_docs:
        if doc.get("id"):
            get_document(doc["id"])
    
    # Step 4: Update document
    print("\n4️⃣ Updating Document:")
    if added_docs and added_docs[0].get("id"):
        update_text = "UPDATED: Machine learning is a powerful subset of artificial intelligence that focuses on algorithms and statistical models. It enables computers to learn and make intelligent decisions from data without being explicitly programmed for every scenario."
        update_document(added_docs[0]["id"], update_text)
    
    # Step 5: Search documents
    print("\n5️⃣ Searching Documents:")
    search_machine_learning()
    search_artificial_intelligence()
    search_web_development()
    search_natural_language()
    search_data_science()
    
    # Step 6: Delete documents
    print("\n6️⃣ Deleting Documents:")
    for doc in added_docs:
        if doc.get("id"):
            delete_document(doc["id"])
    
    print("\n✅ CRUD Workflow Complete!")

# =============================================================================
# 8. INDIVIDUAL TEST FUNCTIONS
# =============================================================================
def test_individual_operations():
    """Test individual operations"""
    print("🔧 Testing Individual Operations")
    print("="*40)
    
    # Test health
    health_check()
    
    # Test add
    doc1 = add_document_with_id()
    doc2 = add_document_auto_id()
    
    # Test get
    if doc1.get("id"):
        get_document(doc1["id"])
    
    # Test search
    search_machine_learning()
    
    # Test update
    if doc1.get("id"):
        update_document(doc1["id"], "This is an updated document about machine learning and AI.")
    
    # Test delete
    if doc1.get("id"):
        delete_document(doc1["id"])
    if doc2.get("id"):
        delete_document(doc2["id"])

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--workflow":
            complete_crud_workflow()
        elif sys.argv[1] == "--individual":
            test_individual_operations()
        elif sys.argv[1] == "--search":
            print("🔍 Testing Semantic Search Only:")
            search_machine_learning()
            search_artificial_intelligence()
            search_web_development()
        else:
            print("Usage:")
            print("python crud_payloads.py --workflow    # Run complete CRUD workflow")
            print("python crud_payloads.py --individual  # Test individual operations")
            print("python crud_payloads.py --search      # Test semantic search only")
    else:
        print("ChromaDB FastAPI - CRUD Payload Examples")
        print("="*45)
        print("Available functions:")
        print("- health_check()")
        print("- add_document_with_id()")
        print("- add_document_auto_id()")
        print("- add_multiple_documents()")
        print("- get_document(doc_id)")
        print("- update_document(doc_id, new_text)")
        print("- search_machine_learning()")
        print("- search_artificial_intelligence()")
        print("- search_web_development()")
        print("- search_natural_language()")
        print("- search_data_science()")
        print("- delete_document(doc_id)")
        print("- complete_crud_workflow()")
        print("\nRun with --workflow to test all operations")
        print("Run with --individual to test individual operations")
        print("Run with --search to test semantic search only")

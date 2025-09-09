#!/usr/bin/env python3
"""
Complete CRUD Operations Test with Semantic Search
Tests all endpoints with detailed payloads and responses
"""

import requests
import json
import os
import time
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

class ChromaDBTester:
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        self.added_docs = []
    
    def print_section(self, title):
        """Print a formatted section header"""
        print(f"\n{'='*80}")
        print(f"🔍 {title}")
        print(f"{'='*80}")
    
    def print_result(self, operation, response, success_msg="✅ Success", error_msg="❌ Failed"):
        """Print formatted result"""
        status = response.status_code
        try:
            data = response.json()
        except:
            data = response.text
        
        if 200 <= status < 300:
            print(f"{success_msg} (Status: {status})")
            print(f"📄 Response: {json.dumps(data, indent=2)}")
            return True
        else:
            print(f"{error_msg} (Status: {status})")
            print(f"📄 Response: {json.dumps(data, indent=2)}")
            return False
    
    def test_health(self):
        """Test health endpoint"""
        self.print_section("HEALTH CHECK")
        try:
            response = requests.get(f"{self.base_url}/health", timeout=10)
            return self.print_result("Health Check", response)
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    def test_add_documents(self):
        """Test adding multiple documents"""
        self.print_section("ADD DOCUMENTS")
        
        documents = [
            {
                "id": "ml-doc-001",
                "text": "Machine learning is a subset of artificial intelligence that focuses on algorithms and statistical models. It enables computers to learn and make decisions from data without being explicitly programmed."
            },
            {
                "id": "ai-doc-002", 
                "text": "Artificial intelligence encompasses machine learning, deep learning, neural networks, and natural language processing. AI systems can perform tasks that typically require human intelligence."
            },
            {
                "text": "Deep learning uses artificial neural networks with multiple layers to model and understand complex patterns in data. It's particularly effective for image recognition, speech processing, and language understanding."
            },
            {
                "id": "web-doc-004",
                "text": "FastAPI is a modern, fast web framework for building APIs with Python. It provides automatic API documentation, type hints, and high performance for web applications."
            },
            {
                "text": "Natural language processing (NLP) combines computational linguistics with machine learning to help computers understand, interpret, and manipulate human language."
            }
        ]
        
        success_count = 0
        for i, doc in enumerate(documents, 1):
            print(f"\n📝 Adding Document {i}:")
            print(f"   ID: {doc.get('id', 'Auto-generated')}")
            print(f"   Text: {doc['text'][:100]}...")
            
            try:
                response = requests.post(f"{self.base_url}/add", headers=self.headers, json=doc, timeout=10)
                if self.print_result(f"Add Document {i}", response):
                    result = response.json()
                    self.added_docs.append(result)
                    success_count += 1
            except Exception as e:
                print(f"❌ Error: {e}")
        
        print(f"\n📊 Added {success_count}/{len(documents)} documents successfully")
        return success_count > 0
    
    def test_get_documents(self):
        """Test getting documents by ID"""
        self.print_section("GET DOCUMENTS")
        
        if not self.added_docs:
            print("❌ No documents to retrieve")
            return False
        
        success_count = 0
        for i, doc in enumerate(self.added_docs, 1):
            doc_id = doc.get("id")
            if doc_id:
                print(f"\n📖 Getting Document {i} (ID: {doc_id}):")
                try:
                    response = requests.get(f"{self.base_url}/get/{doc_id}", headers=self.headers, timeout=10)
                    if self.print_result(f"Get Document {i}", response):
                        success_count += 1
                except Exception as e:
                    print(f"❌ Error: {e}")
        
        print(f"\n📊 Retrieved {success_count}/{len(self.added_docs)} documents successfully")
        return success_count > 0
    
    def test_update_documents(self):
        """Test updating documents"""
        self.print_section("UPDATE DOCUMENTS")
        
        if not self.added_docs:
            print("❌ No documents to update")
            return False
        
        # Update the first document
        first_doc = self.added_docs[0]
        doc_id = first_doc.get("id")
        
        if doc_id:
            updated_text = "UPDATED: Machine learning is a powerful subset of artificial intelligence that focuses on algorithms and statistical models. It enables computers to learn and make intelligent decisions from data without being explicitly programmed for every scenario."
            
            print(f"\n✏️ Updating Document (ID: {doc_id}):")
            print(f"   Original: {first_doc['text'][:100]}...")
            print(f"   Updated: {updated_text[:100]}...")
            
            payload = {"id": doc_id, "text": updated_text}
            try:
                response = requests.put(f"{self.base_url}/update", headers=self.headers, json=payload, timeout=10)
                return self.print_result("Update Document", response)
            except Exception as e:
                print(f"❌ Error: {e}")
                return False
        
        return False
    
    def test_semantic_search(self):
        """Test semantic search with various queries"""
        self.print_section("SEMANTIC SEARCH")
        
        search_queries = [
            {
                "query": "machine learning algorithms",
                "description": "Search for machine learning related content"
            },
            {
                "query": "artificial intelligence systems",
                "description": "Search for AI and intelligence systems"
            },
            {
                "query": "neural networks deep learning",
                "description": "Search for neural networks and deep learning"
            },
            {
                "query": "web development APIs",
                "description": "Search for web development and API content"
            },
            {
                "query": "natural language processing",
                "description": "Search for NLP and language processing"
            },
            {
                "query": "data science analytics",
                "description": "Search for data science and analytics"
            }
        ]
        
        success_count = 0
        for i, search in enumerate(search_queries, 1):
            print(f"\n🔍 Search {i}: {search['description']}")
            print(f"   Query: '{search['query']}'")
            
            params = {"query": search["query"], "limit": 5}
            try:
                response = requests.get(f"{self.base_url}/search", headers=self.headers, params=params, timeout=10)
                if self.print_result(f"Search {i}", response):
                    result = response.json()
                    if isinstance(result, list) and len(result) > 0:
                        print(f"   📊 Found {len(result)} results")
                        for j, match in enumerate(result[:3], 1):  # Show top 3 results
                            print(f"      {j}. ID: {match.get('id', 'N/A')} | Distance: {match.get('distance', 'N/A'):.4f}")
                            print(f"         Text: {match.get('text', 'N/A')[:80]}...")
                    else:
                        print("   📊 No results found")
                    success_count += 1
            except Exception as e:
                print(f"❌ Error: {e}")
        
        print(f"\n📊 Completed {success_count}/{len(search_queries)} searches successfully")
        return success_count > 0
    
    def test_delete_documents(self):
        """Test deleting documents"""
        self.print_section("DELETE DOCUMENTS")
        
        if not self.added_docs:
            print("❌ No documents to delete")
            return False
        
        success_count = 0
        for i, doc in enumerate(self.added_docs, 1):
            doc_id = doc.get("id")
            if doc_id:
                print(f"\n🗑️ Deleting Document {i} (ID: {doc_id}):")
                try:
                    response = requests.delete(f"{self.base_url}/delete/{doc_id}", headers=self.headers, timeout=10)
                    if self.print_result(f"Delete Document {i}", response):
                        success_count += 1
                except Exception as e:
                    print(f"❌ Error: {e}")
        
        print(f"\n📊 Deleted {success_count}/{len(self.added_docs)} documents successfully")
        return success_count > 0
    
    def run_complete_test(self):
        """Run complete CRUD test suite"""
        print("🚀 CHROMADB FASTAPI - COMPLETE CRUD TEST SUITE")
        print(f"🌐 Base URL: {self.base_url}")
        print(f"🔑 API Key: {self.api_key[:10]}...{self.api_key[-4:]}")
        print(f"⏰ Started at: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        results = {}
        
        # Test 1: Health Check
        results['health'] = self.test_health()
        
        # Test 2: Add Documents
        results['add'] = self.test_add_documents()
        
        # Test 3: Get Documents
        results['get'] = self.test_get_documents()
        
        # Test 4: Update Documents
        results['update'] = self.test_update_documents()
        
        # Test 5: Semantic Search
        results['search'] = self.test_semantic_search()
        
        # Test 6: Delete Documents
        results['delete'] = self.test_delete_documents()
        
        # Final Results
        self.print_section("FINAL RESULTS")
        print(f"⏰ Completed at: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        print("\n📊 Test Results Summary:")
        for test, passed in results.items():
            status = "✅ PASS" if passed else "❌ FAIL"
            print(f"   {test.upper()}: {status}")
        
        total_passed = sum(results.values())
        total_tests = len(results)
        print(f"\n🎯 Overall: {total_passed}/{total_tests} tests passed")
        
        if total_passed == total_tests:
            print("🎉 ALL TESTS PASSED! Your ChromaDB FastAPI is working perfectly!")
        else:
            print("⚠️ Some tests failed. Check the error messages above.")
        
        return results

def main():
    """Main function"""
    tester = ChromaDBTester(BASE_URL, API_KEY)
    results = tester.run_complete_test()
    
    print(f"\n{'='*80}")
    print("💡 USAGE EXAMPLES:")
    print(f"{'='*80}")
    print("python complete_crud_test.py  # Run complete test suite")
    print("\n🔧 Individual test functions available:")
    print("- tester.test_health()")
    print("- tester.test_add_documents()")
    print("- tester.test_get_documents()")
    print("- tester.test_update_documents()")
    print("- tester.test_semantic_search()")
    print("- tester.test_delete_documents()")

if __name__ == "__main__":
    main()

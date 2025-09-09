from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import os
from typing import Optional, List
import uuid
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="ChromaDB API", version="1.0.0")

# Security scheme
security = HTTPBearer()

# Simple in-memory storage for testing
documents_storage = {}

# Pydantic models
class DocumentAdd(BaseModel):
    id: Optional[str] = None
    text: str

class DocumentUpdate(BaseModel):
    id: str
    text: str

class DocumentResponse(BaseModel):
    id: str
    text: str

class SearchResponse(BaseModel):
    id: str
    text: str
    distance: float

# API Key authentication
def verify_api_key(credentials: HTTPAuthorizationCredentials = Depends(security)):
    api_key = os.getenv("API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="API_KEY not configured")
    
    if credentials.credentials != api_key:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    return credentials.credentials

# CRUD Operations

@app.post("/add", response_model=DocumentResponse)
async def add_document(
    document: DocumentAdd,
    api_key: str = Depends(verify_api_key)
):
    """Add a new document to the collection"""
    try:
        # Generate ID if not provided
        doc_id = document.id or str(uuid.uuid4())
        
        # Add document to storage
        documents_storage[doc_id] = document.text
        
        return DocumentResponse(id=doc_id, text=document.text)
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to add document: {str(e)}")

@app.get("/get/{doc_id}", response_model=DocumentResponse)
async def get_document(
    doc_id: str,
    api_key: str = Depends(verify_api_key)
):
    """Get a document by ID"""
    try:
        if doc_id not in documents_storage:
            raise HTTPException(status_code=404, detail="Document not found")
        
        return DocumentResponse(
            id=doc_id,
            text=documents_storage[doc_id]
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to get document: {str(e)}")

@app.put("/update", response_model=DocumentResponse)
async def update_document(
    document: DocumentUpdate,
    api_key: str = Depends(verify_api_key)
):
    """Update an existing document"""
    try:
        # Check if document exists
        if document.id not in documents_storage:
            raise HTTPException(status_code=404, detail="Document not found")
        
        # Update document
        documents_storage[document.id] = document.text
        
        return DocumentResponse(id=document.id, text=document.text)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to update document: {str(e)}")

@app.delete("/delete/{doc_id}")
async def delete_document(
    doc_id: str,
    api_key: str = Depends(verify_api_key)
):
    """Delete a document by ID"""
    try:
        # Check if document exists
        if doc_id not in documents_storage:
            raise HTTPException(status_code=404, detail="Document not found")
        
        # Delete document
        del documents_storage[doc_id]
        
        return {"message": "Document deleted successfully", "id": doc_id}
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to delete document: {str(e)}")

@app.get("/search", response_model=List[SearchResponse])
async def search_documents(
    query: str,
    limit: int = 10,
    api_key: str = Depends(verify_api_key)
):
    """Search documents using simple text matching"""
    try:
        if not query.strip():
            raise HTTPException(status_code=400, detail="Query cannot be empty")
        
        # Simple text search (case-insensitive)
        results = []
        query_lower = query.lower()
        
        for doc_id, text in documents_storage.items():
            if query_lower in text.lower():
                # Simple distance calculation (inverse of match count)
                match_count = text.lower().count(query_lower)
                distance = 1.0 / (match_count + 1)  # Lower distance = better match
                
                results.append(SearchResponse(
                    id=doc_id,
                    text=text,
                    distance=distance
                ))
        
        # Sort by distance (ascending) and limit results
        results.sort(key=lambda x: x.distance)
        return results[:limit]
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Search failed: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint (no auth required)"""
    return {"status": "healthy", "service": "ChromaDB API (Minimal Version)"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)

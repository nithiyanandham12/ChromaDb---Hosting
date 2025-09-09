from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import chromadb
from chromadb.config import Settings
import os
from typing import Optional, List
import uuid
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="ChromaDB API", version="1.0.0")

# Security scheme
security = HTTPBearer()

# ChromaDB client with error handling
try:
    chroma_client = chromadb.PersistentClient(
        path="./chroma_store",
        settings=Settings(anonymized_telemetry=False)
    )
    
    # Get or create collection
    collection = chroma_client.get_or_create_collection(
        name="documents",
        metadata={"hnsw:space": "cosine"}
    )
    logger.info("ChromaDB initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize ChromaDB: {e}")
    # For development/testing, we'll handle this gracefully
    chroma_client = None
    collection = None

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

# Check if ChromaDB is available
def check_chromadb():
    if collection is None:
        raise HTTPException(status_code=503, detail="ChromaDB service unavailable")

# CRUD Operations

@app.post("/add", response_model=DocumentResponse)
async def add_document(
    document: DocumentAdd,
    api_key: str = Depends(verify_api_key)
):
    """Add a new document to the collection"""
    check_chromadb()
    
    try:
        # Generate ID if not provided
        doc_id = document.id or str(uuid.uuid4())
        
        # Add document to ChromaDB
        collection.add(
            documents=[document.text],
            ids=[doc_id]
        )
        
        return DocumentResponse(id=doc_id, text=document.text)
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to add document: {str(e)}")

@app.get("/get/{doc_id}", response_model=DocumentResponse)
async def get_document(
    doc_id: str,
    api_key: str = Depends(verify_api_key)
):
    """Get a document by ID"""
    check_chromadb()
    
    try:
        result = collection.get(ids=[doc_id])
        
        if not result['ids']:
            raise HTTPException(status_code=404, detail="Document not found")
        
        return DocumentResponse(
            id=result['ids'][0],
            text=result['documents'][0]
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
    check_chromadb()
    
    try:
        # Check if document exists
        existing = collection.get(ids=[document.id])
        if not existing['ids']:
            raise HTTPException(status_code=404, detail="Document not found")
        
        # Update document
        collection.update(
            documents=[document.text],
            ids=[document.id]
        )
        
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
    check_chromadb()
    
    try:
        # Check if document exists
        existing = collection.get(ids=[doc_id])
        if not existing['ids']:
            raise HTTPException(status_code=404, detail="Document not found")
        
        # Delete document
        collection.delete(ids=[doc_id])
        
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
    """Search documents using semantic similarity"""
    check_chromadb()
    
    try:
        if not query.strip():
            raise HTTPException(status_code=400, detail="Query cannot be empty")
        
        # Perform semantic search
        results = collection.query(
            query_texts=[query],
            n_results=min(limit, 100)  # Cap at 100 results
        )
        
        if not results['ids'][0]:
            return []
        
        # Format results
        search_results = []
        for i, doc_id in enumerate(results['ids'][0]):
            search_results.append(SearchResponse(
                id=doc_id,
                text=results['documents'][0][i],
                distance=results['distances'][0][i]
            ))
        
        return search_results
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Search failed: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint (no auth required)"""
    return {"status": "healthy", "service": "ChromaDB API"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)

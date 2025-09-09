# ChromaDB FastAPI - Postman Collection Setup

## 🚀 **Quick Import Link:**

**Copy this link and paste it in Postman:**
```
https://raw.githubusercontent.com/nithiyanandham12/ChromaDb---Hosting/main/ChromaDB_API_Postman_Collection.json
```

## 📋 **Manual Setup Instructions:**

### **1. Import Collection:**
1. Open Postman
2. Click "Import" button
3. Choose "Link" tab
4. Paste the import link above
5. Click "Continue" → "Import"

### **2. Collection Details:**
- **Name:** ChromaDB FastAPI - Deployed API
- **Base URL:** `https://chromadb-hosting.onrender.com`
- **API Key:** `cSC3pej89xYEBKlFjHFs6I3wfyQmAh0n`

### **3. Available Endpoints:**

#### **Health Check (No Auth Required):**
- **Method:** GET
- **URL:** `https://chromadb-hosting.onrender.com/health`

#### **Add Document:**
- **Method:** POST
- **URL:** `https://chromadb-hosting.onrender.com/add`
- **Body:** 
```json
{
  "id": "ml-doc-001",
  "text": "Your document text here"
}
```

#### **Get Document:**
- **Method:** GET
- **URL:** `https://chromadb-hosting.onrender.com/get/{doc_id}`

#### **Update Document:**
- **Method:** PUT
- **URL:** `https://chromadb-hosting.onrender.com/update`
- **Body:**
```json
{
  "id": "ml-doc-001",
  "text": "Updated document text"
}
```

#### **Search Documents:**
- **Method:** GET
- **URL:** `https://chromadb-hosting.onrender.com/search?query=your_search_term&limit=5`

#### **Delete Document:**
- **Method:** DELETE
- **URL:** `https://chromadb-hosting.onrender.com/delete/{doc_id}`

## 🔑 **Authentication:**
All endpoints (except health check) require Bearer token authentication:
- **Header:** `Authorization`
- **Value:** `Bearer cSC3pej89xYEBKlFjHFs6I3wfyQmAh0n`

## 🧪 **Test Sequence:**
1. **Health Check** - Verify API is running
2. **Add Document** - Create a test document
3. **Get Document** - Retrieve the document
4. **Search Documents** - Search for content
5. **Update Document** - Modify the document
6. **Delete Document** - Remove the document

## 📊 **Expected Responses:**

### **Health Check:**
```json
{
  "status": "healthy",
  "service": "ChromaDB API (Minimal Version)"
}
```

### **Add Document:**
```json
{
  "id": "ml-doc-001",
  "text": "Your document text here"
}
```

### **Search Results:**
```json
[
  {
    "id": "ml-doc-001",
    "text": "Document text...",
    "distance": 0.5
  }
]
```

## 🎯 **Ready to Test!**
Your Postman collection is ready with all CRUD operations for your deployed ChromaDB FastAPI!

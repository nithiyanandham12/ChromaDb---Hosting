# ChromaDB FastAPI - Deployment Guide

## 🚀 Files Required for Git Push & Render Deployment

### **Essential Files (MUST include):**

#### **Core Application Files:**
- ✅ `main.py` - Main FastAPI application
- ✅ `requirements.txt` - Python dependencies
- ✅ `render.yaml` - Render deployment configuration

#### **Documentation:**
- ✅ `README.md` - Project documentation
- ✅ `DEPLOYMENT.md` - This deployment guide

### **Optional Files (Recommended to include):**
- ✅ `api_payloads.py` - API usage examples
- ✅ `complete_crud_test.py` - Complete test suite
- ✅ `crud_payloads.py` - CRUD operation examples

### **Files to EXCLUDE (in .gitignore):**
- ❌ `.env` - Contains sensitive API keys
- ❌ `chroma_store/` - Local database storage
- ❌ `__pycache__/` - Python cache files
- ❌ `*.log` - Log files
- ❌ `venv/` - Virtual environment

## 📋 Git Commands for Deployment

### **1. Initialize Git Repository:**
```bash
git init
git add .gitignore
git add main.py
git add requirements.txt
git add render.yaml
git add README.md
git add DEPLOYMENT.md
git add api_payloads.py
git add complete_crud_test.py
git add crud_payloads.py
```

### **2. Commit Files:**
```bash
git commit -m "Initial commit: ChromaDB FastAPI with CRUD operations"
```

### **3. Create GitHub Repository:**
1. Go to GitHub.com
2. Create a new repository (e.g., `chromadb-fastapi`)
3. Don't initialize with README (we already have files)

### **4. Push to GitHub:**
```bash
git remote add origin https://github.com/YOUR_USERNAME/chromadb-fastapi.git
git branch -M main
git push -u origin main
```

## 🌐 Render Deployment Steps

### **1. Connect to Render:**
1. Go to [render.com](https://render.com)
2. Sign up/Login with GitHub
3. Click "New +" → "Web Service"
4. Connect your GitHub repository

### **2. Configure Render Service:**
- **Name:** `chromadb-api` (or your preferred name)
- **Environment:** `Python 3`
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`

### **3. Set Environment Variables:**
In Render dashboard, add:
- **Key:** `API_KEY`
- **Value:** `cSC3pej89xYEBKlFjHFs6I3wfyQmAh0n` (or generate a new one)

### **4. Deploy:**
- Click "Create Web Service"
- Render will automatically build and deploy your app
- Your API will be available at: `https://your-app-name.onrender.com`

## 🔧 Post-Deployment Testing

### **Test Your Deployed API:**
```python
import requests

# Update the URL to your Render deployment
BASE_URL = "https://your-app-name.onrender.com"
API_KEY = "cSC3pej89xYEBKlFjHFs6I3wfyQmAh0n"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Test health endpoint
response = requests.get(f"{BASE_URL}/health")
print("Health Check:", response.json())

# Test add document
payload = {"text": "Test document for deployed API"}
response = requests.post(f"{BASE_URL}/add", headers=headers, json=payload)
print("Add Document:", response.json())
```

## 📁 Final File Structure for Git:

```
chromadb-fastapi/
├── .gitignore                 # Git ignore rules
├── main.py                   # Main FastAPI application
├── requirements.txt          # Python dependencies
├── render.yaml              # Render deployment config
├── README.md                # Project documentation
├── DEPLOYMENT.md            # This deployment guide
├── api_payloads.py          # API usage examples
├── complete_crud_test.py    # Complete test suite
└── crud_payloads.py         # CRUD operation examples
```

## ⚠️ Important Notes:

1. **Never commit `.env` file** - It contains sensitive API keys
2. **ChromaDB storage** will be created automatically on Render
3. **Free tier limitations:** 512MB RAM, may sleep after inactivity
4. **API Key:** Use the same key from your `.env` file in Render environment variables

## 🎯 Quick Deployment Checklist:

- [ ] All essential files added to Git
- [ ] `.gitignore` configured properly
- [ ] Repository pushed to GitHub
- [ ] Render service connected to GitHub
- [ ] Environment variables set in Render
- [ ] API tested after deployment

Your ChromaDB FastAPI is now ready for production deployment! 🚀

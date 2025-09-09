#!/usr/bin/env python3
"""
Startup script for Render deployment
"""
import os
import uvicorn

if __name__ == "__main__":
    # Get port from environment variable, default to 10000
    port = int(os.getenv("PORT", 10000))
    
    # Start the server
    uvicorn.run(
        "main_simple:app",
        host="0.0.0.0",
        port=port,
        log_level="info"
    )

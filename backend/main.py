"""Kavach — Legal AI Trust Platform

Main FastAPI application with complete sophisticated feature set.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from api.routes import router

app = FastAPI(
    title="Kavach",
    description="Legal AI Trust Platform — Making AI safe, reliable, and defensible for legal practice",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")

@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Kavach API</title>
        <style>
            body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 1000px; margin: 50px auto; padding: 20px; background: #f8fafc; }
            h1 { color: #059669; font-size: 2.5rem; }
            h2 { color: #334155; margin-top: 2rem; }
            .endpoint { background: white; padding: 20px; margin: 15px 0; border-radius: 12px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
            .method { color: white; padding: 4px 10px; border-radius: 6px; font-weight: bold; font-size: 12px; }
            .post { background: #3b82f6; }
            .get { background: #22c55e; }
            .feature { display: inline-block; background: #ecfdf5; color: #059669; padding: 4px 12px; border-radius: 20px; margin: 4px; font-size: 14px; }
            code { background: #f1f5f9; padding: 2px 6px; border-radius: 4px; font-family: monospace; }
        </style>
    </head>
    <body>
        <h1>🛡️ Kavach — Legal AI Trust Platform</h1>
        <p style="color: #64748b; font-size: 1.1rem;">Making AI safe, reliable, and defensible for legal practice</p>
        
        <div style="margin: 20px 0;">
            <span class="feature">📜 Citation Verification</span>
            <span class="feature">🔒 Privilege Shield</span>
            <span class="feature">📊 Confidence Scoring</span>
            <span class="feature">🔍 Multi-Agent Verification</span>
            <span class="feature">🎯 Vector Similarity</span>
            <span class="feature">🕸️ Citation Graph</span>
            <span class="feature">📋 Contract Analysis</span>
            <span class="feature">⚡ Advanced RAG</span>
        </div>
        
        <h2>API Endpoints</h2>
        
        <div class="endpoint">
            <span class="method post">POST</span> <strong>/api/analyze</strong>
            <p>Complete trust analysis with all sophisticated features</p>
        </div>
        
        <div class="endpoint">
            <span class="method post">POST</span> <strong>/api/verify</strong>
            <p>Multi-agent verification pipeline (5 specialized agents)</p>
        </div>
        
        <div class="endpoint">
            <span class="method post">POST</span> <strong>/api/analyze-contract</strong>
            <p>Comprehensive contract clause extraction and risk analysis</p>
        </div>
        
        <div class="endpoint">
            <span class="method post">POST</span> <strong>/api/verify-citation</strong>
            <p>Verify single citation with detailed analysis</p>
        </div>
        
        <div class="endpoint">
            <span class="method post">POST</span> <strong>/api/scan-privilege</strong>
            <p>Scan for privileged content with detailed report</p>
        </div>
        
        <div class="endpoint">
            <span class="method post">POST</span> <strong>/api/find-similar-cases</strong>
            <p>Find similar cases using vector similarity</p>
        </div>
        
        <div class="endpoint">
            <span class="method get">GET</span> <strong>/api/citation-graph</strong>
            <p>Get citation graph with PageRank analysis</p>
        </div>
        
        <div class="endpoint">
            <span class="method get">GET</span> <strong>/api/citation-influence/{case_id}</strong>
            <p>Get detailed influence metrics for a case</p>
        </div>
        
        <div class="endpoint">
            <span class="method post">POST</span> <strong>/api/batch-verify</strong>
            <p>Verify multiple citations at once</p>
        </div>
        
        <div class="endpoint">
            <span class="method get">GET</span> <strong>/api/audit/history</strong>
            <p>Get audit trail history</p>
        </div>
        
        <p style="margin-top: 2rem;"><a href="/docs" style="color: #059669; font-weight: bold;">📖 Interactive API Documentation (Swagger UI)</a></p>
        <p><a href="/redoc" style="color: #059669;">📚 API Documentation (ReDoc)</a></p>
        
        <hr style="margin: 2rem 0; border: none; border-top: 1px solid #e2e8f0;">
        <p style="color: #94a3b8; font-size: 14px;">Kavach v2.0.0 — Built for WashU Law Vibe Coding Challenge 2026</p>
    </body>
    </html>
    """

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "kavach", "version": "2.0.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

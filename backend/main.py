"""Kavach — Legal AI Trust Platform

Main FastAPI application with complete feature set.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import time
import json

from ai.kavach_engine import KavachEngine
from ai.citation_verifier import CitationVerifier
from ai.privilege_shield import PrivilegeShield
from ai.confidence_scorer import ConfidenceScorer
from ai.audit_trail import AuditTrail
from ai.case_predictor import CasePredictor

app = FastAPI(
    title="Kavach",
    description="Legal AI Trust Platform — Making AI safe, reliable, and defensible for legal practice",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response models
class AnalyzeRequest(BaseModel):
    text: str
    user_id: Optional[str] = None
    options: Optional[Dict[str, Any]] = None

class VerifyCitationRequest(BaseModel):
    citation: str

class ScanPrivilegeRequest(BaseModel):
    text: str

class PredictCaseRequest(BaseModel):
    case_type: Optional[str] = None
    facts: Dict[str, Any]

class GenerateDocumentRequest(BaseModel):
    document_type: str
    facts: Dict[str, Any]
    jurisdiction: Optional[str] = "Maharashtra"

# Health check
@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Kavach API</title>
        <style>
            body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
            h1 { color: #059669; }
            .endpoint { background: #f3f4f6; padding: 15px; margin: 10px 0; border-radius: 8px; }
            .method { color: white; padding: 3px 8px; border-radius: 4px; font-weight: bold; }
            .post { background: #3b82f6; }
            .get { background: #22c55e; }
        </style>
    </head>
    <body>
        <h1>🛡️ Kavach — Legal AI Trust Platform</h1>
        <p>Making AI safe, reliable, and defensible for legal practice</p>
        
        <h2>API Endpoints</h2>
        
        <div class="endpoint">
            <span class="method post">POST</span> <strong>/analyze</strong>
            <p>Complete trust analysis: citations + privilege + confidence scoring</p>
        </div>
        
        <div class="endpoint">
            <span class="method post">POST</span> <strong>/verify-citation</strong>
            <p>Verify a single case citation</p>
        </div>
        
        <div class="endpoint">
            <span class="method post">POST</span> <strong>/scan-privilege</strong>
            <p>Scan text for privileged content</p>
        </div>
        
        <div class="endpoint">
            <span class="method post">POST</span> <strong>/predict-case</strong>
            <p>Predict case outcome based on facts</p>
        </div>
        
        <div class="endpoint">
            <span class="method get">GET</span> <strong>/audit/history</strong>
            <p>Get audit trail history</p>
        </div>
        
        <div class="endpoint">
            <span class="method get">GET</span> <strong>/audit/report</strong>
            <p>Generate audit report</p>
        </div>
        
        <p><a href="/docs">📖 Interactive API Documentation (Swagger)</a></p>
        <p><a href="/redoc">📚 API Documentation (ReDoc)</a></p>
    </body>
    </html>
    """

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "kavach", "version": "1.0.0"}

# Main analysis endpoint
@app.post("/analyze")
async def analyze_text(request: AnalyzeRequest):
    """Complete Kavach analysis: citations + privilege + confidence + prediction"""
    engine = KavachEngine()
    result = await engine.analyze(request.text, request.user_id)
    
    # Try to predict case type if requested
    prediction = None
    if request.options and request.options.get("predict_case"):
        predictor = CasePredictor()
        facts = {"text": request.text, **request.options.get("facts", {})}
        prediction = predictor.predict(request.options.get("case_type", ""), facts)
    
    return {
        "input_text": result.input_text,
        "citations": [
            {
                "citation": c.citation,
                "is_valid": c.is_valid,
                "confidence": c.confidence,
                "verified_source": c.verified_source,
                "case_title": c.case_title,
                "year": c.year,
                "court": c.court,
                "actual_text": c.actual_text,
            }
            for c in result.citations
        ],
        "privilege_detections": [
            {
                "text": d.text,
                "start": d.start,
                "end": d.end,
                "privilege_type": d.privilege_type.value,
                "confidence": d.confidence,
                "suggested_redaction": d.suggested_redaction,
                "severity": d.severity,
            }
            for d in result.privilege_detections
        ],
        "confidence_score": {
            "overall": result.confidence_score.overall,
            "citation_accuracy": result.confidence_score.citation_accuracy,
            "source_reliability": result.confidence_score.source_reliability,
            "privilege_safety": result.confidence_score.privilege_safety,
            "factors": result.confidence_score.factors,
        },
        "redacted_text": result.redacted_text,
        "audit_entry_id": result.audit_entry_id,
        "processing_time_ms": result.processing_time_ms,
        "recommendation": result.recommendation,
        "prediction": {
            "case_type": prediction.case_type,
            "win_probability": prediction.win_probability,
            "likely_outcome": prediction.likely_outcome,
            "timeline_months": prediction.timeline_months,
            "risk_factors": prediction.risk_factors,
            "similar_cases": prediction.similar_cases,
        } if prediction else None,
    }

# Single citation verification
@app.post("/verify-citation")
async def verify_citation(request: VerifyCitationRequest):
    """Verify a single citation"""
    verifier = CitationVerifier()
    result = await verifier.verify_citation(request.citation)
    
    return {
        "citation": result.citation,
        "is_valid": result.is_valid,
        "confidence": result.confidence,
        "verified_source": result.verified_source,
        "case_title": result.case_title,
        "year": result.year,
        "court": result.court,
        "actual_text": result.actual_text,
    }

# Privilege scanning
@app.post("/scan-privilege")
async def scan_privilege(request: ScanPrivilegeRequest):
    """Scan text for privileged content"""
    shield = PrivilegeShield()
    detections = shield.scan(request.text)
    report = shield.generate_report(request.text, detections)
    
    return {
        "detections": [
            {
                "text": d.text,
                "start": d.start,
                "end": d.end,
                "privilege_type": d.privilege_type.value,
                "confidence": d.confidence,
                "suggested_redaction": d.suggested_redaction,
                "severity": d.severity,
            }
            for d in detections
        ],
        "report": report,
    }

# Case prediction
@app.post("/predict-case")
async def predict_case(request: PredictCaseRequest):
    """Predict case outcome"""
    predictor = CasePredictor()
    prediction = predictor.predict(request.case_type or "", request.facts)
    
    return {
        "case_type": prediction.case_type,
        "win_probability": prediction.win_probability,
        "likely_outcome": prediction.likely_outcome,
        "key_factors": prediction.key_factors,
        "remedies": prediction.remedies,
        "timeline_months": prediction.timeline_months,
        "risk_factors": prediction.risk_factors,
        "similar_cases": prediction.similar_cases,
        "confidence": prediction.confidence,
    }

# Audit endpoints
@app.get("/audit/history")
async def get_audit_history(action: Optional[str] = None, limit: int = 100):
    """Get audit trail history"""
    trail = AuditTrail()
    entries = trail.get_history(action=action, limit=limit)
    
    return {
        "entries": [
            {
                "entry_id": e.entry_id,
                "timestamp": e.timestamp,
                "action": e.action,
                "status": e.status,
                "duration_ms": e.duration_ms,
            }
            for e in entries
        ]
    }

@app.get("/audit/report")
async def get_audit_report():
    """Generate audit report"""
    trail = AuditTrail()
    report = trail.generate_report()
    return report

# Batch verification
@app.post("/batch-verify")
async def batch_verify_citations(citations: List[str]):
    """Verify multiple citations at once"""
    verifier = CitationVerifier()
    results = await verifier.verify_citations(citations)
    
    return {
        "total": len(results),
        "verified": sum(1 for r in results if r.is_valid),
        "unverified": sum(1 for r in results if not r.is_valid),
        "results": [
            {
                "citation": r.citation,
                "is_valid": r.is_valid,
                "confidence": r.confidence,
                "case_title": r.case_title,
            }
            for r in results
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

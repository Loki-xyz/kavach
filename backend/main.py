"""Kavach — Legal AI Trust Platform

Main FastAPI application entry point.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import time

from ai.kavach_engine import KavachEngine
from ai.citation_verifier import CitationVerifier
from ai.privilege_shield import PrivilegeShield
from ai.confidence_scorer import ConfidenceScorer
from ai.audit_trail import AuditTrail

app = FastAPI(
    title="Kavach",
    description="Legal AI Trust Platform — Making AI safe, reliable, and defensible for legal practice",
    version="0.1.0",
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

class VerifyCitationRequest(BaseModel):
    citation: str

class ScanPrivilegeRequest(BaseModel):
    text: str

class CitationResponse(BaseModel):
    citation: str
    is_valid: bool
    confidence: float
    verified_source: Optional[str]
    case_title: Optional[str]
    year: Optional[int]
    court: Optional[str]

class PrivilegeDetectionResponse(BaseModel):
    text: str
    start: int
    end: int
    privilege_type: str
    confidence: float
    suggested_redaction: str

class AnalyzeResponse(BaseModel):
    input_text: str
    citations: List[CitationResponse]
    privilege_detections: List[PrivilegeDetectionResponse]
    confidence_score: dict
    redacted_text: Optional[str]
    audit_entry_id: str
    processing_time_ms: float
    recommendation: str

@app.get("/")
async def root():
    return {
        "name": "Kavach",
        "tagline": "Legal AI Trust Platform",
        "description": "Making AI safe, reliable, and defensible for legal practice",
        "version": "0.1.0",
    }

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "kavach"}

@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze_text(request: AnalyzeRequest):
    """Complete Kavach analysis: citations + privilege + confidence"""
    engine = KavachEngine()
    result = await engine.analyze(request.text, request.user_id)
    
    return AnalyzeResponse(
        input_text=result.input_text,
        citations=[
            CitationResponse(
                citation=c.citation,
                is_valid=c.is_valid,
                confidence=c.confidence,
                verified_source=c.verified_source,
                case_title=c.case_title,
                year=c.year,
                court=c.court,
            )
            for c in result.citations
        ],
        privilege_detections=[
            PrivilegeDetectionResponse(
                text=d.text,
                start=d.start,
                end=d.end,
                privilege_type=d.privilege_type.value,
                confidence=d.confidence,
                suggested_redaction=d.suggested_redaction,
            )
            for d in result.privilege_detections
        ],
        confidence_score={
            "overall": result.confidence_score.overall,
            "citation_accuracy": result.confidence_score.citation_accuracy,
            "source_reliability": result.confidence_score.source_reliability,
            "privilege_safety": result.confidence_score.privilege_safety,
            "factors": result.confidence_score.factors,
        },
        redacted_text=result.redacted_text,
        audit_entry_id=result.audit_entry_id,
        processing_time_ms=result.processing_time_ms,
        recommendation=result.recommendation,
    )

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
            }
            for d in detections
        ],
        "report": report,
    }

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

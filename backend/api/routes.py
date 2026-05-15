"""API Routes — Complete Kavach API with all features"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import time

from ai.kavach_engine import KavachEngine
from ai.citation_verifier import CitationVerifier
from ai.privilege_shield import PrivilegeShield
from ai.confidence_scorer import ConfidenceScorer
from ai.audit_trail import AuditTrail
from ai.vector_store import create_legal_vector_store
from ai.citation_graph import create_indian_citation_graph
from ai.verification_pipeline import VerificationPipeline
from ai.contract_analyzer import ContractAnalyzer

router = APIRouter()

# Request/Response models
class AnalyzeRequest(BaseModel):
    text: str
    user_id: Optional[str] = None
    options: Optional[Dict[str, Any]] = None

class VerifyCitationRequest(BaseModel):
    citation: str

class ScanPrivilegeRequest(BaseModel):
    text: str

class ContractAnalysisRequest(BaseModel):
    contract_text: str
    contract_name: Optional[str] = "Contract"

class SimilarCasesRequest(BaseModel):
    query: str
    top_k: Optional[int] = 5

class CitationGraphRequest(BaseModel):
    case_id: str

# Health check
@router.get("/")
async def root():
    return {
        "name": "Kavach",
        "tagline": "Legal AI Trust Platform",
        "version": "2.0.0",
        "features": [
            "Citation Verification",
            "Privilege Shield",
            "Confidence Scoring",
            "Multi-Agent Verification",
            "Vector Similarity Search",
            "Citation Graph Analysis",
            "Contract Clause Extraction",
            "Advanced RAG",
        ]
    }

@router.get("/health")
async def health():
    return {"status": "healthy", "service": "kavach", "version": "2.0.0"}

# Main analysis endpoint
@router.post("/analyze")
async def analyze_text(request: AnalyzeRequest):
    """Complete Kavach analysis with all sophisticated features"""
    engine = KavachEngine()
    result = await engine.analyze(request.text, request.user_id, request.options)
    
    response = {
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
    }
    
    # Add verification pipeline results
    if result.verification_result:
        response["verification"] = {
            "overall_status": result.verification_result.overall_status.value,
            "overall_confidence": result.verification_result.overall_confidence,
            "total_findings": result.verification_result.total_findings,
            "critical_findings": result.verification_result.critical_findings,
            "agent_votes": [
                {
                    "agent": v.agent_name,
                    "status": v.status.value,
                    "confidence": v.confidence,
                    "findings_count": len(v.findings),
                }
                for v in result.verification_result.votes
            ],
            "recommendations": result.verification_result.recommendations,
        }
    
    # Add similar cases
    if result.similar_cases:
        response["similar_cases"] = result.similar_cases
    
    # Add citation influence
    if result.citation_influence:
        response["citation_influence"] = result.citation_influence
    
    # Add contract analysis
    if result.contract_analysis:
        response["contract_analysis"] = {
            "total_clauses": result.contract_analysis.total_clauses,
            "clauses_by_type": result.contract_analysis.clauses_by_type,
            "risk_summary": result.contract_analysis.risk_summary,
            "overall_risk": result.contract_analysis.overall_risk.value,
            "key_obligations": result.contract_analysis.key_obligations[:5],
            "critical_dates": result.contract_analysis.critical_dates,
            "recommendations": result.contract_analysis.recommendations,
        }
    
    # Add RAG results
    if result.rag_results:
        response["rag_results"] = result.rag_results
    
    return response

# Single citation verification
@router.post("/verify-citation")
async def verify_citation(request: VerifyCitationRequest):
    """Verify a single citation with detailed analysis"""
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
@router.post("/scan-privilege")
async def scan_privilege(request: ScanPrivilegeRequest):
    """Scan text for privileged content with detailed report"""
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

# Contract analysis
@router.post("/analyze-contract")
async def analyze_contract(request: ContractAnalysisRequest):
    """Perform comprehensive contract analysis"""
    analyzer = ContractAnalyzer()
    analysis = analyzer.analyze_contract(request.contract_text, request.contract_name)
    
    return {
        "contract_name": analysis.contract_name,
        "total_clauses": analysis.total_clauses,
        "clauses_by_type": analysis.clauses_by_type,
        "risk_summary": analysis.risk_summary,
        "overall_risk": analysis.overall_risk.value,
        "key_obligations": analysis.key_obligations,
        "critical_dates": analysis.critical_dates,
        "recommendations": analysis.recommendations,
        "extracted_clauses": [
            {
                "clause_type": c.clause_type.value,
                "text": c.text[:300],
                "risk_level": c.risk_level.value,
                "risk_factors": c.risk_factors,
                "key_terms": c.key_terms,
            }
            for c in analysis.extracted_clauses
        ],
    }

# Similar cases search
@router.post("/find-similar-cases")
async def find_similar_cases(request: SimilarCasesRequest):
    """Find similar cases using vector similarity"""
    store = create_legal_vector_store()
    results = store.find_similar_cases(request.query, top_k=request.top_k)
    
    return {
        "query": request.query,
        "results": [
            {
                "id": r.id,
                "title": r.metadata.get("title", "Unknown"),
                "citation": r.metadata.get("citation", ""),
                "similarity": r.similarity,
                "area": r.metadata.get("area", ""),
                "court": r.metadata.get("court", ""),
                "year": r.metadata.get("year", 0),
            }
            for r in results
        ],
    }

# Citation graph analysis
@router.get("/citation-graph")
async def get_citation_graph():
    """Get the full citation graph"""
    graph = create_indian_citation_graph()
    
    # Calculate PageRank
    pagerank = graph.calculate_pagerank()
    
    # Detect communities
    communities = graph.detect_communities()
    
    return {
        "nodes": len(graph.graph.nodes),
        "edges": len(graph.graph.edges),
        "pagerank": {k: round(v, 4) for k, v in pagerank.items()},
        "communities": communities,
        "influential_cases": [
            {
                "id": c.id,
                "title": c.title,
                "citation": c.citation,
                "pagerank": c.pagerank_score,
            }
            for c in graph.get_influential_cases(5)
        ],
    }

# Citation influence analysis
@router.get("/citation-influence/{case_id}")
async def get_citation_influence(case_id: str):
    """Get detailed influence metrics for a case"""
    graph = create_indian_citation_graph()
    graph.calculate_pagerank()
    
    influence = graph.get_citation_influence(case_id)
    
    if not influence:
        raise HTTPException(status_code=404, detail="Case not found")
    
    return influence

# Multi-agent verification
@router.post("/verify")
async def verify_text(request: ScanPrivilegeRequest):
    """Run multi-agent verification pipeline"""
    pipeline = VerificationPipeline()
    result = pipeline.verify(request.text)
    
    return {
        "overall_status": result.overall_status.value,
        "overall_confidence": result.overall_confidence,
        "total_findings": result.total_findings,
        "critical_findings": result.critical_findings,
        "agent_votes": [
            {
                "agent": v.agent_name,
                "status": v.status.value,
                "confidence": v.confidence,
                "findings": v.findings,
                "suggestions": v.suggestions,
                "processing_time_ms": v.processing_time_ms,
            }
            for v in result.votes
        ],
        "recommendations": result.recommendations,
        "processing_time_ms": result.processing_time_ms,
    }

# Batch verification
@router.post("/batch-verify")
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

# Audit endpoints
@router.get("/audit/history")
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

@router.get("/audit/report")
async def get_audit_report():
    """Generate audit report"""
    trail = AuditTrail()
    report = trail.generate_report()
    return report

"""Kavach Engine — Main orchestration layer

Combines citation verification, privilege scanning, confidence scoring,
and audit logging into a unified trust engine.
"""

import time
from typing import Dict, List, Optional
from dataclasses import dataclass

from .citation_verifier import CitationVerifier, CitationResult
from .privilege_shield import PrivilegeShield, PrivilegeDetection
from .confidence_scorer import ConfidenceScorer, ConfidenceScore
from .audit_trail import AuditTrail

@dataclass
class KavachResult:
    """Complete result from Kavach analysis"""
    input_text: str
    citations: List[CitationResult]
    privilege_detections: List[PrivilegeDetection]
    confidence_score: ConfidenceScore
    redacted_text: Optional[str]
    audit_entry_id: str
    processing_time_ms: float
    recommendation: str

class KavachEngine:
    """Main trust engine that orchestrates all components"""
    
    def __init__(self):
        self.citation_verifier = CitationVerifier()
        self.privilege_shield = PrivilegeShield()
        self.confidence_scorer = ConfidenceScorer()
        self.audit_trail = AuditTrail()
    
    async def analyze(self, text: str, user_id: Optional[str] = None) -> KavachResult:
        """Perform complete Kavach analysis on text"""
        start_time = time.time()
        
        # 1. Extract and verify citations
        citations = await self._verify_citations(text)
        
        # 2. Scan for privilege issues
        privilege_detections = self._scan_privilege(text)
        
        # 3. Redact privileged content
        redacted_text, _ = self.privilege_shield.redact(text, privilege_detections)
        
        # 4. Calculate confidence score
        confidence_score = self._calculate_confidence(
            text, citations, privilege_detections
        )
        
        # 5. Generate recommendation
        recommendation = self.confidence_scorer.get_recommendation(confidence_score)
        
        # 6. Log to audit trail
        processing_time_ms = (time.time() - start_time) * 1000
        
        audit_entry = self.audit_trail.log(
            action="kavach_analyze",
            input_data={"text_length": len(text)},
            output_data={
                "citations_verified": sum(1 for c in citations if c.is_valid),
                "privilege_detections": len(privilege_detections),
                "confidence_score": confidence_score.overall,
            },
            user_id=user_id,
            details={
                "citation_count": len(citations),
                "privilege_count": len(privilege_detections),
            },
            duration_ms=processing_time_ms,
        )
        
        return KavachResult(
            input_text=text,
            citations=citations,
            privilege_detections=privilege_detections,
            confidence_score=confidence_score,
            redacted_text=redacted_text,
            audit_entry_id=audit_entry.entry_id,
            processing_time_ms=processing_time_ms,
            recommendation=recommendation,
        )
    
    async def _verify_citations(self, text: str) -> List[CitationResult]:
        """Extract and verify citations from text"""
        import re
        
        # Common citation patterns
        citation_patterns = [
            r"\d{4}\s+SCC\s+\d+\s+SC\s+\d+",
            r"\d{4}\s+AIR\s+\w+\s+\d+",
            r"\d{4}\s+\w+\s+HC\s+\d+",
        ]
        
        citations = []
        for pattern in citation_patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                result = await self.citation_verifier.verify_citation(match)
                citations.append(result)
        
        return citations
    
    def _scan_privilege(self, text: str) -> List[PrivilegeDetection]:
        """Scan text for privileged content"""
        return self.privilege_shield.scan(text)
    
    def _calculate_confidence(
        self,
        text: str,
        citations: List[CitationResult],
        privilege_detections: List[PrivilegeDetection],
    ) -> ConfidenceScore:
        """Calculate overall confidence score"""
        # Count verified citations
        verified = sum(1 for c in citations if c.is_valid)
        total = len(citations)
        
        # Count privilege detections by confidence
        high_conf_detections = sum(
            1 for d in privilege_detections if d.confidence > 0.8
        )
        
        return self.confidence_scorer.calculate(
            text=text,
            citations_verified=verified,
            citations_total=total,
            sources_found=verified,  # Using verified citations as sources
            sources_total=total,
            privilege_detections=len(privilege_detections),
            high_confidence_detections=high_conf_detections,
        )

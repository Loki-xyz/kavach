"""Confidence Scorer — Calculates reliability scores for AI outputs

Every AI-generated content gets a confidence score based on:
- Source verification
- Citation validity
- Privilege risk
- Historical accuracy
"""

from typing import List, Dict, Optional
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class ConfidenceScore:
    """Confidence score for AI-generated content"""
    overall: float  # 0-1
    citation_accuracy: float  # 0-1
    source_reliability: float  # 0-1
    privilege_safety: float  # 0-1
    factors: List[Dict] = field(default_factory=list)
    calculated_at: str = ""

    def __post_init__(self):
        if not self.calculated_at:
            self.calculated_at = datetime.now().isoformat()

class ConfidenceScorer:
    """Calculates confidence scores for AI outputs"""
    
    def __init__(self):
        # Weight factors for overall score
        self.weights = {
            "citation_accuracy": 0.4,
            "source_reliability": 0.3,
            "privilege_safety": 0.3,
        }
    
    def calculate(
        self,
        text: str,
        citations_verified: int = 0,
        citations_total: int = 0,
        sources_found: int = 0,
        sources_total: int = 0,
        privilege_detections: int = 0,
        high_confidence_detections: int = 0,
    ) -> ConfidenceScore:
        """Calculate overall confidence score"""
        
        # Citation accuracy score
        if citations_total > 0:
            citation_accuracy = citations_verified / citations_total
        else:
            citation_accuracy = 1.0  # No citations = no risk
        
        # Source reliability score
        if sources_total > 0:
            source_reliability = sources_found / sources_total
        else:
            source_reliability = 0.8  # Default for unsourced content
        
        # Privilege safety score (inverse of risk)
        if privilege_detections > 0:
            # Lower score if high-confidence privilege detections
            privilege_safety = 1.0 - (high_confidence_detections / privilege_detections)
        else:
            privilege_safety = 1.0  # No privilege issues
        
        # Calculate overall score
        overall = (
            citation_accuracy * self.weights["citation_accuracy"] +
            source_reliability * self.weights["source_reliability"] +
            privilege_safety * self.weights["privilege_safety"]
        )
        
        # Generate factors for transparency
        factors = []
        
        if citations_total > 0:
            factors.append({
                "name": "Citation Verification",
                "score": citation_accuracy,
                "details": f"{citations_verified}/{citations_total} citations verified",
                "impact": "high" if citation_accuracy < 0.8 else "low"
            })
        
        if sources_total > 0:
            factors.append({
                "name": "Source Reliability",
                "score": source_reliability,
                "details": f"{sources_found}/{sources_total} sources found",
                "impact": "medium"
            })
        
        if privilege_detections > 0:
            factors.append({
                "name": "Privilege Safety",
                "score": privilege_safety,
                "details": f"{privilege_detections} privilege issues detected",
                "impact": "high" if privilege_safety < 0.8 else "medium"
            })
        
        return ConfidenceScore(
            overall=overall,
            citation_accuracy=citation_accuracy,
            source_reliability=source_reliability,
            privilege_safety=privilege_safety,
            factors=factors
        )
    
    def get_recommendation(self, score: ConfidenceScore) -> str:
        """Get human-readable recommendation based on score"""
        if score.overall >= 0.9:
            return "HIGH CONFIDENCE: This content is reliable and safe to use."
        elif score.overall >= 0.7:
            return "MODERATE CONFIDENCE: Review flagged issues before using."
        elif score.overall >= 0.5:
            return "LOW CONFIDENCE: Significant issues detected. Manual review required."
        else:
            return "WARNING: Critical issues detected. Do not use without thorough review."
    
    def get_risk_factors(self, score: ConfidenceScore) -> List[str]:
        """Get list of risk factors"""
        risks = []
        
        if score.citation_accuracy < 0.8:
            risks.append(f"Citation accuracy low ({score.citation_accuracy:.0%})")
        
        if score.source_reliability < 0.7:
            risks.append(f"Source reliability low ({score.source_reliability:.0%})")
        
        if score.privilege_safety < 0.8:
            risks.append(f"Privilege risk detected ({score.privilege_safety:.0%})")
        
        return risks

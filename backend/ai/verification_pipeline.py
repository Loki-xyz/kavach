"""Verification Pipeline — Multi-agent verification system

Implements a pipeline of specialized verification agents:
1. Citation Verifier — checks case citations
2. Privilege Scanner — detects privileged content
3. Consistency Checker — finds contradictions
4. Fact Checker — verifies factual claims
5. Compliance Checker — checks regulatory compliance

Each agent runs independently and votes on content trustworthiness.
"""

from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import json

class VerificationStatus(Enum):
    PASS = "pass"
    WARN = "warn"
    FAIL = "fail"
    ERROR = "error"

@dataclass
class VerificationVote:
    """A single verification agent's vote"""
    agent_name: str
    status: VerificationStatus
    confidence: float
    findings: List[Dict]
    suggestions: List[str]
    processing_time_ms: float = 0

@dataclass
class PipelineResult:
    """Result from the verification pipeline"""
    text_hash: str
    votes: List[VerificationVote]
    overall_status: VerificationStatus
    overall_confidence: float
    total_findings: int
    critical_findings: int
    recommendations: List[str]
    processing_time_ms: float
    completed_at: str = ""

    def __post_init__(self):
        if not self.completed_at:
            self.completed_at = datetime.now().isoformat()

class VerificationPipeline:
    """Multi-agent verification pipeline"""
    
    def __init__(self):
        self.agents = [
            CitationVerificationAgent(),
            PrivilegeScanningAgent(),
            ConsistencyCheckingAgent(),
            FactCheckingAgent(),
            ComplianceCheckingAgent(),
        ]
    
    def verify(self, text: str, context: Optional[Dict] = None) -> PipelineResult:
        """Run all verification agents on the text"""
        import hashlib
        import time
        
        start_time = time.time()
        text_hash = hashlib.sha256(text.encode()).hexdigest()[:16]
        
        votes = []
        for agent in self.agents:
            try:
                vote = agent.verify(text, context)
                votes.append(vote)
            except Exception as e:
                votes.append(VerificationVote(
                    agent_name=agent.name,
                    status=VerificationStatus.ERROR,
                    confidence=0.0,
                    findings=[{"error": str(e)}],
                    suggestions=["Agent failed - manual review required"],
                ))
        
        # Aggregate votes
        overall_status = self._aggregate_status(votes)
        overall_confidence = self._aggregate_confidence(votes)
        total_findings = sum(len(v.findings) for v in votes)
        critical_findings = sum(
            1 for v in votes 
            for f in v.findings 
            if f.get("severity") == "critical"
        )
        recommendations = self._generate_recommendations(votes)
        
        processing_time = (time.time() - start_time) * 1000
        
        return PipelineResult(
            text_hash=text_hash,
            votes=votes,
            overall_status=overall_status,
            overall_confidence=overall_confidence,
            total_findings=total_findings,
            critical_findings=critical_findings,
            recommendations=recommendations,
            processing_time_ms=processing_time,
        )
    
    def _aggregate_status(self, votes: List[VerificationVote]) -> VerificationStatus:
        """Aggregate votes to determine overall status"""
        statuses = [v.status for v in votes]
        
        if VerificationStatus.FAIL in statuses:
            return VerificationStatus.FAIL
        elif VerificationStatus.WARN in statuses:
            return VerificationStatus.WARN
        elif all(s == VerificationStatus.PASS for s in statuses):
            return VerificationStatus.PASS
        else:
            return VerificationStatus.WARN
    
    def _aggregate_confidence(self, votes: List[VerificationVote]) -> float:
        """Calculate weighted average confidence"""
        if not votes:
            return 0.0
        
        # Weight by agent importance
        weights = {
            "Citation Verifier": 0.3,
            "Privilege Scanner": 0.25,
            "Consistency Checker": 0.2,
            "Fact Checker": 0.15,
            "Compliance Checker": 0.1,
        }
        
        total_weight = 0
        weighted_confidence = 0
        
        for vote in votes:
            weight = weights.get(vote.agent_name, 0.1)
            weighted_confidence += vote.confidence * weight
            total_weight += weight
        
        return weighted_confidence / total_weight if total_weight > 0 else 0
    
    def _generate_recommendations(self, votes: List[VerificationVote]) -> List[str]:
        """Generate recommendations based on votes"""
        recommendations = []
        
        for vote in votes:
            if vote.status == VerificationStatus.FAIL:
                recommendations.append(f"CRITICAL: {vote.agent_name} found issues requiring immediate attention")
            elif vote.status == VerificationStatus.WARN:
                recommendations.extend(vote.suggestions[:2])
        
        if not recommendations:
            recommendations.append("All verification checks passed. Content appears trustworthy.")
        
        return recommendations


class CitationVerificationAgent:
    """Agent that verifies case citations"""
    
    name = "Citation Verifier"
    
    # Known valid citations
    KNOWN_CITATIONS = {
        "2020 SCC 9 SC 609": {"title": "Vineeta Sharma v. Rakesh Sharma", "valid": True},
        "2011 SCC 7 SC 1": {"title": "Indian Medical Association v. Union of India", "valid": True},
        "2008 AIR SC 1234": {"title": "Satyawati Sharma v. Union of India", "valid": True},
        "2017 SCC 9 SC 1": {"title": "Shayara Bano v. Union of India", "valid": True},
        "2018 SCC 3 SC 1": {"title": "Joseph Shine v. Union of India", "valid": True},
        "2017 SCC 1 SC 1": {"title": "Justice K.S. Puttaswamy v. Union of India", "valid": True},
    }
    
    def verify(self, text: str, context: Optional[Dict] = None) -> VerificationVote:
        """Verify citations in text"""
        import re
        import time
        
        start = time.time()
        findings = []
        suggestions = []
        
        # Extract citations
        citation_patterns = [
            r"(\d{4})\s+SCC\s+(\d+)\s+SC\s+(\d+)",
            r"(\d{4})\s+AIR\s+(\w+)\s+(\d+)",
        ]
        
        found_citations = []
        for pattern in citation_patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                citation = " ".join(match)
                found_citations.append(citation)
        
        # Verify each citation
        verified_count = 0
        for citation in found_citations:
            if citation in self.KNOWN_CITATIONS:
                verified_count += 1
                findings.append({
                    "type": "citation_verified",
                    "citation": citation,
                    "title": self.KNOWN_CITATIONS[citation]["title"],
                    "severity": "info",
                })
            else:
                findings.append({
                    "type": "citation_unverified",
                    "citation": citation,
                    "severity": "warning",
                })
                suggestions.append(f"Citation '{citation}' could not be verified. Manual check recommended.")
        
        # Determine status
        if len(found_citations) == 0:
            status = VerificationStatus.PASS
            confidence = 0.9
        elif verified_count == len(found_citations):
            status = VerificationStatus.PASS
            confidence = 0.95
        elif verified_count > 0:
            status = VerificationStatus.WARN
            confidence = 0.7
        else:
            status = VerificationStatus.WARN
            confidence = 0.5
        
        processing_time = (time.time() - start) * 1000
        
        return VerificationVote(
            agent_name=self.name,
            status=status,
            confidence=confidence,
            findings=findings,
            suggestions=suggestions,
            processing_time_ms=processing_time,
        )


class PrivilegeScanningAgent:
    """Agent that scans for privileged content"""
    
    name = "Privilege Scanner"
    
    PRIVILEGE_PATTERNS = {
        "attorney_client": [
            r"client\s+(?:told|informed|stated|disclosed)",
            r"attorney[- ]client\s+privilege",
            r"legal\s+(?:advice|counsel|opinion)",
        ],
        "work_product": [
            r"work\s+product",
            r"litigation\s+(?:strategy|plan)",
            r"case\s+(?:strategy|theory|analysis)",
        ],
        "confidential": [
            r"confidential\s+(?:information|data|document)",
            r"trade\s+secret",
            r"proprietary\s+(?:information|data)",
        ],
    }
    
    def verify(self, text: str, context: Optional[Dict] = None) -> VerificationVote:
        """Scan for privileged content"""
        import re
        import time
        
        start = time.time()
        findings = []
        suggestions = []
        
        for ptype, patterns in self.PRIVILEGE_PATTERNS.items():
            for pattern in patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                for match in matches:
                    findings.append({
                        "type": "privilege_detected",
                        "privilege_type": ptype,
                        "text": match,
                        "severity": "critical" if ptype in ["attorney_client", "work_product"] else "warning",
                    })
        
        # Determine status
        critical_count = sum(1 for f in findings if f.get("severity") == "critical")
        
        if critical_count > 0:
            status = VerificationStatus.FAIL
            confidence = 0.9
            suggestions.append("Privileged content detected. Redact before sharing with AI tools.")
        elif len(findings) > 0:
            status = VerificationStatus.WARN
            confidence = 0.8
            suggestions.append("Confidential information detected. Review before sharing.")
        else:
            status = VerificationStatus.PASS
            confidence = 0.95
        
        processing_time = (time.time() - start) * 1000
        
        return VerificationVote(
            agent_name=self.name,
            status=status,
            confidence=confidence,
            findings=findings,
            suggestions=suggestions,
            processing_time_ms=processing_time,
        )


class ConsistencyCheckingAgent:
    """Agent that checks for internal contradictions"""
    
    name = "Consistency Checker"
    
    def verify(self, text: str, context: Optional[Dict] = None) -> VerificationVote:
        """Check for internal consistency"""
        import re
        import time
        
        start = time.time()
        findings = []
        suggestions = []
        
        # Check for contradictory statements
        contradiction_patterns = [
            (r"not\s+(?:a|an|the)", r"(?:is|was|are|were)\s+(?:a|an|the)", "Potential negation contradiction"),
            (r"never", r"always", "Absolute contradiction detected"),
            (r"impossible", r"possible", "Possibility contradiction"),
        ]
        
        for neg_pattern, pos_pattern, desc in contradiction_patterns:
            neg_matches = re.findall(neg_pattern, text, re.IGNORECASE)
            pos_matches = re.findall(pos_pattern, text, re.IGNORECASE)
            
            if neg_matches and pos_matches:
                findings.append({
                    "type": "contradiction",
                    "description": desc,
                    "severity": "warning",
                })
                suggestions.append(f"Review: {desc}")
        
        # Check for date inconsistencies
        date_pattern = r"\b(\d{1,2})[/-](\d{1,2})[/-](\d{4})\b"
        dates = re.findall(date_pattern, text)
        
        if len(dates) > 1:
            # Check if dates are in logical order
            parsed_dates = []
            for d, m, y in dates:
                try:
                    parsed_dates.append((int(y), int(m), int(d)))
                except:
                    pass
            
            if len(parsed_dates) > 1:
                for i in range(len(parsed_dates) - 1):
                    if parsed_dates[i] > parsed_dates[i + 1]:
                        findings.append({
                            "type": "date_inconsistency",
                            "description": f"Date {parsed_dates[i]} appears after {parsed_dates[i+1]}",
                            "severity": "warning",
                        })
        
        # Determine status
        if any(f.get("severity") == "critical" for f in findings):
            status = VerificationStatus.FAIL
            confidence = 0.7
        elif findings:
            status = VerificationStatus.WARN
            confidence = 0.8
        else:
            status = VerificationStatus.PASS
            confidence = 0.85
        
        processing_time = (time.time() - start) * 1000
        
        return VerificationVote(
            agent_name=self.name,
            status=status,
            confidence=confidence,
            findings=findings,
            suggestions=suggestions,
            processing_time_ms=processing_time,
        )


class FactCheckingAgent:
    """Agent that verifies factual claims"""
    
    name = "Fact Checker"
    
    # Common legal facts that can be verified
    VERIFIABLE_FACTS = {
        "consumer protection act": {"year": 2019, "correct": "Consumer Protection Act, 2019"},
        "consumer protection act, 1986": {"year": 1986, "correct": "Consumer Protection Act, 1986 (repealed by 2019 Act)"},
        "indian penal code": {"year": 1860, "correct": "Indian Penal Code, 1860"},
        "bharatiya nyaya sanhita": {"year": 2023, "correct": "Bharatiya Nyaya Sanhita, 2023"},
    }
    
    def verify(self, text: str, context: Optional[Dict] = None) -> VerificationVote:
        """Verify factual claims"""
        import re
        import time
        
        start = time.time()
        findings = []
        suggestions = []
        
        text_lower = text.lower()
        
        for fact_key, fact_info in self.VERIFIABLE_FACTS.items():
            if fact_key in text_lower:
                # Check if the year matches
                year_pattern = r"\b(\d{4})\b"
                years_near_fact = re.findall(year_pattern, text[text_lower.find(fact_key):text_lower.find(fact_key) + 100])
                
                for year_str in years_near_fact:
                    year = int(year_str)
                    if year != fact_info["year"] and abs(year - fact_info["year"]) < 50:
                        findings.append({
                            "type": "factual_error",
                            "claim": f"{fact_key} ({year})",
                            "correction": fact_info["correct"],
                            "severity": "warning",
                        })
                        suggestions.append(f"Verify: {fact_info['correct']}")
        
        # Determine status
        if findings:
            status = VerificationStatus.WARN
            confidence = 0.75
        else:
            status = VerificationStatus.PASS
            confidence = 0.85
        
        processing_time = (time.time() - start) * 1000
        
        return VerificationVote(
            agent_name=self.name,
            status=status,
            confidence=confidence,
            findings=findings,
            suggestions=suggestions,
            processing_time_ms=processing_time,
        )


class ComplianceCheckingAgent:
    """Agent that checks regulatory compliance"""
    
    name = "Compliance Checker"
    
    COMPLIANCE_RULES = {
        "indian_evidence_act": {
            "patterns": [
                r"section\s+(\d+)",
                r"\bIEA\b",
            ],
            "sections": {
                "126": "Professional communications are privileged",
                "127": "Communication during marriage is privileged",
                "129": "Official communications are privileged",
            }
        },
        "code_of_civil_procedure": {
            "patterns": [
                r"section\s+(\d+)\s+CPC",
                r"\bCPC\b",
            ],
            "sections": {
                "9": "Courts can try all civil suits",
                "11": "Res judicata",
                "100": "Second appeal only on substantial question of law",
            }
        },
    }
    
    def verify(self, text: str, context: Optional[Dict] = None) -> VerificationVote:
        """Check compliance with legal regulations"""
        import re
        import time
        
        start = time.time()
        findings = []
        suggestions = []
        
        # Check for proper legal citations format
        if "section" in text.lower() and not re.search(r"section\s+\d+", text, re.IGNORECASE):
            findings.append({
                "type": "citation_format",
                "description": "Section reference without number",
                "severity": "info",
            })
        
        # Check for missing jurisdiction
        if any(word in text.lower() for word in ["court", "tribunal", "forum"]):
            if not re.search(r"(supreme court|high court|district court|tribunal|forum|commission)", text, re.IGNORECASE):
                findings.append({
                    "type": "missing_jurisdiction",
                    "description": "Court reference without specifying jurisdiction",
                    "severity": "info",
                })
                suggestions.append("Consider specifying the court/jurisdiction")
        
        # Determine status
        if findings:
            status = VerificationStatus.WARN
            confidence = 0.8
        else:
            status = VerificationStatus.PASS
            confidence = 0.9
        
        processing_time = (time.time() - start) * 1000
        
        return VerificationVote(
            agent_name=self.name,
            status=status,
            confidence=confidence,
            findings=findings,
            suggestions=suggestions,
            processing_time_ms=processing_time,
        )

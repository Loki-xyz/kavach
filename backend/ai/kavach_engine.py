"""Kavach Engine — Main orchestration layer with sophisticated analysis

Combines all advanced modules into a unified trust engine:
- Citation verification with graph analysis
- Privilege scanning
- Confidence scoring
- Advanced RAG
- Multi-agent verification
- Contract analysis
- Audit logging
"""

import time
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

from .citation_verifier import CitationVerifier, CitationResult
from .privilege_shield import PrivilegeShield, PrivilegeDetection
from .confidence_scorer import ConfidenceScorer, ConfidenceScore
from .audit_trail import AuditTrail
from .vector_store import LegalVectorStore, create_legal_vector_store
from .citation_graph import CitationGraph, create_indian_citation_graph
from .verification_pipeline import VerificationPipeline, PipelineResult
from .contract_analyzer import ContractAnalyzer, ContractAnalysis

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
    # Advanced features
    verification_result: Optional[PipelineResult] = None
    similar_cases: Optional[List[Dict]] = None
    citation_influence: Optional[Dict] = None
    contract_analysis: Optional[ContractAnalysis] = None
    rag_results: Optional[Dict] = None

class KavachEngine:
    """Main trust engine that orchestrates all components"""
    
    def __init__(self):
        self.citation_verifier = CitationVerifier()
        self.privilege_shield = PrivilegeShield()
        self.confidence_scorer = ConfidenceScorer()
        self.audit_trail = AuditTrail()
        self.vector_store = create_legal_vector_store()
        self.citation_graph = create_indian_citation_graph()
        self.verification_pipeline = VerificationPipeline()
        self.contract_analyzer = ContractAnalyzer()
    
    async def analyze(
        self, 
        text: str, 
        user_id: Optional[str] = None,
        options: Optional[Dict[str, Any]] = None
    ) -> KavachResult:
        """Perform complete Kavach analysis on text"""
        start_time = time.time()
        options = options or {}
        
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
        
        # 5. Run multi-agent verification pipeline
        verification_result = self.verification_pipeline.verify(text)
        
        # 6. Find similar cases using vector store
        similar_cases = self._find_similar_cases(text)
        
        # 7. Analyze citation influence
        citation_influence = self._analyze_citation_influence(citations)
        
        # 8. Analyze contract if applicable
        contract_analysis = None
        if options.get("analyze_contract") or self._is_contract(text):
            contract_analysis = self.contract_analyzer.analyze_contract(text)
        
        # 9. Advanced RAG retrieval
        rag_results = self._advanced_retrieval(text)
        
        # 10. Generate recommendation
        recommendation = self._generate_recommendation(
            confidence_score, verification_result, privilege_detections
        )
        
        # 11. Log to audit trail
        processing_time_ms = (time.time() - start_time) * 1000
        
        audit_entry = self.audit_trail.log(
            action="kavach_analyze",
            input_data={"text_length": len(text)},
            output_data={
                "citations_verified": sum(1 for c in citations if c.is_valid),
                "privilege_detections": len(privilege_detections),
                "confidence_score": confidence_score.overall,
                "verification_status": verification_result.overall_status.value if verification_result else "unknown",
                "similar_cases_found": len(similar_cases) if similar_cases else 0,
            },
            user_id=user_id,
            details={
                "citation_count": len(citations),
                "privilege_count": len(privilege_detections),
                "has_contract_analysis": contract_analysis is not None,
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
            verification_result=verification_result,
            similar_cases=similar_cases,
            citation_influence=citation_influence,
            contract_analysis=contract_analysis,
            rag_results=rag_results,
        )
    
    async def _verify_citations(self, text: str) -> List[CitationResult]:
        """Extract and verify citations from text"""
        import re
        
        # Common citation patterns
        citation_patterns = [
            r"\d{4}\s+SCC\s+\d+\s+SC\s+\d+",
            r"\d{4}\s+AIR\s+\w+\s+\d+",
            r"\d{4}\s+SCR\s+\d+\s+\d+",
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
            sources_found=verified,
            sources_total=total,
            privilege_detections=len(privilege_detections),
            high_confidence_detections=high_conf_detections,
        )
    
    def _find_similar_cases(self, text: str) -> List[Dict]:
        """Find similar cases using vector similarity"""
        results = self.vector_store.find_similar_cases(text, top_k=3)
        
        return [
            {
                "id": r.id,
                "title": r.metadata.get("title", "Unknown"),
                "citation": r.metadata.get("citation", ""),
                "similarity": r.similarity,
                "area": r.metadata.get("area", ""),
            }
            for r in results
        ]
    
    def _analyze_citation_influence(self, citations: List[CitationResult]) -> Dict:
        """Analyze influence of citations using graph analysis"""
        influence_data = {}
        
        for citation in citations:
            # Try to find the case in our graph
            for case_id, case in self.citation_graph.cases.items():
                if citation.case_title and citation.case_title.lower() in case.title.lower():
                    influence = self.citation_graph.get_citation_influence(case_id)
                    influence_data[citation.citation] = {
                        "case_title": case.title,
                        "pagerank": influence.get("pagerank", 0),
                        "cited_by_count": influence.get("cited_by_count", 0),
                        "influence_rank": influence.get("influence_rank", 0),
                    }
                    break
        
        return influence_data
    
    def _is_contract(self, text: str) -> bool:
        """Detect if text is a contract"""
        contract_indicators = [
            "agreement", "contract", "party", "parties",
            "whereas", "now therefore", "in witness whereof",
            "terms and conditions", "obligations",
        ]
        
        text_lower = text.lower()
        matches = sum(1 for indicator in contract_indicators if indicator in text_lower)
        
        return matches >= 3
    
    def _advanced_retrieval(self, text: str) -> Dict:
        """Perform advanced RAG retrieval"""
        try:
            from .advanced_rag import AdvancedRAG
            rag = AdvancedRAG(self.vector_store)
            result = rag.retrieve_with_hyde(text, top_k=3)
            
            return {
                "method": result.method,
                "confidence": result.confidence,
                "results_count": len(result.reranked_docs),
                "hypothetical_doc": result.hypothetical_doc,
            }
        except Exception as e:
            return {"error": str(e)}
    
    def _generate_recommendation(
        self,
        confidence_score: ConfidenceScore,
        verification_result: Optional[PipelineResult],
        privilege_detections: List[PrivilegeDetection],
    ) -> str:
        """Generate comprehensive recommendation"""
        recommendations = []
        
        # Check verification pipeline
        if verification_result:
            if verification_result.overall_status.value == "fail":
                recommendations.append("⚠️ CRITICAL: Verification pipeline found issues requiring immediate attention")
            elif verification_result.overall_status.value == "warn":
                recommendations.append("⚠️ WARNING: Some issues detected - review before using")
            else:
                recommendations.append("✅ All verification checks passed")
        
        # Check confidence score
        if confidence_score.overall >= 0.9:
            recommendations.append("📊 High confidence score - content appears trustworthy")
        elif confidence_score.overall >= 0.7:
            recommendations.append("📊 Moderate confidence - review flagged items")
        else:
            recommendations.append("📊 Low confidence - manual review required")
        
        # Check privilege detections
        critical_priv = [d for d in privilege_detections if d.severity == "high"]
        if critical_priv:
            recommendations.append(f"🔒 {len(critical_priv)} high-risk privilege issues detected - redact before sharing with AI")
        
        return " | ".join(recommendations) if recommendations else "Analysis complete"

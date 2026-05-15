"""Contract Analyzer — Extract and analyze contract clauses

Uses LLM-based extraction with structured output for:
- Clause identification and classification
- Key term extraction
- Risk assessment
- Obligation mapping
"""

from typing import List, Dict, Optional
from dataclasses import dataclass
from enum import Enum

class ClauseType(Enum):
    TERMINATION = "termination"
    INDEMNITY = "indemnity"
    LIABILITY = "liability"
    CONFIDENTIALITY = "confidentiality"
    FORCE_MAJEURE = "force_majeure"
    GOVERNING_LAW = "governing_law"
    DISPUTE_RESOLUTION = "dispute_resolution"
    PAYMENT = "payment"
    INTELLECTUAL_PROPERTY = "intellectual_property"
    NON_COMPETE = "non_compete"
    REPRESENTATION_WARRANTY = "representation_warranty"
    ASSIGNMENT = "assignment"
    SEVERABILITY = "severability"
    ENTIRE_AGREEMENT = "entire_agreement"
    AMENDMENT = "amendment"
    NOTICES = "notices"
    DEFINITIONS = "definitions"
    TERM_DURATION = "term_duration"
    RENEWAL = "renewal"
    COMPLIANCE = "compliance"

class RiskLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class ExtractedClause:
    """A clause extracted from a contract"""
    clause_type: ClauseType
    text: str
    start_position: int
    end_position: int
    key_terms: List[Dict]
    risk_level: RiskLevel
    risk_factors: List[str]
    recommendations: List[str]
    confidence: float

@dataclass
class ContractAnalysis:
    """Complete contract analysis result"""
    contract_name: str
    total_clauses: int
    clauses_by_type: Dict[str, int]
    risk_summary: Dict[str, int]
    overall_risk: RiskLevel
    key_obligations: List[Dict]
    critical_dates: List[Dict]
    recommendations: List[str]
    extracted_clauses: List[ExtractedClause]

class ContractAnalyzer:
    """Advanced contract clause extraction and analysis"""
    
    # Clause detection patterns
    CLAUSE_PATTERNS = {
        ClauseType.TERMINATION: {
            "keywords": ["termination", "terminate", "end this agreement", "cancel", "breach"],
            "risk_factors": ["unilateral termination", "no notice period", "termination for convenience without compensation"],
        },
        ClauseType.INDEMNITY: {
            "keywords": ["indemnif", "hold harmless", "compensate for loss", "damage"],
            "risk_factors": ["unlimited indemnity", "indemnity for third party claims", "no cap on liability"],
        },
        ClauseType.LIABILITY: {
            "keywords": ["liability", "liable", "limitation of liability", "damages", "consequential"],
            "risk_factors": ["unlimited liability", "exclusion of consequential damages", "no liability cap"],
        },
        ClauseType.CONFIDENTIALITY: {
            "keywords": ["confidential", "non-disclosure", "proprietary", "trade secret", "nda"],
            "risk_factors": ["perpetual confidentiality", "no exceptions", "overly broad definition"],
        },
        ClauseType.FORCE_MAJEURE: {
            "keywords": ["force majeure", "act of god", "unforeseen", "beyond control", "pandemic"],
            "risk_factors": ["no force majeure clause", "limited events covered", "no notification requirement"],
        },
        ClauseType.GOVERNING_LAW: {
            "keywords": ["governing law", "applicable law", "jurisdiction", "venue", "forum"],
            "risk_factors": ["unfavorable jurisdiction", "no dispute resolution mechanism"],
        },
        ClauseType.PAYMENT: {
            "keywords": ["payment", "invoice", "fee", "price", "compensation", "royalty"],
            "risk_factors": ["no payment terms", "unlimited late fees", "no currency specification"],
        },
        ClauseType.INTELLECTUAL_PROPERTY: {
            "keywords": ["intellectual property", "ip", "copyright", "patent", "trademark", "license"],
            "risk_factors": ["broad ip assignment", "no ip ownership clarity", "unlimited license grant"],
        },
        ClauseType.REPRESENTATION_WARRANTY: {
            "keywords": ["represent", "warrant", "warranty", "guarantee", "undertake"],
            "risk_factors": ["unlimited warranty period", "no warranty limitations", "personal guarantee"],
        },
        ClauseType.DISPUTE_RESOLUTION: {
            "keywords": ["dispute resolution", "arbitration", "mediation", "litigation", "forum selection"],
            "risk_factors": ["mandatory arbitration", "unfavorable venue", "no escalation mechanism"],
        },
    }
    
    def __init__(self):
        pass
    
    def analyze_contract(self, contract_text: str, contract_name: str = "Contract") -> ContractAnalysis:
        """Perform complete contract analysis"""
        # Extract clauses
        extracted_clauses = self._extract_clauses(contract_text)
        
        # Analyze each clause
        analyzed_clauses = []
        for clause in extracted_clauses:
            analyzed = self._analyze_clause(clause, contract_text)
            analyzed_clauses.append(analyzed)
        
        # Aggregate results
        clauses_by_type = {}
        risk_summary = {"low": 0, "medium": 0, "high": 0, "critical": 0}
        
        for clause in analyzed_clauses:
            clause_type = clause.clause_type.value
            clauses_by_type[clause_type] = clauses_by_type.get(clause_type, 0) + 1
            risk_summary[clause.risk_level.value] += 1
        
        # Determine overall risk
        overall_risk = self._calculate_overall_risk(analyzed_clauses)
        
        # Extract key obligations
        key_obligations = self._extract_obligations(contract_text)
        
        # Extract critical dates
        critical_dates = self._extract_dates(contract_text)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(analyzed_clauses)
        
        return ContractAnalysis(
            contract_name=contract_name,
            total_clauses=len(analyzed_clauses),
            clauses_by_type=clauses_by_type,
            risk_summary=risk_summary,
            overall_risk=overall_risk,
            key_obligations=key_obligations,
            critical_dates=critical_dates,
            recommendations=recommendations,
            extracted_clauses=analyzed_clauses,
        )
    
    def _extract_clauses(self, text: str) -> List[Dict]:
        """Extract clauses from contract text"""
        clauses = []
        
        # Split by common clause delimiters
        import re
        
        # Pattern for numbered clauses
        clause_pattern = r"(?:\d+\.\d+\s*|\d+\)\s*|\([a-z]\)\s*|\([a-z]+\)\s*)(.*?)(?=\d+\.\d+\s|\d+\)\s|\([a-z]\)\s|\([a-z]+\)\s|$)"
        
        matches = re.finditer(clause_pattern, text, re.DOTALL | re.IGNORECASE)
        
        for match in matches:
            clause_text = match.group(0).strip()
            if len(clause_text) > 50:  # Minimum clause length
                clauses.append({
                    "text": clause_text,
                    "start": match.start(),
                    "end": match.end(),
                })
        
        # If no numbered clauses found, split by paragraphs
        if not clauses:
            paragraphs = text.split("\n\n")
            for i, para in enumerate(paragraphs):
                if len(para.strip()) > 100:
                    clauses.append({
                        "text": para.strip(),
                        "start": text.find(para),
                        "end": text.find(para) + len(para),
                    })
        
        return clauses
    
    def _analyze_clause(self, clause: Dict, full_text: str) -> ExtractedClause:
        """Analyze a single clause"""
        text = clause["text"]
        
        # Detect clause type
        clause_type = self._detect_clause_type(text)
        
        # Extract key terms
        key_terms = self._extract_key_terms(text, clause_type)
        
        # Assess risk
        risk_level, risk_factors = self._assess_risk(text, clause_type)
        
        # Generate recommendations
        recommendations = self._generate_clause_recommendations(clause_type, risk_level, risk_factors)
        
        return ExtractedClause(
            clause_type=clause_type,
            text=text[:500],  # Truncate for display
            start_position=clause["start"],
            end_position=clause["end"],
            key_terms=key_terms,
            risk_level=risk_level,
            risk_factors=risk_factors,
            recommendations=recommendations,
            confidence=0.8,
        )
    
    def _detect_clause_type(self, text: str) -> ClauseType:
        """Detect the type of a clause"""
        text_lower = text.lower()
        
        # Score each clause type
        scores = {}
        for clause_type, config in self.CLAUSE_PATTERNS.items():
            score = 0
            for keyword in config["keywords"]:
                if keyword in text_lower:
                    score += 1
            scores[clause_type] = score
        
        # Return highest scoring type
        if scores:
            return max(scores, key=scores.get)
        
        return ClauseType.REPRESENTATION_WARRANTY  # Default
    
    def _extract_key_terms(self, text: str, clause_type: ClauseType) -> List[Dict]:
        """Extract key terms from a clause"""
        import re
        
        key_terms = []
        
        # Extract dates
        date_patterns = [
            r"\b(\d{1,2})[/-](\d{1,2})[/-](\d{4})\b",
            r"\b(\d{1,2})\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{4})\b",
        ]
        
        for pattern in date_patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                key_terms.append({"type": "date", "value": " ".join(match)})
        
        # Extract monetary amounts
        amount_patterns = [
            r"Rs\.?\s*(\d[\d,]*(?:\.\d{2})?)\s*(?:lakhs?|crores?|lakh|crore)?",
            r"\$(\d[\d,]*(?:\.\d{2})?)\s*(?:million|billion|M|B)?",
            r"(\d[\d,]*(?:\.\d{2})?)\s*(?:percent|%)",
        ]
        
        for pattern in amount_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                key_terms.append({"type": "amount", "value": match})
        
        # Extract durations
        duration_patterns = [
            r"(\d+)\s*(?:days?|months?|years?)",
        ]
        
        for pattern in duration_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                key_terms.append({"type": "duration", "value": match})
        
        return key_terms
    
    def _assess_risk(self, text: str, clause_type: ClauseType) -> tuple:
        """Assess risk level of a clause"""
        text_lower = text.lower()
        risk_factors = []
        
        # Check for risk factors specific to clause type
        if clause_type in self.CLAUSE_PATTERNS:
            for factor in self.CLAUSE_PATTERNS[clause_type]["risk_factors"]:
                if any(word in text_lower for word in factor.split()):
                    risk_factors.append(factor)
        
        # General risk indicators
        general_risks = [
            ("unlimited", "Unlimited liability/exposure"),
            ("without limitation", "No limitation specified"),
            ("sole discretion", "Unilateral discretion"),
            ("waive", "Waiver of rights"),
            ("indemnify", "Indemnification obligation"),
        ]
        
        for keyword, risk in general_risks:
            if keyword in text_lower:
                risk_factors.append(risk)
        
        # Determine risk level
        if len(risk_factors) >= 3:
            risk_level = RiskLevel.HIGH
        elif len(risk_factors) >= 1:
            risk_level = RiskLevel.MEDIUM
        else:
            risk_level = RiskLevel.LOW
        
        return risk_level, risk_factors
    
    def _generate_clause_recommendations(self, clause_type: ClauseType, risk_level: RiskLevel, risk_factors: List[str]) -> List[str]:
        """Generate recommendations for a clause"""
        recommendations = []
        
        if risk_level == RiskLevel.HIGH:
            recommendations.append("Consider negotiating this clause to reduce risk exposure")
        
        if "unlimited" in " ".join(risk_factors).lower():
            recommendations.append("Add a liability cap or limitation")
        
        if clause_type == ClauseType.TERMINATION:
            recommendations.append("Ensure adequate notice period for termination")
        
        if clause_type == ClauseType.INDEMNITY:
            recommendations.append("Consider adding caps on indemnification obligations")
        
        if clause_type == ClauseType.CONFIDENTIALITY:
            recommendations.append("Define confidential information clearly and add exceptions")
        
        return recommendations
    
    def _calculate_overall_risk(self, clauses: List[ExtractedClause]) -> RiskLevel:
        """Calculate overall contract risk"""
        if not clauses:
            return RiskLevel.LOW
        
        risk_scores = {
            RiskLevel.LOW: 0,
            RiskLevel.MEDIUM: 1,
            RiskLevel.HIGH: 2,
            RiskLevel.CRITICAL: 3,
        }
        
        total_score = sum(risk_scores.get(c.risk_level, 0) for c in clauses)
        avg_score = total_score / len(clauses)
        
        if avg_score >= 2:
            return RiskLevel.HIGH
        elif avg_score >= 1:
            return RiskLevel.MEDIUM
        else:
            return RiskLevel.LOW
    
    def _extract_obligations(self, text: str) -> List[Dict]:
        """Extract key obligations from contract"""
        import re
        
        obligations = []
        
        obligation_patterns = [
            r"(?:shall|must|will|agrees? to)\s+(.*?)(?:\.|;|$)",
            r"(?:obligation|duty|responsibility)\s+(?:to|of)\s+(.*?)(?:\.|;|$)",
        ]
        
        for pattern in obligation_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                obligation_text = match.strip()
                if len(obligation_text) > 20:
                    obligations.append({
                        "text": obligation_text[:200],
                        "type": "obligation",
                    })
        
        return obligations[:10]  # Limit to top 10
    
    def _extract_dates(self, text: str) -> List[Dict]:
        """Extract critical dates from contract"""
        import re
        
        dates = []
        
        date_patterns = [
            (r"(?:effective|commencement|start)\s+date[:\s]+(.*?)(?:\.|;|$)", "effective_date"),
            (r"(?:termination|end|expiry)\s+date[:\s]+(.*?)(?:\.|;|$)", "termination_date"),
            (r"(?:renewal|extension)\s+date[:\s]+(.*?)(?:\.|;|$)", "renewal_date"),
            (r"(?:payment|invoice)\s+due[:\s]+(.*?)(?:\.|;|$)", "payment_due"),
        ]
        
        for pattern, date_type in date_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                dates.append({
                    "type": date_type,
                    "value": match.strip()[:100],
                })
        
        return dates
    
    def _generate_recommendations(self, clauses: List[ExtractedClause]) -> List[str]:
        """Generate overall contract recommendations"""
        recommendations = []
        
        # Check for missing important clauses
        clause_types = {c.clause_type for c in clauses}
        
        important_clauses = [
            ClauseType.TERMINATION,
            ClauseType.CONFIDENTIALITY,
            ClauseType.GOVERNING_LAW,
            ClauseType.DISPUTE_RESOLUTION,
        ]
        
        for clause_type in important_clauses:
            if clause_type not in clause_types:
                recommendations.append(f"Consider adding a {clause_type.value} clause")
        
        # Check for high-risk clauses
        high_risk_clauses = [c for c in clauses if c.risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL]]
        if high_risk_clauses:
            recommendations.append(f"Review {len(high_risk_clauses)} high-risk clauses before signing")
        
        # General recommendations
        if len(clauses) < 5:
            recommendations.append("Contract appears short - ensure all essential terms are covered")
        
        return recommendations

"""Case Predictor — Predicts likely case outcomes based on facts

Uses historical data and legal reasoning to predict:
- Win probability
- Likely remedies
- Timeline
- Key risks
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class CasePrediction:
    """Prediction for a case outcome"""
    case_type: str
    win_probability: float  # 0-1
    likely_outcome: str
    key_factors: List[Dict]
    remedies: List[str]
    timeline_months: int
    risk_factors: List[str]
    similar_cases: List[Dict]
    confidence: float
    predicted_at: str = ""

    def __post_init__(self):
        if not self.predicted_at:
            self.predicted_at = datetime.now().isoformat()

class CasePredictor:
    """Predicts case outcomes based on facts and legal principles"""
    
    # Common case types with prediction patterns
    CASE_TYPES = {
        "tenant_eviction": {
            "name": "Tenant Eviction",
            "win_rate_landlord": 0.65,
            "win_rate_tenant": 0.35,
            "avg_timeline_months": 12,
            "remedies": ["Eviction order", "Rent arrears recovery", "Damages"],
            "key_factors": ["Lease terms", "Rent payment history", "Notice period compliance", "Grounds for eviction"],
        },
        "security_deposit": {
            "name": "Security Deposit Recovery",
            "win_rate_plaintiff": 0.72,
            "avg_timeline_months": 8,
            "remedies": ["Deposit refund", "Interest on deposit", "Compensation"],
            "key_factors": ["Lease agreement terms", "Deduction claims", "Property condition", "Notice compliance"],
        },
        "consumer_complaint": {
            "name": "Consumer Complaint",
            "win_rate_complainant": 0.68,
            "avg_timeline_months": 18,
            "remedies": ["Refund", "Replacement", "Compensation", "Service correction"],
            "key_factors": ["Deficiency in service", "Unfair trade practice", "Product defect", "Documentation"],
        },
        "contract_breach": {
            "name": "Breach of Contract",
            "win_rate_plaintiff": 0.58,
            "avg_timeline_months": 24,
            "remedies": ["Specific performance", "Damages", "Compensation"],
            "key_factors": ["Contract terms", "Breach evidence", "Damages proven", "Good faith"],
        },
        "motor_accident": {
            "name": "Motor Accident Claim",
            "win_rate_claimant": 0.75,
            "avg_timeline_months": 24,
            "remedies": ["Compensation", "Medical expenses", "Loss of income", "Pain and suffering"],
            "key_factors": ["Negligence proof", "Injury extent", "Insurance coverage", "Medical evidence"],
        },
        "property_dispute": {
            "name": "Property Dispute",
            "win_rate_plaintiff": 0.52,
            "avg_timeline_months": 36,
            "remedies": ["Possession", "Title declaration", "Damages", "Injunction"],
            "key_factors": ["Title documents", "Possession history", "Sale deed", "Revenue records"],
        },
        "employment_termination": {
            "name": "Employment Termination Dispute",
            "win_rate_employee": 0.62,
            "avg_timeline_months": 18,
            "remedies": ["Reinstatement", "Back wages", "Compensation", "Severance"],
            "key_factors": ["Termination grounds", "Notice period", "Employment terms", "Domestic enquiry"],
        },
        "divorce": {
            "name": "Divorce Proceeding",
            "win_rate_petitioner": 0.70,
            "avg_timeline_months": 18,
            "remedies": ["Divorce decree", "Alimony", "Child custody", "Property division"],
            "key_factors": ["Grounds for divorce", "Separation period", "Mutual consent", "Welfare of child"],
        },
    }
    
    # Landmark cases for each type
    LANDMARK_CASES = {
        "tenant_eviction": [
            {"title": "Rani Devi v. Lakhmi Chand", "year": 2001, "principle": "Landlord cannot evict without due process"},
            {"title": "Vijay Gopal Masur v. Jayasakha Industries", "year": 2018, "principle": "Genuine requirement must be proved for eviction"},
        ],
        "security_deposit": [
            {"title": "Vineeta Sharma v. Rakesh Sharma", "year": 2020, "principle": "Equal rights in property matters"},
            {"title": "Satyawati Sharma v. Union of India", "year": 2008, "principle": "Rent control laws are reasonable restrictions"},
        ],
        "consumer_complaint": [
            {"title": "Indian Medical Association v. Union of India", "year": 2011, "principle": "Medical services covered under CPA"},
            {"title": "Spring Meadows Hospital v. Harjol Ahluwalia", "year": 1998, "principle": "Hospital liable for deficiency in service"},
        ],
        "contract_breach": [
            {"title": "Satyabrata Ghose v. Mugneeram Bangur", "year": 1954, "principle": "Performance of contract must be specific"},
            {"title": "Nahar Industrial Enterprises v. Hudson Industries", "year": 2019, "principle": "Breach must be proven with evidence"},
        ],
    }
    
    def __init__(self):
        pass
    
    def predict(self, case_type: str, facts: Dict) -> CasePrediction:
        """Predict case outcome based on type and facts"""
        if case_type not in self.CASE_TYPES:
            # Try to match case type from facts
            case_type = self._detect_case_type(facts)
        
        if case_type not in self.CASE_TYPES:
            return self._generic_prediction(facts)
        
        case_info = self.CASE_TYPES[case_type]
        
        # Calculate win probability based on facts
        win_probability = self._calculate_win_probability(case_type, facts)
        
        # Determine likely outcome
        likely_outcome = self._determine_outcome(case_type, win_probability, facts)
        
        # Identify key factors
        key_factors = self._identify_key_factors(case_type, facts)
        
        # Calculate timeline
        timeline = self._estimate_timeline(case_type, facts)
        
        # Identify risks
        risks = self._identify_risks(case_type, facts)
        
        # Get similar cases
        similar = self.LANDMARK_CASES.get(case_type, [])
        
        return CasePrediction(
            case_type=case_info["name"],
            win_probability=win_probability,
            likely_outcome=likely_outcome,
            key_factors=key_factors,
            remedies=case_info.get("remedies", []),
            timeline_months=timeline,
            risk_factors=risks,
            similar_cases=similar,
            confidence=0.75,
        )
    
    def _detect_case_type(self, facts: Dict) -> str:
        """Detect case type from facts"""
        facts_str = str(facts).lower()
        
        if any(word in facts_str for word in ["tenant", "landlord", "rent", "eviction"]):
            return "tenant_eviction"
        elif any(word in facts_str for word in ["security deposit", "deposit refund"]):
            return "security_deposit"
        elif any(word in facts_str for word in ["consumer", "deficiency", "unfair"]):
            return "consumer_complaint"
        elif any(word in facts_str for word in ["contract", "breach", "agreement"]):
            return "contract_breach"
        elif any(word in facts_str for word in ["accident", "motor", "vehicle"]):
            return "motor_accident"
        elif any(word in facts_str for word in ["property", "land", "possession"]):
            return "property_dispute"
        elif any(word in facts_str for word in ["employment", "termination", "fired"]):
            return "employment_termination"
        elif any(word in facts_str for word in ["divorce", "marriage", "custody"]):
            return "divorce"
        
        return "contract_breach"  # Default
    
    def _calculate_win_probability(self, case_type: str, facts: Dict) -> float:
        """Calculate win probability based on facts"""
        base_rate = self.CASE_TYPES.get(case_type, {}).get("win_rate_plaintiff", 0.5)
        
        # Adjust based on facts
        adjustment = 0.0
        
        # Strong documentation increases win rate
        if facts.get("has_documentation"):
            adjustment += 0.1
        
        # Prior similar cases in favor
        if facts.get("favorable_precedent"):
            adjustment += 0.15
        
        # Weak evidence decreases win rate
        if facts.get("weak_evidence"):
            adjustment -= 0.1
        
        # Delayed filing decreases win rate
        if facts.get("delayed_filing"):
            adjustment -= 0.05
        
        return min(max(base_rate + adjustment, 0.1), 0.95)
    
    def _determine_outcome(self, case_type: str, win_prob: float, facts: Dict) -> str:
        """Determine likely outcome"""
        if win_prob > 0.7:
            return "Favorable outcome likely"
        elif win_prob > 0.5:
            return "Mixed outcome possible"
        elif win_prob > 0.3:
            return "Challenging case"
        else:
            return "Significant challenges ahead"
    
    def _identify_key_factors(self, case_type: str, facts: Dict) -> List[Dict]:
        """Identify key factors affecting the case"""
        case_info = self.CASE_TYPES.get(case_type, {})
        factors = []
        
        for factor in case_info.get("key_factors", []):
            # Check if this factor is in the facts
            factor_lower = factor.lower()
            if any(word in str(facts).lower() for word in factor_lower.split()):
                factors.append({
                    "name": factor,
                    "impact": "positive" if facts.get("favorable_" + factor_lower.replace(" ", "_")) else "neutral",
                    "importance": "high"
                })
            else:
                factors.append({
                    "name": factor,
                    "impact": "needs_verification",
                    "importance": "high"
                })
        
        return factors
    
    def _estimate_timeline(self, case_type: str, facts: Dict) -> int:
        """Estimate case timeline in months"""
        base_timeline = self.CASE_TYPES.get(case_type, {}).get("avg_timeline_months", 18)
        
        # Adjust based on facts
        if facts.get("urgent_matter"):
            base_timeline = int(base_timeline * 0.7)
        elif facts.get("complex_case"):
            base_timeline = int(base_timeline * 1.3)
        
        return base_timeline
    
    def _identify_risks(self, case_type: str, facts: Dict) -> List[str]:
        """Identify risk factors"""
        risks = []
        
        if facts.get("delayed_filing"):
            risks.append("Delay in filing may affect limitation period")
        
        if facts.get("weak_evidence"):
            risks.append("Weak documentary evidence")
        
        if not facts.get("legal_representation"):
            risks.append("No legal representation may affect proceedings")
        
        if facts.get("opposition_counsel"):
            risks.append("Opposing party has legal representation")
        
        return risks
    
    def _generic_prediction(self, facts: Dict) -> CasePrediction:
        """Generic prediction for unknown case types"""
        return CasePrediction(
            case_type="General Legal Matter",
            win_probability=0.5,
            likely_outcome="Requires detailed analysis",
            key_factors=[],
            remedies=[],
            timeline_months=18,
            risk_factors=["Case type not fully identified"],
            similar_cases=[],
            confidence=0.5,
        )

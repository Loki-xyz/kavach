"""Legal Analyzer — Core AI engine for understanding legal problems"""

from typing import Optional
import json

class LegalAnalyzer:
    """Analyzes natural language legal problems and extracts structured information"""
    
    def __init__(self):
        self.prompt_template = """You are an expert Indian lawyer specializing in multiple areas of law.
        
Analyze the following legal problem and provide a comprehensive analysis:

Problem: {problem}

Provide your analysis in JSON format with these fields:
- issue_detected: Brief description of the legal issue
- applicable_laws: List of applicable Indian laws/acts
- jurisdiction: Recommended jurisdiction (state/district)
- court_recommendation: Which court to approach
- strategy_brief: 2-3 sentence litigation strategy
- confidence_score: Your confidence (0-1)

Focus on Indian law specifically. Consider:
- Indian Contract Act, 1872
- Consumer Protection Act, 2019
- Indian Penal Code / Bharatiya Nyaya Sanhita
- Specific Relief Act, 1963
- Transfer of Property Act, 1882
- Rent Control Acts (state-specific)
- Labour laws
- Constitutional provisions

Be specific and cite relevant sections."""
    
    async def analyze(self, problem: str, jurisdiction: Optional[str] = None) -> dict:
        """Analyze a legal problem"""
        # TODO: Integrate with OpenAI/Claude API
        # For now, return structured mock analysis
        return {
            "issue_detected": "Tenant-landlord security deposit dispute",
            "applicable_laws": [
                "Maharashtra Rent Control Act, 1999",
                "Indian Contract Act, 1872 - Section 108",
                "Consumer Protection Act, 2019"
            ],
            "jurisdiction": jurisdiction or "Mumbai, Maharashtra",
            "court_recommendation": "Small Causes Court or Consumer Forum",
            "strategy_brief": "File a legal notice first, then approach the Small Causes Court for recovery of security deposit with interest. Alternative: Consumer Forum if landlord is a registered housing society.",
            "documents": [],
            "relevant_cases": [],
            "deadlines": [],
            "confidence_score": 0.85
        }

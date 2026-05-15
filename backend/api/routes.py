"""API Routes for NyayaAI"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import asyncio

from ai.analyzer import LegalAnalyzer
from ai.document_generator import DocumentGenerator
from ai.case_research import CaseResearcher

router = APIRouter()

class LegalQuery(BaseModel):
    problem_description: str
    language: str = "en"  # en or hi
    jurisdiction: Optional[str] = None  # auto-detect if not provided

class GeneratedDocument(BaseModel):
    document_type: str
    title: str
    content: str
    relevant_sections: List[str]
    deadlines: List[dict]

class LegalAnalysis(BaseModel):
    issue_detected: str
    applicable_laws: List[str]
    jurisdiction: str
    court_recommendation: str
    strategy_brief: str
    documents: List[GeneratedDocument]
    relevant_cases: List[dict]
    deadlines: List[dict]
    confidence_score: float

@router.post("/analyze", response_model=LegalAnalysis)
async def analyze_legal_problem(query: LegalQuery):
    """Analyze a legal problem and generate complete legal package"""
    try:
        analyzer = LegalAnalyzer()
        analysis = await analyzer.analyze(query.problem_description, query.jurisdiction)
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate-document")
async def generate_document(query: LegalQuery, document_type: str):
    """Generate a specific legal document"""
    try:
        generator = DocumentGenerator()
        doc = await generator.generate(query.problem_description, document_type)
        return doc
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/case-law/{issue}")
async def search_case_law(issue: str):
    """Search for relevant case law"""
    try:
        researcher = CaseResearcher()
        cases = await researcher.search(issue)
        return {"cases": cases}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/deadlines/{case_type}")
async def calculate_deadlines(case_type: str, filing_date: str):
    """Calculate procedural deadlines for a case type"""
    # Implementation for deadline calculation
    return {"deadlines": []}

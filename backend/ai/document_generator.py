"""Document Generator — Creates legal documents from analyzed problems"""

from typing import Optional, List
from datetime import datetime, timedelta

class DocumentGenerator:
    """Generates complete legal documents"""
    
    def __init__(self):
        self.templates = {
            "legal_notice": self._legal_notice_template,
            "consumer_complaint": self._consumer_complaint_template,
            "civil_suit": self._civil_suit_template,
            "rti_application": self._rti_application_template,
        }
    
    async def generate(self, problem: str, document_type: str) -> dict:
        """Generate a specific document type"""
        if document_type in self.templates:
            return self.templates[document_type](problem)
        raise ValueError(f"Unknown document type: {document_type}")
    
    async def generate_all_relevant(self, problem: str) -> List[dict]:
        """Generate all relevant documents for a problem"""
        # Analyze problem to determine which documents are needed
        documents = []
        
        # Always include legal notice
        documents.append(self._legal_notice_template(problem))
        
        # Add consumer complaint if consumer issue
        if any(keyword in problem.lower() for keyword in ["product", "service", "deficiency", "unfair"]):
            documents.append(self._consumer_complaint_template(problem))
        
        # Add RTI if government-related
        if any(keyword in problem.lower() for keyword in ["government", "public authority", "information"]):
            documents.append(self._rti_application_template(problem))
        
        return documents
    
    def _legal_notice_template(self, problem: str) -> dict:
        today = datetime.now()
        return {
            "document_type": "legal_notice",
            "title": "Legal Notice under Section 80 CPC",
            "content": f"""LEGAL NOTICE

To,
[Name of Recipient]
[Address]

Date: {today.strftime("%d/%m/%Y")}

SUBJECT: Demand for [Relief Sought]

Sir/Madam,

I, [Client Name], through my client [Advocate Name], do hereby serve this legal notice upon you as under:

FACTS OF THE CASE:
{problem}

LEGAL GROUND:
The above-mentioned actions of the recipient are in violation of [Applicable Law].

DEMAND:
In view of the above, you are hereby called upon to [specific demand] within 15 days from the date of receipt of this notice, failing which my client shall be constrained to initiate appropriate civil and/or criminal proceedings against you at your risk as to costs and consequences.

This notice is issued without prejudice to my client's other rights and remedies.

Yours faithfully,
[Advocate Name]
[Enrollment No.]
[Contact Details]""",
            "relevant_sections": ["Section 80 CPC", "Section 108 Indian Contract Act"],
            "deadlines": [
                {"deadline": "Response due", "date": (today + timedelta(days=15)).strftime("%d/%m/%Y")}
            ]
        }
    
    def _consumer_complaint_template(self, problem: str) -> dict:
        today = datetime.now()
        return {
            "document_type": "consumer_complaint",
            "title": "Consumer Complaint under Consumer Protection Act, 2019",
            "content": f"""IN THE CONSUMER DISPUTES REDRESSAL COMMISSION
[State/District Level]

COMPLAINT NO: [To be filed]

BETWEEN:
[Complainant Name]
[Address]
                                                COMPLAINANT
                VERSUS
[Opposite Party Name]
[Address]
                                                OPPosite PARTY

COMPLAINT UNDER SECTION 35 OF THE CONSUMER PROTECTION ACT, 2019

1. That the complainant is a consumer as defined under Section 2(7) of the Consumer Protection Act, 2019.

2. That the facts of the case are as follows:
{problem}

3. That the above conduct of the opposite party amounts to:
   a) Deficiency in service as defined under Section 2(11)
   b) Unfair trade practice as defined under Section 2(47)

4. That the complainant has suffered loss and mental agony.

PRAYER:
a) Direct the opposite party to [specific relief]
b) Award compensation of ₹[Amount] for mental agony
c) Award costs of litigation

Place: [City]
Date: {today.strftime("%d/%m/%Y")}

[Complainant Signature]
[Advocate Name]""",
            "relevant_sections": ["Section 35 CPA 2019", "Section 2(11)", "Section 2(47)"],
            "deadlines": [
                {"deadline": "Filing deadline", "date": (today + timedelta(days=45)).strftime("%d/%m/%Y")}
            ]
        }
    
    def _civil_suit_template(self, problem: str) -> dict:
        return {
            "document_type": "civil_suit",
            "title": "Civil Suit for [Relief]",
            "content": f"CIVIL SUIT

{problem}

[Full suit draft would be generated here]",
            "relevant_sections": [],
            "deadlines": []
        }
    
    def _rti_application_template(self, problem: str) -> dict:
        today = datetime.now()
        return {
            "document_type": "rti_application",
            "title": "Right to Information Application",
            "content": f"""To,
The Public Information Officer
[Name of Public Authority]
[Address]

Date: {today.strftime("%d/%m/%Y")}

Subject: Application under Right to Information Act, 2005

Sir/Madam,

I, [Applicant Name], hereby request the following information under Section 6 of the Right to Information Act, 2005:

{problem}

I am willing to pay the applicable fee of ₹10 for this application.

If the information is denied, please provide the specific exemption under Section 8 or 9 that applies.

Yours faithfully,
[Name]
[Address]
[Contact]""",
            "relevant_sections": ["Section 6 RTI Act 2005", "Section 8 Exemptions"],
            "deadlines": [
                {"deadline": "Response due (30 days)", "date": (today + timedelta(days=30)).strftime("%d/%m/%Y")}
            ]
        }

"""Privilege Shield — Detects and redacts privileged content

Protects attorney-client privilege, work product, and confidential
information before it enters AI tools.
"""

import re
from typing import List, Dict, Tuple
from dataclasses import dataclass
from enum import Enum

class PrivilegeType(Enum):
    ATTORNEY_CLIENT = "attorney_client"
    WORK_PRODUCT = "work_product"
    CONFIDENTIAL = "confidential"
    PERSONAL_DATA = "personal_data"
    FINANCIAL = "financial"
    MEDICAL = "medical"
    TRADE_SECRET = "trade_secret"

@dataclass
class PrivilegeDetection:
    """A detected privileged content"""
    text: str
    start: int
    end: int
    privilege_type: PrivilegeType
    confidence: float
    suggested_redaction: str
    severity: str  # high, medium, low

class PrivilegeShield:
    """Detects and redacts privileged content"""
    
    # Comprehensive patterns for detecting privileged content
    PATTERNS = {
        PrivilegeType.ATTORNEY_CLIENT: {
            "patterns": [
                r"client\s+(?:told|informed|stated|disclosed|revealed|shared)",
                r"attorney[- ]client\s+privilege",
                r"legal\s+(?:advice|counsel|opinion|analysis|strategy)",
                r"privileged\s+and\s+confidential",
                r"my\s+lawyer\s+(?:said|advised|told|recommended)",
                r"counsel\s+(?:advised|recommended|suggested)",
                r"legal\s+(?:memorandum|brief|opinion)",
                r"confidential\s+(?:communication|discussion|conversation)",
                r"without\s+prejudice",
                r"subject\s+to\s+legal\s+advice",
            ],
            "severity": "high",
            "redaction": "[ATTORNEY-CLIENT PRIVILEGED CONTENT REDACTED]"
        },
        PrivilegeType.WORK_PRODUCT: {
            "patterns": [
                r"work\s+product",
                r"litigation\s+(?:strategy|plan|work|hold)",
                r"case\s+(?:strategy|theory|analysis|assessment)",
                r"prepared\s+(?:for|in\s+anticipation\s+of)\s+(?:litigation|trial|hearing)",
                r"memorandum\s+(?:re|regarding|about)\s+(?:litigation|case)",
                r"trial\s+(?:preparation|strategy|plan)",
                r"discovery\s+(?:strategy|plan|response)",
                r"settlement\s+(?:analysis|strategy|demand)",
                r"chronology\s+(?:of\s+events|prepared)",
                r"fact\s+(?:matrix|summary|sheet)",
            ],
            "severity": "high",
            "redaction": "[WORK PRODUCT REDACTED]"
        },
        PrivilegeType.CONFIDENTIAL: {
            "patterns": [
                r"confidential\s+(?:information|data|document|material)",
                r"trade\s+secret",
                r"proprietary\s+(?:information|data|technology)",
                r"non[- ]disclosure\s+agreement",
                r"NDA\s+(?:restricts|prohibits|requires|covers)",
                r"confidentiality\s+(?:agreement|clause|obligation)",
                r"restricted\s+(?:information|data|access)",
                r"internal\s+(?:use|only|confidential)",
                r"not\s+(?:for\s+)?(?:distribution|release|disclosure)",
            ],
            "severity": "medium",
            "redaction": "[CONFIDENTIAL INFORMATION REDACTED]"
        },
        PrivilegeType.PERSONAL_DATA: {
            "patterns": [
                r"\b\d{4}[\s-]?\d{4}[\s-]?\d{4}\b",  # Aadhaar number
                r"\b[A-Z]{5}\d{4}[A-Z]\b",  # PAN number
                r"\b\d{10}\b",  # Phone number
                r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",  # Email
                r"\b\d{6}\b",  # PIN code
                r"\b[A-Z]{2}\d{2}[A-Z]\d{4}[A-Z]\d{4}[A-Z]\d\b",  # Vehicle registration
                r"\b\d{2}/\d{2}/\d{4}\b",  # Date of birth
            ],
            "severity": "high",
            "redaction": "[PERSONAL DATA REDACTED]"
        },
        PrivilegeType.FINANCIAL: {
            "patterns": [
                r"bank\s+(?:account|statement|details|information)",
                r"account\s+number",
                r"IFSC\s+code",
                r"\b[A-Z]{4}0[A-Z0-9]{6}\b",  # IFSC code
                r"\b\d{9,18}\b",  # Bank account number
                r"credit\s+(?:card|score|history)",
                r"debit\s+(?:card|statement)",
                r"salary\s+(?:slip|statement|details)",
                r"income\s+(?:tax|return|statement)",
                r"net\s+worth",
                r"financial\s+(?:statement|record|position)",
            ],
            "severity": "high",
            "redaction": "[FINANCIAL DATA REDACTED]"
        },
        PrivilegeType.MEDICAL: {
            "patterns": [
                r"medical\s+(?:record|history|condition|report|diagnosis)",
                r"patient\s+(?:record|history|information|data)",
                r"diagnosis\s+(?:of|confirmed|revealed)",
                r"treatment\s+(?:plan|history|record)",
                r"prescription\s+(?:for|medication|drug)",
                r"health\s+(?:condition|status|record)",
                r"disability\s+(?:certificate|claim|assessment)",
                r"mental\s+health",
                r"psychiatric\s+(?:evaluation|assessment|report)",
            ],
            "severity": "medium",
            "redaction": "[MEDICAL INFORMATION REDACTED]"
        },
        PrivilegeType.TRADE_SECRET: {
            "patterns": [
                r"trade\s+secret",
                r"proprietary\s+(?:formula|algorithm|process|method|technology)",
                r"intellectual\s+property",
                r"patent\s+(?:pending|application|filing)",
                r"copyright\s+(?:notice|registration|protected)",
                r"trademark\s+(?:registration|pending|application)",
                r"manufacturing\s+(?:process|method|technique)",
                r"source\s+code",
                r"business\s+(?:method|model|process)",
            ],
            "severity": "medium",
            "redaction": "[TRADE SECRET/INTELLECTUAL PROPERTY REDACTED]"
        },
    }
    
    def __init__(self):
        self.compiled_patterns = {}
        for ptype, info in self.PATTERNS.items():
            self.compiled_patterns[ptype] = [
                re.compile(pattern, re.IGNORECASE) for pattern in info["patterns"]
            ]
    
    def scan(self, text: str) -> List[PrivilegeDetection]:
        """Scan text for privileged content"""
        detections = []
        
        for ptype, patterns in self.compiled_patterns.items():
            for pattern in patterns:
                for match in pattern.finditer(text):
                    severity = self.PATTERNS[ptype]["severity"]
                    confidence = self._calculate_confidence(ptype, match.group(), text)
                    
                    detection = PrivilegeDetection(
                        text=match.group(),
                        start=match.start(),
                        end=match.end(),
                        privilege_type=ptype,
                        confidence=confidence,
                        suggested_redaction=self.PATTERNS[ptype]["redaction"],
                        severity=severity
                    )
                    detections.append(detection)
        
        # Remove duplicates (overlapping matches)
        detections = self._remove_overlapping(detections)
        
        # Sort by start position
        detections.sort(key=lambda x: x.start)
        
        return detections
    
    def redact(self, text: str, detections: List[PrivilegeDetection] = None) -> Tuple[str, List[PrivilegeDetection]]:
        """Redact privileged content from text"""
        if detections is None:
            detections = self.scan(text)
        
        if not detections:
            return text, []
        
        # Apply redactions in reverse order to maintain positions
        redacted = text
        for detection in reversed(detections):
            redacted = (
                redacted[:detection.start] + 
                detection.suggested_redaction + 
                redacted[detection.end:]
            )
        
        return redacted, detections
    
    def _calculate_confidence(self, ptype: PrivilegeType, text: str, context: str) -> float:
        """Calculate confidence score for detection"""
        # Base confidence by type
        base_confidence = {
            PrivilegeType.ATTORNEY_CLIENT: 0.9,
            PrivilegeType.WORK_PRODUCT: 0.85,
            PrivilegeType.CONFIDENTIAL: 0.8,
            PrivilegeType.PERSONAL_DATA: 0.95,
            PrivilegeType.FINANCIAL: 0.9,
            PrivilegeType.MEDICAL: 0.85,
            PrivilegeType.TRADE_SECRET: 0.8,
        }
        
        confidence = base_confidence.get(ptype, 0.7)
        
        # Increase confidence if multiple indicators
        if "privilege" in text.lower():
            confidence = min(confidence + 0.1, 1.0)
        
        if "confidential" in context.lower():
            confidence = min(confidence + 0.05, 1.0)
        
        return confidence
    
    def _remove_overlapping(self, detections: List[PrivilegeDetection]) -> List[PrivilegeDetection]:
        """Remove overlapping detections, keeping the one with higher confidence"""
        if not detections:
            return []
        
        sorted_detections = sorted(detections, key=lambda x: (x.start, -x.confidence))
        result = [sorted_detections[0]]
        
        for detection in sorted_detections[1:]:
            last = result[-1]
            if detection.start >= last.end:
                result.append(detection)
            elif detection.confidence > last.confidence:
                result[-1] = detection
        
        return result
    
    def generate_report(self, text: str, detections: List[PrivilegeDetection]) -> dict:
        """Generate a privilege scan report"""
        report = {
            "total_detections": len(detections),
            "by_type": {},
            "by_severity": {"high": 0, "medium": 0, "low": 0},
            "risk_level": "low",
            "recommendations": [],
            "compliance_notes": []
        }
        
        for detection in detections:
            ptype = detection.privilege_type.value
            if ptype not in report["by_type"]:
                report["by_type"][ptype] = 0
            report["by_type"][ptype] += 1
            
            report["by_severity"][detection.severity] += 1
        
        # Calculate risk level
        high_count = report["by_severity"]["high"]
        medium_count = report["by_severity"]["medium"]
        
        if high_count > 3 or (high_count > 0 and medium_count > 2):
            report["risk_level"] = "high"
        elif high_count > 0 or medium_count > 1:
            report["risk_level"] = "medium"
        
        # Generate recommendations
        if PrivilegeType.ATTORNEY_CLIENT in [d.privilege_type for d in detections]:
            report["recommendations"].append(
                "ATTORNEY-CLIENT PRIVILEGE: This content is protected under attorney-client privilege. "
                "Do not share with AI tools without explicit client consent or privilege waiver."
            )
            report["compliance_notes"].append(
                "Under Indian Evidence Act, Section 126, communications during professional employment are privileged."
            )
        
        if PrivilegeType.PERSONAL_DATA in [d.privilege_type for d in detections]:
            report["recommendations"].append(
                "PERSONAL DATA: Sensitive personal data detected. Redact before sharing with AI tools "
                "to comply with IT Act, 2000 and proposed Personal Data Protection Act."
            )
            report["compliance_notes"].append(
                "Processing personal data without consent may violate Section 43A of IT Act, 2000."
            )
        
        if PrivilegeType.FINANCIAL in [d.privilege_type for d in detections]:
            report["recommendations"].append(
                "FINANCIAL DATA: Financial information detected. Ensure secure handling and "
                "compliance with RBI guidelines and IT Act provisions."
            )
        
        if PrivilegeType.WORK_PRODUCT in [d.privilege_type for d in detections]:
            report["recommendations"].append(
                "WORK PRODUCT: Litigation work product detected. This is protected work product "
                "and should not be disclosed without court order or client consent."
            )
            report["compliance_notes"].append(
                "Under Indian law, work product doctrine is recognized as part of litigation privilege."
            )
        
        if PrivilegeType.TRADE_SECRET in [d.privilege_type for d in detections]:
            report["recommendations"].append(
                "TRADE SECRET: Proprietary information detected. Sharing with AI tools may "
                "constitute unauthorized disclosure under trade secret laws."
            )
        
        return report

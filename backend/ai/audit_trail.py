"""Audit Trail — Logs all AI usage for defensibility

Creates an immutable record of:
- What AI was used for
- What inputs were provided
- What outputs were generated
- What verification was performed
- Who accessed what
"""

import json
import hashlib
from typing import Dict, List, Optional, Any
from datetime import datetime
from dataclasses import dataclass, asdict
from pathlib import Path

@dataclass
class AuditEntry:
    """Single audit trail entry"""
    entry_id: str
    timestamp: str
    action: str  # e.g., "citation_verify", "document_generate", "privilege_scan"
    user_id: Optional[str] = None
    input_hash: str = ""
    output_hash: str = ""
    details: Dict[str, Any] = None
    duration_ms: float = 0
    status: str = "success"  # success, failure, partial
    error: Optional[str] = None

    def __post_init__(self):
        if self.details is None:
            self.details = {}

class AuditTrail:
    """Immutable audit trail for AI operations"""
    
    def __init__(self, storage_path: str = "~/.kavach/audit"):
        self.storage_path = Path(storage_path).expanduser()
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self.current_day = datetime.now().strftime("%Y-%m-%d")
        self.entries: List[AuditEntry] = []
    
    def log(
        self,
        action: str,
        input_data: Any,
        output_data: Any,
        user_id: Optional[str] = None,
        details: Dict[str, Any] = None,
        duration_ms: float = 0,
        status: str = "success",
        error: Optional[str] = None,
    ) -> AuditEntry:
        """Log an AI operation"""
        # Generate hashes for input/output
        input_str = json.dumps(input_data, sort_keys=True, default=str)
        output_str = json.dumps(output_data, sort_keys=True, default=str)
        
        input_hash = hashlib.sha256(input_str.encode()).hexdigest()[:16]
        output_hash = hashlib.sha256(output_str.encode()).hexdigest()[:16]
        
        # Create entry
        entry = AuditEntry(
            entry_id=self._generate_entry_id(),
            timestamp=datetime.now().isoformat(),
            action=action,
            user_id=user_id,
            input_hash=input_hash,
            output_hash=output_hash,
            details=details or {},
            duration_ms=duration_ms,
            status=status,
            error=error,
        )
        
        # Store entry
        self.entries.append(entry)
        self._persist_entry(entry)
        
        return entry
    
    def log_citation_verify(
        self,
        citation: str,
        result: dict,
        duration_ms: float = 0,
    ) -> AuditEntry:
        """Log a citation verification operation"""
        return self.log(
            action="citation_verify",
            input_data={"citation": citation},
            output_data=result,
            details={"verified": result.get("is_valid", False)},
            duration_ms=duration_ms,
        )
    
    def log_privilege_scan(
        self,
        text_length: int,
        detections: List[dict],
        duration_ms: float = 0,
    ) -> AuditEntry:
        """Log a privilege scan operation"""
        return self.log(
            action="privilege_scan",
            input_data={"text_length": text_length},
            output_data={"detections": len(detections)},
            details={
                "detection_count": len(detections),
                "types": list(set(d.get("type") for d in detections)),
            },
            duration_ms=duration_ms,
        )
    
    def log_document_generate(
        self,
        document_type: str,
        input_text: str,
        output_text: str,
        confidence_score: float,
        duration_ms: float = 0,
    ) -> AuditEntry:
        """Log a document generation operation"""
        return self.log(
            action="document_generate",
            input_data={"document_type": document_type, "input": input_text[:100]},
            output_data={"output": output_text[:100], "confidence": confidence_score},
            details={"document_type": document_type},
            duration_ms=duration_ms,
        )
    
    def get_history(
        self,
        action: Optional[str] = None,
        user_id: Optional[str] = None,
        limit: int = 100,
    ) -> List[AuditEntry]:
        """Get audit history with optional filters"""
        filtered = self.entries
        
        if action:
            filtered = [e for e in filtered if e.action == action]
        
        if user_id:
            filtered = [e for e in filtered if e.user_id == user_id]
        
        return filtered[-limit:]
    
    def generate_report(self, entries: List[AuditEntry] = None) -> dict:
        """Generate audit report"""
        if entries is None:
            entries = self.entries
        
        report = {
            "total_operations": len(entries),
            "by_action": {},
            "by_status": {},
            "success_rate": 0,
            "avg_duration_ms": 0,
            "time_range": {
                "start": entries[0].timestamp if entries else None,
                "end": entries[-1].timestamp if entries else None,
            }
        }
        
        for entry in entries:
            # Count by action
            if entry.action not in report["by_action"]:
                report["by_action"][entry.action] = 0
            report["by_action"][entry.action] += 1
            
            # Count by status
            if entry.status not in report["by_status"]:
                report["by_status"][entry.status] = 0
            report["by_status"][entry.status] += 1
        
        # Calculate success rate
        success_count = report["by_status"].get("success", 0)
        report["success_rate"] = success_count / len(entries) if entries else 0
        
        # Calculate average duration
        durations = [e.duration_ms for e in entries if e.duration_ms > 0]
        report["avg_duration_ms"] = sum(durations) / len(durations) if durations else 0
        
        return report
    
    def _generate_entry_id(self) -> str:
        """Generate unique entry ID"""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        random_part = hashlib.sha256(str(datetime.now()).encode()).hexdigest()[:8]
        return f"audit_{timestamp}_{random_part}"
    
    def _persist_entry(self, entry: AuditEntry):
        """Persist entry to disk"""
        # Use day-based file partitioning
        day = entry.timestamp[:10]
        file_path = self.storage_path / f"{day}.jsonl"
        
        with open(file_path, "a") as f:
            f.write(json.dumps(asdict(entry), default=str) + "\n")

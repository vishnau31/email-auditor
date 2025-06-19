from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
from enum import Enum


class RuleStatus(str, Enum):
    PASS = "pass"
    FAIL = "fail"


class RuleResult(BaseModel):
    rule_name: str
    status: RuleStatus
    score: float
    justification: str
    details: Optional[Dict[str, Any]] = None


class AuditResult(BaseModel):
    audit_timestamp: str
    overall_score: float
    summary: str
    recommendations: List[str]
    rule_results: List[RuleResult]
    statistics: Dict[str, Any]
    email_thread: Optional[Any] = None
    
    @property
    def passed_rules(self) -> List[RuleResult]:
        return [result for result in self.rule_results if result.status == RuleStatus.PASS]
    
    @property
    def failed_rules(self) -> List[RuleResult]:
        return [result for result in self.rule_results if result.status == RuleStatus.FAIL] 
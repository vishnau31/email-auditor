from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from loguru import logger

from ..models import EmailThread, RuleResult
from ..models.audit import RuleStatus


class BaseRule(ABC):
    
    def __init__(self, name: str, description: str, weight: float = 1.0):
        self.name = name
        self.description = description
        self.weight = weight
    
    @abstractmethod
    def evaluate(self, email_thread: EmailThread) -> RuleResult:
        pass
    
    def _create_result(self, status: RuleStatus, score: float, justification: str, details: Optional[Dict[str, Any]] = None) -> RuleResult:
        return RuleResult(
            rule_name=self.name,
            status=status,
            score=score,
            justification=justification,
            details=details
        )
    
    def _log_evaluation(self, email_thread: EmailThread, result: RuleResult):
        logger.info(f"Rule {self.name}: {result.status} - {result.justification}")
    
    def run(self, email_thread: EmailThread) -> RuleResult:
        try:
            result = self.evaluate(email_thread)
            self._log_evaluation(email_thread, result)
            return result
        except Exception as e:
            logger.error(f"Rule {self.name} failed: {str(e)}")
            return self._create_result(
                status=RuleStatus.FAIL,
                score=0.0,
                justification=f"Rule evaluation failed: {str(e)}"
            ) 
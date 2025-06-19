from ..models import EmailThread, RuleResult
from ..models.audit import RuleStatus
from .base import BaseRule


class LengthRule(BaseRule):
    
    def __init__(self):
        super().__init__("LengthRule", "Checks email length appropriateness", 1.0)
    
    def evaluate(self, email_thread: EmailThread) -> RuleResult:
        if not email_thread.messages:
            return self._create_result(
                status=RuleStatus.FAIL,
                score=0.0,
                justification="No messages in thread"
            )
        
        first_message = email_thread.messages[0]
        content_length = len(first_message.plain_text.strip())
        
        if content_length < 50:
            return self._create_result(
                status=RuleStatus.FAIL,
                score=0.0,
                justification="Email is too short"
            )
        elif content_length > 2000:
            return self._create_result(
                status=RuleStatus.FAIL,
                score=0.0,
                justification="Email is too long"
            )
        else:
            return self._create_result(
                status=RuleStatus.PASS,
                score=1.0,
                justification=f"Email length is appropriate ({content_length} characters)"
            ) 
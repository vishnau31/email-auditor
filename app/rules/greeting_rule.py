from ..models import EmailThread, RuleResult
from ..models.audit import RuleStatus
from .base import BaseRule


class GreetingRule(BaseRule):
    
    def __init__(self):
        super().__init__("GreetingRule", "Checks if email contains a greeting", 1.0)
    
    def evaluate(self, email_thread: EmailThread) -> RuleResult:
        if not email_thread.messages:
            return self._create_result(
                status=RuleStatus.FAIL,
                score=0.0,
                justification="No messages in thread"
            )
        
        first_message = email_thread.messages[0]
        content = first_message.plain_text.lower()
        
        greetings = [
            'dear', 'hello', 'hi', 'hey', 'good morning', 'good afternoon',
            'good evening', 'greetings', 'salutations'
        ]
        
        for greeting in greetings:
            if greeting in content[:200]:
                return self._create_result(
                    status=RuleStatus.PASS,
                    score=1.0,
                    justification="Email contains appropriate greeting"
                )
        
        return self._create_result(
            status=RuleStatus.FAIL,
            score=0.0,
            justification="Email lacks appropriate greeting"
        ) 
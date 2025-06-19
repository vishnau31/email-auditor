from ..models import EmailThread, RuleResult
from ..models.audit import RuleStatus
from .base import BaseRule


class AttachmentRule(BaseRule):
    
    def __init__(self):
        super().__init__("AttachmentRule", "Checks for image attachments", 1.0)
    
    def evaluate(self, email_thread: EmailThread) -> RuleResult:
        if not email_thread.messages:
            return self._create_result(
                status=RuleStatus.FAIL,
                score=0.0,
                justification="No messages in thread"
            )
        
        first_message = email_thread.messages[0]
        
        if not first_message.attachments:
            return self._create_result(
                status=RuleStatus.FAIL,
                score=0.0,
                justification="No attachments found"
            )
        
        image_attachments = [
            att for att in first_message.attachments
            if att.content_type.startswith('image/')
        ]
        
        if image_attachments:
            return self._create_result(
                status=RuleStatus.PASS,
                score=1.0,
                justification="At least one image attachment found"
            )
        else:
            return self._create_result(
                status=RuleStatus.FAIL,
                score=0.0,
                justification="No image attachments found"
            ) 
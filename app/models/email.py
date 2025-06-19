from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
from datetime import datetime


class Attachment(BaseModel):
    filename: str
    content_type: str
    size: int
    content_id: Optional[str] = None


class EmailMessage(BaseModel):
    headers: Dict[str, str]
    content: Dict[str, str]
    metadata: Dict[str, Any]
    attachments: Optional[List[Attachment]] = None
    
    @property
    def subject(self) -> str:
        return self.headers.get('subject', '')
    
    @property
    def sender(self) -> str:
        return self.headers.get('from', '')
    
    @property
    def recipient(self) -> str:
        return self.headers.get('to', '')
    
    @property
    def date(self) -> Optional[datetime]:
        return self.metadata.get('parsed_date')
    
    @property
    def plain_text(self) -> str:
        return self.content.get('plain_text', '')
    
    @property
    def html(self) -> str:
        return self.content.get('html', '')


class EmailThread(BaseModel):
    messages: List[EmailMessage]
    
    @property
    def first_message(self) -> Optional[EmailMessage]:
        return self.messages[0] if self.messages else None
    
    @property
    def last_message(self) -> Optional[EmailMessage]:
        return self.messages[-1] if self.messages else None
    
    @property
    def message_count(self) -> int:
        return len(self.messages)
    
    @property
    def subject(self) -> str:
        if self.first_message:
            return self.first_message.subject
        return ""
    
    @property
    def participants(self) -> List[str]:
        participants = set()
        for message in self.messages:
            if message.sender:
                participants.add(message.sender)
            if message.recipient:
                participants.add(message.recipient)
        return list(participants) 
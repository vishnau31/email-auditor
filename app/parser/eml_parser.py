import email
from email import policy
from email.parser import BytesParser
from email.utils import parsedate_to_datetime
from typing import Dict, List, Optional, Tuple, Any
import mimetypes
import base64
from datetime import datetime
from loguru import logger


class EMLParser:
    
    def __init__(self):
        self.policy = policy.default
        self.parser = BytesParser(policy=self.policy)
    
    def parse_eml_file(self, file_path: str) -> Dict[str, Any]:
        try:
            with open(file_path, 'rb') as f:
                email_data = f.read()
            
            return self.parse_eml_data(email_data)
            
        except FileNotFoundError:
            logger.error(f"EML file not found: {file_path}")
            raise
        except Exception as e:
            logger.error(f"Error parsing EML file {file_path}: {str(e)}")
            raise
    
    def parse_eml_data(self, email_data: bytes) -> Dict[str, Any]:
        try:
            message = self.parser.parsebytes(email_data)
            
            parsed_email = {
                'headers': self._extract_headers(message),
                'content': self._extract_content(message),
                'metadata': self._extract_metadata(message),
                'attachments': self._extract_attachments(message)
            }
            
            logger.info(f"Parsed email: {parsed_email['headers'].get('subject', 'No subject')}")
            return parsed_email
            
        except Exception as e:
            logger.error(f"Error parsing email data: {str(e)}")
            raise
    
    def _extract_headers(self, message) -> Dict[str, str]:
        headers = {}
        
        essential_headers = ['from', 'to', 'subject', 'date', 'cc', 'bcc', 'reply-to']
        
        for header in essential_headers:
            value = message.get(header)
            if value:
                headers[header] = str(value)
        
        additional_headers = ['message-id', 'in-reply-to', 'references', 'content-type']
        for header in additional_headers:
            value = message.get(header)
            if value:
                headers[header] = str(value)
        
        return headers
    
    def _extract_content(self, message) -> Dict[str, str]:
        content = {
            'plain_text': '',
            'html': ''
        }
        
        for part in message.walk():
            if part.is_multipart():
                continue
            
            content_type = part.get_content_type()
            
            if content_type == 'text/plain':
                try:
                    text_content = part.get_content()
                    if text_content:
                        content['plain_text'] += text_content
                except Exception as e:
                    logger.warning(f"Error extracting plain text: {str(e)}")
            
            elif content_type == 'text/html':
                try:
                    html_content = part.get_content()
                    if html_content:
                        content['html'] += html_content
                except Exception as e:
                    logger.warning(f"Error extracting HTML: {str(e)}")
        
        return content
    
    def _extract_metadata(self, message) -> Dict[str, Any]:
        metadata = {
            'parsed_date': None
        }
        
        date_header = message.get('date')
        if date_header:
            try:
                metadata['parsed_date'] = parsedate_to_datetime(date_header)
            except Exception as e:
                logger.warning(f"Error parsing date: {str(e)}")
        
        return metadata

    def _extract_attachments(self, message) -> List[Dict[str, Any]]:
        attachments = []
        
        for part in message.walk():
            if part.is_multipart():
                continue
            
            content_type = part.get_content_type()
            
            if content_type.startswith('image/') or part.get_filename():
                try:
                    attachment = {
                        'filename': part.get_filename() or f"attachment_{len(attachments)}",
                        'content_type': content_type,
                        'size': len(part.get_payload(decode=True)) if part.get_payload(decode=True) else 0,
                        'content_id': part.get('content-id')
                    }
                    attachments.append(attachment)
                except Exception as e:
                    logger.warning(f"Error extracting attachment: {str(e)}")
        
        return attachments


def parse_eml_file(file_path: str) -> Dict[str, Any]:
    parser = EMLParser()
    return parser.parse_eml_file(file_path)


def parse_eml_data(email_data: bytes) -> Dict[str, Any]:
    parser = EMLParser()
    return parser.parse_eml_data(email_data) 
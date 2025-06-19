from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from starlette.status import HTTP_400_BAD_REQUEST

from ..parser import parse_eml_data
from ..models import EmailMessage, EmailThread, Attachment
from ..audit import Auditor, ReportGenerator

router = APIRouter(prefix="/api/v1", tags=["audit"])

auditor = Auditor()
report_generator = ReportGenerator()

@router.post("/audit")
async def audit_eml(file: UploadFile = File(...)):
    if not file.filename or not file.filename.endswith(".eml"):
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Only .eml files are supported.")
    content = await file.read()
    try:
        parsed = parse_eml_data(content)
        
        attachments = []
        if parsed.get('attachments'):
            for att_data in parsed['attachments']:
                attachment = Attachment(**att_data)
                attachments.append(attachment)
        
        email_message = EmailMessage(
            headers=parsed['headers'],
            content=parsed['content'],
            metadata=parsed['metadata'],
            attachments=attachments
        )
        email_thread = EmailThread(messages=[email_message])
    except Exception as e:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"Failed to parse EML: {str(e)}")
    audit_result = auditor.audit_email_thread(email_thread)
    json_report = report_generator.generate_json_report(audit_result)
    return JSONResponse(content=json_report) 
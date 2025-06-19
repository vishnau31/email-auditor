import json
from typing import Dict, Any
from loguru import logger

from ..models import AuditResult


class ReportGenerator:
    
    def __init__(self):
        pass
    
    def generate_json_report(self, audit_result: AuditResult) -> Dict[str, Any]:
        try:
            report = {
                "audit_timestamp": audit_result.audit_timestamp,
                "overall_score": audit_result.overall_score,
                "summary": audit_result.summary,
                "recommendations": audit_result.recommendations,
                "rule_results": [
                    {
                        "rule_name": result.rule_name,
                        "status": result.status,
                        "score": result.score,
                        "justification": result.justification,
                        "details": result.details
                    }
                    for result in audit_result.rule_results
                ],
                "statistics": audit_result.statistics
            }
            
            logger.info(f"Generated JSON report with {len(audit_result.rule_results)} rules")
            return report
            
        except Exception as e:
            logger.error(f"Failed to generate JSON report: {str(e)}")
            return {
                "error": "Failed to generate report",
                "message": str(e)
            } 
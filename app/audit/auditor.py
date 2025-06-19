from datetime import datetime
from typing import List
from loguru import logger

from ..models import EmailThread, AuditResult, RuleResult
from ..models.audit import RuleStatus
from ..rules.registry import RuleRegistry


class Auditor:
    
    def __init__(self):
        self.rule_registry = RuleRegistry()
    
    def audit_email_thread(self, email_thread: EmailThread) -> AuditResult:
        logger.info(f"Starting audit for {len(email_thread.messages)} messages")
        
        try:
            rule_results = self.rule_registry.execute_all_rules(email_thread)
            
            overall_score = self._calculate_overall_score(rule_results)
            summary = self._generate_summary(rule_results)
            recommendations = self._generate_recommendations(rule_results)
            statistics = self._calculate_statistics(rule_results)
            
            return AuditResult(
                audit_timestamp=datetime.utcnow().isoformat(),
                overall_score=overall_score,
                summary=summary,
                recommendations=recommendations,
                rule_results=rule_results,
                statistics=statistics,
                email_thread=email_thread
            )
            
        except Exception as e:
            logger.error(f"Audit failed: {str(e)}")
            return self._create_error_result(email_thread, str(e))
    
    def _calculate_overall_score(self, rule_results: List[RuleResult]) -> float:
        if not rule_results:
            return 0.0
        
        total_score = sum(result.score for result in rule_results)
        return total_score / len(rule_results)
    
    def _generate_summary(self, rule_results: List[RuleResult]) -> str:
        total_count = len(rule_results)
        passed_count = sum(1 for result in rule_results if result.status == RuleStatus.PASS)
        pass_rate = passed_count / total_count if total_count > 0 else 0.0
        
        if pass_rate >= 0.8:
            quality = "excellent"
        elif pass_rate >= 0.6:
            quality = "good"
        elif pass_rate >= 0.4:
            quality = "fair"
        else:
            quality = "poor"
        
        return f"Email quality is {quality}. {passed_count}/{total_count} rules passed ({pass_rate:.1%})."
    
    def _generate_recommendations(self, rule_results: List[RuleResult]) -> List[str]:
        recommendations = []
        
        for result in rule_results:
            if result.status == RuleStatus.FAIL:
                if "greeting" in result.rule_name.lower():
                    recommendations.append("Add a proper greeting to your email")
                elif "length" in result.rule_name.lower():
                    if "short" in result.justification.lower():
                        recommendations.append("Your email is too short - provide more context")
                    elif "long" in result.justification.lower():
                        recommendations.append("Your email is too long - be more concise")
                elif "attachment" in result.rule_name.lower():
                    recommendations.append("Consider adding visual content to your email")
        
        if not recommendations:
            recommendations.append("Great job! Your email meets all quality standards.")
        
        return recommendations
    
    def _calculate_statistics(self, rule_results: List[RuleResult]) -> dict:
        total_rules = len(rule_results)
        passed_rules = sum(1 for result in rule_results if result.status == RuleStatus.PASS)
        failed_rules = total_rules - passed_rules
        pass_rate = passed_rules / total_rules if total_rules > 0 else 0.0
        
        return {
            "total_rules": total_rules,
            "passed_rules": passed_rules,
            "failed_rules": failed_rules,
            "pass_rate": pass_rate
        }
    
    def _create_error_result(self, email_thread: EmailThread, error_message: str) -> AuditResult:
        return AuditResult(
            audit_timestamp=datetime.utcnow().isoformat(),
            overall_score=0.0,
            summary=f"Audit failed: {error_message}",
            recommendations=["Please try again or contact support if the issue persists."],
            rule_results=[],
            statistics={"total_rules": 0, "passed_rules": 0, "failed_rules": 0, "pass_rate": 0.0},
            email_thread=email_thread
        ) 
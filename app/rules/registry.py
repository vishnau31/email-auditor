import os
import importlib
import inspect
from typing import Dict, List, Type, Optional
from loguru import logger

from .base import BaseRule
from ..models import EmailThread, RuleResult
from ..models.audit import RuleStatus


class RuleRegistry:
    
    def __init__(self):
        self.rules: Dict[str, BaseRule] = {}
        self._discover_rules()
    
    def _discover_rules(self):
        rules_dir = os.path.dirname(__file__)
        
        for filename in os.listdir(rules_dir):
            if filename.endswith('.py') and not filename.startswith('_'):
                module_name = filename[:-3]
                
                if module_name in ['base', 'registry']:
                    continue
                
                try:
                    module = importlib.import_module(f'.{module_name}', package='app.rules')
                    
                    for name, obj in inspect.getmembers(module):
                        if (inspect.isclass(obj) and 
                            issubclass(obj, BaseRule) and 
                            obj != BaseRule):
                            
                            rule_instance = obj()
                            self.rules[rule_instance.name] = rule_instance
                            logger.info(f"Loaded rule: {rule_instance.name}")
                            
                except Exception as e:
                    logger.error(f"Failed to load rule from {module_name}: {str(e)}")
    
    def get_rule(self, rule_name: str) -> Optional[BaseRule]:
        return self.rules.get(rule_name)
    
    def get_all_rules(self) -> List[BaseRule]:
        return list(self.rules.values())
    
    def execute_rule(self, rule_name: str, email_thread: EmailThread) -> RuleResult:
        rule = self.get_rule(rule_name)
        if not rule:
            return RuleResult(
                rule_name=rule_name,
                status=RuleStatus.FAIL,
                score=0.0,
                justification=f"Rule '{rule_name}' not found"
            )
        
        return rule.run(email_thread)
    
    def execute_all_rules(self, email_thread: EmailThread) -> List[RuleResult]:
        results = []
        for rule in self.get_all_rules():
            result = rule.run(email_thread)
            results.append(result)
        
        return results


rule_registry = RuleRegistry() 
"""
Email Audit Service - EML Parser Package
"""

from .eml_parser import EMLParser, parse_eml_file, parse_eml_data

__all__ = ['EMLParser', 'parse_eml_file', 'parse_eml_data'] 
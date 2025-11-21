"""
Data ingestion module - handles multiple file formats
"""

from .base_handler import BaseHandler
from .excel_handler import ExcelHandler
from .csv_handler import CSVHandler
from .json_handler import JSONHandler
from .ppt_handler import PPTHandler
from .database_handler import DatabaseHandler
from .registry import FormatRegistry

__all__ = [
    'BaseHandler',
    'ExcelHandler',
    'CSVHandler',
    'JSONHandler',
    'PPTHandler',
    'DatabaseHandler',
    'FormatRegistry',
]


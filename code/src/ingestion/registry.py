"""
Format registry for managing data handlers
"""
from typing import Dict, List, Optional, Type
from pathlib import Path
from .base_handler import BaseHandler
from .excel_handler import ExcelHandler
from .csv_handler import CSVHandler
from .json_handler import JSONHandler
from .ppt_handler import PPTHandler
from .word_handler import WordHandler
from .database_handler import DatabaseHandler
from .pdf_handler import PDFHandler
from .image_handler import ImageHandler
from .text_handler import TextHandler
from .archive_handler import ArchiveHandler

# Enterprise connectors
from .enterprise_connectors import (
    SalesforceConnector,
    HubSpotConnector,
    DynamicsConnector,
    SAPConnector,
    OneDriveConnector,
    GoogleDriveConnector,
    OracleERPConnector,
    NetSuiteConnector
)


class FormatRegistry:
    """Registry for managing format handlers"""
    
    def __init__(self):
        self._handlers: List[BaseHandler] = []
        self._register_default_handlers()
    
    def _register_default_handlers(self):
        """Register default format handlers"""
        default_handlers = [
            # File handlers
            ExcelHandler(),
            CSVHandler(),
            JSONHandler(),
            PPTHandler(),
            WordHandler(),
            PDFHandler(),
            ImageHandler(),
            TextHandler(),
            ArchiveHandler(),
            # Database
            DatabaseHandler(),
            # Enterprise connectors
            SalesforceConnector(),
            HubSpotConnector(),
            DynamicsConnector(),
            SAPConnector(),
            OneDriveConnector(),
            GoogleDriveConnector(),
            OracleERPConnector(),
            NetSuiteConnector(),
        ]
        
        for handler in default_handlers:
            self.register(handler)
    
    def register(self, handler: BaseHandler):
        """Register a new format handler"""
        if not isinstance(handler, BaseHandler):
            raise TypeError("Handler must be an instance of BaseHandler")
        self._handlers.append(handler)
    
    def get_handler(self, file_path: str) -> Optional[BaseHandler]:
        """Get appropriate handler for a file"""
        for handler in self._handlers:
            if handler.can_handle(file_path):
                return handler
        return None
    
    def get_supported_formats(self) -> List[str]:
        """Get list of all supported file extensions"""
        formats = set()
        for handler in self._handlers:
            formats.update(handler.get_supported_extensions())
        return sorted(list(formats))
    
    def can_handle(self, file_path: str) -> bool:
        """Check if any handler can process the file"""
        return self.get_handler(file_path) is not None


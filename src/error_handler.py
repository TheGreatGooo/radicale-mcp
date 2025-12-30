"""
Error Handler for MCP CalDAV Application
Centralized error handling and logging for the application.
"""

import logging
import json
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class ErrorHandler:
    """Centralized error handling for the MCP CalDAV application."""
    
    # Standard error codes
    INVALID_PARAMETERS = 1001
    RESOURCE_NOT_FOUND = 1002
    AUTHENTICATION_FAILED = 1003
    INTERNAL_ERROR = 1004
    OPERATION_NOT_SUPPORTED = 1005
    
    @staticmethod
    def handle_exception(exception: Exception, method: str = "unknown") -> Dict[str, Any]:
        """
        Handle an exception and return an appropriate error response.
        
        Args:
            exception: The exception that occurred
            method: The method that caused the error
            
        Returns:
            Dictionary containing error information in MCP format
        """
        error_info = {
            "code": ErrorHandler.INTERNAL_ERROR,
            "message": str(exception),
            "data": {
                "method": method,
                "exception_type": type(exception).__name__
            }
        }
        
        # Log the error
        logger.error(f"Error in {method}: {exception}", exc_info=True)
        
        return error_info
    
    @staticmethod
    def create_error_response(error_code: int, message: str, data: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Create a standardized error response.
        
        Args:
            error_code: The error code
            message: Error message
            data: Additional error data
            
        Returns:
            Dictionary containing error response in MCP format
        """
        response = {
            "jsonrpc": "2.0",
            "error": {
                "code": error_code,
                "message": message
            }
        }
        
        if data:
            response["error"]["data"] = data
            
        return response
    
    @staticmethod
    def create_success_response(result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a standardized success response.
        
        Args:
            result: The result data to include in response
            
        Returns:
            Dictionary containing success response in MCP format
        """
        return {
            "jsonrpc": "2.0",
            "result": result
        }
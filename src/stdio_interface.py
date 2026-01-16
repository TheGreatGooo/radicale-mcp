"""
STDIO Interface for MCP CalDAV Application
Implements the MCP protocol for communication over STDIO.
"""

import sys
import json
import logging
from typing import Dict, Any, Optional
from caldav_client import CalDAVClient
from error_handler import ErrorHandler

logger = logging.getLogger(__name__)


class StdioInterface:
    """Handles STDIO communication according to MCP protocol."""

    def __init__(self, config_manager):
        """
        Initialize the STDIO interface.

        Args:
            config_manager: Configuration manager instance
        """
        self.config_manager = config_manager
        self.caldav_client = CalDAVClient(config_manager)
        self.error_handler = ErrorHandler()
        self.running = False

    def start(self) -> None:
        """
        Start the STDIO interface loop.
        """
        logger.info("Starting STDIO interface")
        self.running = True

        # Connect to CalDAV server
        if not self.caldav_client.connect():
            logger.error(
                "Failed to connect to CalDAV server. Continuing in offline mode."
            )

        try:
            while self.running:
                # Read a line from stdin
                line = sys.stdin.readline()
                if not line:
                    break

                # Parse the JSON message
                try:
                    message = json.loads(line.strip())
                    response = self.handle_message(message)

                    # Write response to stdout
                    if response:
                        sys.stdout.write(json.dumps(response) + "\n")
                        sys.stdout.flush()

                except json.JSONDecodeError as e:
                    logger.error(f"Invalid JSON received: {e}")
                    error_response = self.error_handler.create_error_response(
                        ErrorHandler.INVALID_PARAMETERS, "Invalid JSON format"
                    )
                    sys.stdout.write(json.dumps(error_response) + "\n")
                    sys.stdout.flush()

        except KeyboardInterrupt:
            logger.info("STDIO interface interrupted by user")
        except Exception as e:
            logger.error(f"Error in STDIO interface: {e}")
        finally:
            self.stop()

    def stop(self) -> None:
        """Stop the STDIO interface."""
        self.running = False
        self.caldav_client.disconnect()
        logger.info("STDIO interface stopped")

    def handle_message(self, message: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Handle an incoming MCP message.

        Args:
            message: The incoming JSON message

        Returns:
            Response dictionary or None if error
        """
        try:
            # Validate message structure
            if "jsonrpc" not in message or message["jsonrpc"] != "2.0":
                return self.error_handler.create_error_response(
                    ErrorHandler.INVALID_PARAMETERS, "Invalid JSON-RPC version"
                )

            if "method" not in message:
                return self.error_handler.create_error_response(
                    ErrorHandler.INVALID_PARAMETERS, "Missing method"
                )

            method = message["method"]
            params = message.get("params", {})
            request_id = message.get("id", "unknown")

            logger.debug(f"Handling method: {method}")

            # Route to appropriate handler
            if method.startswith("caldav.event."):
                return self.handle_event_operation(method, params, request_id)
            elif method.startswith("caldav.journal."):
                return self.handle_journal_operation(method, params, request_id)
            elif method.startswith("caldav.todo."):
                return self.handle_todo_operation(method, params, request_id)
            else:
                return self.error_handler.create_error_response(
                    ErrorHandler.OPERATION_NOT_SUPPORTED,
                    f"Unsupported method: {method}",
                )

        except Exception as e:
            error_info = self.error_handler.handle_exception(e, "handle_message")
            return self.error_handler.create_error_response(
                error_info["code"], error_info["message"], error_info["data"]
            )

    def handle_event_operation(
        self, method: str, params: Dict[str, Any], request_id: str
    ) -> Dict[str, Any]:
        """
        Handle event-related operations.

        Args:
            method: The method name
            params: Method parameters
            request_id: Request ID

        Returns:
            Response dictionary
        """
        try:
            if method == "caldav.event.create":
                result = self.create_event(params)
                return self.error_handler.create_success_response(result)

            elif method == "caldav.event.read":
                result = self.read_event(params.get("id"))
                return self.error_handler.create_success_response(result)

            elif method == "caldav.event.update":
                result = self.update_event(params.get("id"), params.get("data", {}))
                return self.error_handler.create_success_response(result)

            elif method == "caldav.event.delete":
                result = self.delete_event(params.get("id"))
                return self.error_handler.create_success_response(result)

            elif method == "caldav.event.list":
                result = self.list_events()
                return self.error_handler.create_success_response(result)

            else:
                return self.error_handler.create_error_response(
                    ErrorHandler.OPERATION_NOT_SUPPORTED,
                    f"Unsupported event method: {method}",
                )
        except Exception as e:
            error_info = self.error_handler.handle_exception(e, method)
            return self.error_handler.create_error_response(
                error_info["code"], error_info["message"], error_info["data"]
            )

    def handle_journal_operation(
        self, method: str, params: Dict[str, Any], request_id: str
    ) -> Dict[str, Any]:
        """
        Handle journal-related operations.

        Args:
            method: The method name
            params: Method parameters
            request_id: Request ID

        Returns:
            Response dictionary
        """
        try:
            if method == "caldav.journal.create":
                result = self.create_journal(params)
                return self.error_handler.create_success_response(result)

            elif method == "caldav.journal.read":
                result = self.read_journal(params.get("id"))
                return self.error_handler.create_success_response(result)

            elif method == "caldav.journal.update":
                result = self.update_journal(params.get("id"), params.get("data", {}))
                return self.error_handler.create_success_response(result)

            elif method == "caldav.journal.delete":
                result = self.delete_journal(params.get("id"))
                return self.error_handler.create_success_response(result)

            elif method == "caldav.journal.list":
                result = self.list_journals()
                return self.error_handler.create_success_response(result)

            else:
                return self.error_handler.create_error_response(
                    ErrorHandler.OPERATION_NOT_SUPPORTED,
                    f"Unsupported journal method: {method}",
                )
        except Exception as e:
            error_info = self.error_handler.handle_exception(e, method)
            return self.error_handler.create_error_response(
                error_info["code"], error_info["message"], error_info["data"]
            )

    def handle_todo_operation(
        self, method: str, params: Dict[str, Any], request_id: str
    ) -> Dict[str, Any]:
        """
        Handle todo-related operations.

        Args:
            method: The method name
            params: Method parameters
            request_id: Request ID

        Returns:
            Response dictionary
        """
        try:
            if method == "caldav.todo.create":
                result = self.create_todo(params)
                return self.error_handler.create_success_response(result)

            elif method == "caldav.todo.read":
                result = self.read_todo(params.get("id"))
                return self.error_handler.create_success_response(result)

            elif method == "caldav.todo.update":
                result = self.update_todo(params.get("id"), params.get("data", {}))
                return self.error_handler.create_success_response(result)

            elif method == "caldav.todo.delete":
                result = self.delete_todo(params.get("id"))
                return self.error_handler.create_success_response(result)

            elif method == "caldav.todo.list":
                result = self.list_todos()
                return self.error_handler.create_success_response(result)

            else:
                return self.error_handler.create_error_response(
                    ErrorHandler.OPERATION_NOT_SUPPORTED,
                    f"Unsupported todo method: {method}",
                )
        except Exception as e:
            error_info = self.error_handler.handle_exception(e, method)
            return self.error_handler.create_error_response(
                error_info["code"], error_info["message"], error_info["data"]
            )

    # Event operations (placeholder implementations)
    def create_event(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new event."""
        event_id = self.caldav_client.create_event(event_data)
        if event_id:
            return {"id": event_id, "status": "created"}
        else:
            raise Exception("Failed to create event")

    def read_event(self, event_id: str) -> Dict[str, Any]:
        """Read an existing event."""
        event_data = self.caldav_client.read_event(event_id)
        if event_data:
            return event_data
        else:
            raise Exception(f"Event not found: {event_id}")

    def update_event(self, event_id: str, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing event."""
        success = self.caldav_client.update_event(event_id, event_data)
        if success:
            return {"id": event_id, "status": "updated"}
        else:
            raise Exception(f"Failed to update event: {event_id}")

    def delete_event(self, event_id: str) -> Dict[str, Any]:
        """Delete an event."""
        success = self.caldav_client.delete_event(event_id)
        if success:
            return {"id": event_id, "status": "deleted"}
        else:
            raise Exception(f"Failed to delete event: {event_id}")

    def list_events(self) -> Dict[str, Any]:
        """List all events."""
        # Placeholder implementation
        return {"events": [], "count": 0}

    # Journal operations (placeholder implementations)
    def create_journal(self, journal_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new journal entry."""
        journal_id = self.caldav_client.create_journal(journal_data)
        if journal_id:
            return {"id": journal_id, "status": "created"}
        else:
            raise Exception("Failed to create journal")

    def read_journal(self, journal_id: str) -> Dict[str, Any]:
        """Read an existing journal entry."""
        journal_data = self.caldav_client.read_journal(journal_id)
        if journal_data:
            return journal_data
        else:
            raise Exception(f"Journal not found: {journal_id}")

    def update_journal(
        self, journal_id: str, journal_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update an existing journal entry."""
        success = self.caldav_client.update_journal(journal_id, journal_data)
        if success:
            return {"id": journal_id, "status": "updated"}
        else:
            raise Exception(f"Failed to update journal: {journal_id}")

    def delete_journal(self, journal_id: str) -> Dict[str, Any]:
        """Delete a journal entry."""
        success = self.caldav_client.delete_journal(journal_id)
        if success:
            return {"id": journal_id, "status": "deleted"}
        else:
            raise Exception(f"Failed to delete journal: {journal_id}")

    def list_journals(self) -> Dict[str, Any]:
        """List all journal entries."""
        # Placeholder implementation
        return {"journals": [], "count": 0}

    # Todo operations (placeholder implementations)
    def create_todo(self, todo_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new todo item."""
        todo_id = self.caldav_client.create_todo(todo_data)
        if todo_id:
            return {"id": todo_id, "status": "created"}
        else:
            raise Exception("Failed to create todo")

    def read_todo(self, todo_id: str) -> Dict[str, Any]:
        """Read an existing todo item."""
        todo_data = self.caldav_client.read_todo(todo_id)
        if todo_data:
            return todo_data
        else:
            raise Exception(f"Todo not found: {todo_id}")

    def update_todo(self, todo_id: str, todo_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing todo item."""
        success = self.caldav_client.update_todo(todo_id, todo_data)
        if success:
            return {"id": todo_id, "status": "updated"}
        else:
            raise Exception(f"Failed to update todo: {todo_id}")

    def delete_todo(self, todo_id: str) -> Dict[str, Any]:
        """Delete a todo item."""
        success = self.caldav_client.delete_todo(todo_id)
        if success:
            return {"id": todo_id, "status": "deleted"}
        else:
            raise Exception(f"Failed to delete todo: {todo_id}")

    def list_todos(self) -> Dict[str, Any]:
        """List all todo items."""
        # Placeholder implementation
        return {"todos": [], "count": 0}

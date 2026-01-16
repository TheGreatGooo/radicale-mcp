#!/usr/bin/env python3
"""
FastMCP Server Implementation for CalDAV Operations
This demonstrates how to use the fastmcp library with the existing CalDAV functionality.
"""

from fastmcp import FastMCP
from caldav_client import CalDAVClient
from config_manager import ConfigManager
from models.event import Event
from models.todo import Todo
from datetime import datetime

# Initialize the MCP server
mcp = FastMCP("Radicale MCP server 🚀")

# Initialize configuration and client
config_manager = ConfigManager()
caldav_client = CalDAVClient(config_manager)


@mcp.tool
def get_events() -> list:
    """Get all events from the CalDAV server."""
    try:
        # Check if connected, if not, connect
        if not caldav_client.is_connected():
            success = caldav_client.connect()
            if not success:
                return [{"error": "Failed to connect to CalDAV server"}]

        events = caldav_client.get_events()
        return [event.to_dict() for event in events]
    except Exception as e:
        return [{"error": f"Failed to get events: {str(e)}"}]


@mcp.tool
def connect() -> dict:
    """Connect to the CalDAV server."""
    try:
        success = caldav_client.connect()
        if success:
            return {
                "status": "connected",
                "message": "Successfully connected to CalDAV server",
            }
        else:
            return {"status": "failed", "message": "Failed to connect to CalDAV server"}
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error connecting to CalDAV server: {str(e)}",
        }


@mcp.tool
def reconnect() -> dict:
    """Reconnect to the CalDAV server."""
    try:
        # Disconnect first
        caldav_client.disconnect()
        # Then reconnect
        success = caldav_client.connect()
        if success:
            return {
                "status": "reconnected",
                "message": "Successfully reconnected to CalDAV server",
            }
        else:
            return {
                "status": "failed",
                "message": "Failed to reconnect to CalDAV server",
            }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error reconnecting to CalDAV server: {str(e)}",
        }


@mcp.tool
def create_event(title: str, start_time: str, end_time: str) -> dict:
    """Create a new event on the CalDAV server.

    Args:
        title: Title of the event
        start_time: Start time of the event in ISO format (e.g., '2026-01-14T02:16:17.478')
        end_time: End time of the event in ISO format (e.g., '2026-01-14T02:16:17.478')

    Returns:
        Dictionary with event creation result
    """
    try:
        # Check if connected, if not, connect
        if not caldav_client.is_connected():
            success = caldav_client.connect()
            if not success:
                return {"error": "Failed to connect to CalDAV server"}

        # Convert string timestamps to datetime objects
        start_dt = datetime.fromisoformat(start_time)
        end_dt = datetime.fromisoformat(end_time)

        event = Event(title=title, start_time=start_dt, end_time=end_dt)
        created_event = caldav_client.create_event(event)
        return created_event.to_dict()
    except Exception as e:
        return {"error": f"Failed to create event: {str(e)}"}


@mcp.tool
def create_recurring_event(
    title: str,
    start_time: str,
    end_time: str,
    frequency: str,
    interval: int = 1,
    count: int = None,
) -> dict:
    """Create a recurring event on the CalDAV server.

    Args:
        title: Title of the event
        start_time: Start time of the event in ISO format (e.g., '2026-01-14T02:16:17.478')
        end_time: End time of the event in ISO format (e.g., '2026-01-14T02:16:17.478')
        frequency: Recurrence frequency (YEARLY, MONTHLY, WEEKLY, DAILY)
        interval: Interval between recurrences (default: 1)
        count: Number of occurrences (optional)

    Returns:
        Dictionary with event creation result
    """
    try:
        # Check if connected, if not, connect
        if not caldav_client.is_connected():
            success = caldav_client.connect()
            if not success:
                return {"error": "Failed to connect to CalDAV server"}

        # Create recurrence rule
        rrule = {"FREQ": frequency.upper()}
        if interval != 1:
            rrule["INTERVAL"] = interval
        if count:
            rrule["COUNT"] = count

        # Convert string timestamps to datetime objects
        start_dt = datetime.fromisoformat(start_time)
        end_dt = datetime.fromisoformat(end_time)

        event = Event(title=title, start_time=start_dt, end_time=end_dt, rrule=rrule)
        created_event = caldav_client.create_event(event)
        return created_event.to_dict()
    except Exception as e:
        return {"error": f"Failed to create recurring event: {str(e)}"}


@mcp.tool
def get_todos() -> list:
    """Get all todos from the CalDAV server."""
    try:
        # Check if connected, if not, connect
        if not caldav_client.is_connected():
            success = caldav_client.connect()
            if not success:
                return [{"error": "Failed to connect to CalDAV server"}]

        todos = caldav_client.get_todos()
        return [todo.to_dict() for todo in todos]
    except Exception as e:
        return [{"error": f"Failed to get todos: {str(e)}"}]


@mcp.tool
def create_todo(title: str, due_date: str) -> dict:
    """Create a new todo on the CalDAV server.

    Args:
        title: Title of the todo
        due_date: Due date of the todo in ISO format (e.g., '2026-01-14T02:16:17.478')

    Returns:
        Dictionary with todo creation result
    """
    try:
        # Check if connected, if not, connect
        if not caldav_client.is_connected():
            success = caldav_client.connect()
            if not success:
                return {"error": "Failed to connect to CalDAV server"}

        # Convert string timestamp to datetime object
        due_dt = datetime.fromisoformat(due_date)

        todo = Todo(title=title, due_date=due_dt)
        created_todo = caldav_client.create_todo(todo)
        return created_todo.to_dict()
    except Exception as e:
        return {"error": f"Failed to create todo: {str(e)}"}


def start_server():
    """Start the MCP server using STDIO transport."""
    mcp.run()


if __name__ == "__main__":
    # Run the MCP server using STDIO transport
    start_server()

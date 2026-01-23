#!/usr/bin/env python3
"""
FastMCP Server Implementation for calendar Operations
This demonstrates how to use the fastmcp library with the existing calendar functionality.
"""

from fastmcp import FastMCP
from caldav_client import CalDAVClient
from config_manager import ConfigManager
from models.event import Event
from models.todo import Todo
from datetime import datetime
import os
from zoneinfo import ZoneInfo

# Initialize the MCP server
mcp = FastMCP("Radicale MCP server 🚀")


def _parse_to_tz(dt_str: str) -> datetime:
    """Parse ISO datetime string and convert to target timezone."""
    dt = datetime.fromisoformat(dt_str)
    target_tz_name = os.getenv("TIMEZONE", "America/New_York")
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=ZoneInfo(target_tz_name))

    try:
        target_tz = ZoneInfo(target_tz_name)
    except Exception:
        target_tz = ZoneInfo("America/New_York")
    return dt.astimezone(target_tz)


# Initialize configuration and client
config_manager = ConfigManager()
caldav_client = CalDAVClient(config_manager)


@mcp.tool
def get_events() -> list:
    """Get all events from the calendar."""
    try:
        # Check if connected, if not, connect
        if not caldav_client.is_connected():
            success = caldav_client.connect()
            if not success:
                return [{"error": "Failed to connect to the calendar"}]

        events = caldav_client.get_events()
        return [event.to_dict() for event in events]
    except Exception as e:
        return [{"error": f"Failed to get events: {str(e)}"}]


@mcp.tool
def connect() -> dict:
    """Connect to the calendar."""
    try:
        success = caldav_client.connect()
        if success:
            return {
                "status": "connected",
                "message": "Successfully connected to the calendar",
            }
        else:
            return {"status": "failed", "message": "Failed to connect to the calendar"}
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error connecting to the calendar: {str(e)}",
        }


@mcp.tool
def reconnect() -> dict:
    """Reconnect to the calendar."""
    try:
        # Disconnect first
        caldav_client.disconnect()
        # Then reconnect
        success = caldav_client.connect()
        if success:
            return {
                "status": "reconnected",
                "message": "Successfully reconnected to the calendar",
            }
        else:
            return {
                "status": "failed",
                "message": "Failed to reconnect to the calendar",
            }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error reconnecting to the calendar: {str(e)}",
        }


@mcp.tool
def create_event(title: str, start_time: str, end_time: str) -> dict:
    """Create a new event on the calendar.

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
                return {"error": "Failed to connect to the calendar"}

        # Convert string timestamps to datetime objects
        start_dt = _parse_to_tz(start_time)
        end_dt = _parse_to_tz(end_time)

        event = Event(title=title, start_time=start_dt, end_time=end_dt)
        created_event_id = caldav_client.create_event(event)
        if not created_event_id:
            return {"error": "Failed to create event"}
        # Retrieve full Event object
        event_obj = caldav_client.read_event(created_event_id)
        if hasattr(event_obj, "to_dict"):
            return event_obj.to_dict()
        return {"id": created_event_id}
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
    """Create a recurring event on the calendar.

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
                return {"error": "Failed to connect to the calendar"}

        # Build recurrence rule
        rrule = {"FREQ": frequency.upper()}
        if interval != 1:
            rrule["INTERVAL"] = interval
        if count:
            rrule["COUNT"] = count

        # Parse timestamps
        start_dt = _parse_to_tz(start_time)
        end_dt = _parse_to_tz(end_time)

        # Create Event with recurrence rule
        event = Event(title=title, start_time=start_dt, end_time=end_dt, rrule=rrule)
        created_event_id = caldav_client.create_event(event)
        if not created_event_id:
            return {"error": "Failed to create recurring event"}
        # Retrieve full Event object
        event_obj = caldav_client.read_event(created_event_id)
        if hasattr(event_obj, "to_dict"):
            return event_obj.to_dict()
        return {"id": created_event_id}
    except Exception as e:
        return {"error": f"Failed to create recurring event: {str(e)}"}


@mcp.tool
def get_todos() -> list:
    """Get all todos from the calendar."""
    try:
        # Check if connected, if not, connect
        if not caldav_client.is_connected():
            success = caldav_client.connect()
            if not success:
                return [{"error": "Failed to connect to the calendar"}]

        todos = caldav_client.get_todos()
        return [todo.to_dict() for todo in todos]
    except Exception as e:
        return [{"error": f"Failed to get todos: {str(e)}"}]


# New delete_event tool
@mcp.tool
def delete_event(id: str) -> dict:
    """Delete an event from the calendar."""
    try:
        if not caldav_client.is_connected():
            success = caldav_client.connect()
            if not success:
                return {"error": "Failed to connect to the calendar"}
        result = caldav_client.delete_event(id)
        return {"deleted": result}
    except Exception as e:
        return {"error": f"Failed to delete event: {str(e)}"}


@mcp.tool
def create_todo(title: str, due_date: str) -> dict:
    """Create a new todo on the calendar.

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
                return {"error": "Failed to connect to the calendar"}

        # Convert string timestamp to datetime object
        due_dt = _parse_to_tz(due_date)

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

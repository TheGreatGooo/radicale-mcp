#!/usr/bin/env python3
"""
FastMCP Server Implementation for CalDAV Operations
This demonstrates how to use the fastmcp library with the existing CalDAV functionality.
"""

from fastmcp import FastMCP
from caldav_client import CalDAVClient
from config_manager import ConfigManager
from models.event import Event
from models.journal import Journal
from models.todo import Todo

# Initialize the MCP server
mcp = FastMCP("Radicale MCP server 🚀")

# Initialize configuration and client
config_manager = ConfigManager()
caldav_client = CalDAVClient(config_manager)

@mcp.tool
def get_events() -> list:
    """Get all events from the CalDAV server."""
    try:
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
            return {"status": "connected", "message": "Successfully connected to CalDAV server"}
        else:
            return {"status": "failed", "message": "Failed to connect to CalDAV server"}
    except Exception as e:
        return {"status": "error", "message": f"Error connecting to CalDAV server: {str(e)}"}

@mcp.tool
def reconnect() -> dict:
    """Reconnect to the CalDAV server."""
    try:
        # Disconnect first
        caldav_client.disconnect()
        # Then reconnect
        success = caldav_client.connect()
        if success:
            return {"status": "reconnected", "message": "Successfully reconnected to CalDAV server"}
        else:
            return {"status": "failed", "message": "Failed to reconnect to CalDAV server"}
    except Exception as e:
        return {"status": "error", "message": f"Error reconnecting to CalDAV server: {str(e)}"}

@mcp.tool
def create_event(title: str, start_time: str, end_time: str) -> dict:
    """Create a new event on the CalDAV server."""
    try:
        event = Event(
            title=title,
            start_time=start_time,
            end_time=end_time
        )
        created_event = caldav_client.create_event(event)
        return created_event.to_dict()
    except Exception as e:
        return {"error": f"Failed to create event: {str(e)}"}

@mcp.tool
def get_todos() -> list:
    """Get all todos from the CalDAV server."""
    try:
        todos = caldav_client.get_todos()
        return [todo.to_dict() for todo in todos]
    except Exception as e:
        return [{"error": f"Failed to get todos: {str(e)}"}]

@mcp.tool
def create_todo(title: str, due_date: str) -> dict:
    """Create a new todo on the CalDAV server."""
    try:
        todo = Todo(
            title=title,
            due_date=due_date
        )
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
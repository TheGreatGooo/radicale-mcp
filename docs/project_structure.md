# Project Structure

## Directory Layout

```
caldav-mcp/
├── main.py                 # Main application entry point
├── requirements.txt        # Python dependencies
├── config/                 # Configuration files
│   └── settings.json      # Application settings
├── src/                    # Source code
│   ├── __init__.py
│   ├── caldav_client.py    # CalDAV connection and operations
│   ├── models/             # Data models
│   │   ├── __init__.py
│   │   ├── event.py        # Event data model
│   │   ├── journal.py      # Journal data model
│   │   └── todo.py         # Todo data model
│   ├── operations/         # CRUD operations
│   │   ├── __init__.py
│   │   ├── event_ops.py    # Event CRUD operations
│   │   ├── journal_ops.py  # Journal CRUD operations
│   │   └── todo_ops.py     # Todo CRUD operations
│   ├── stdio_interface.py  # MCP STDIO protocol implementation
│   ├── config_manager.py   # Configuration management
│   └── error_handler.py    # Error handling and logging
├── tests/                  # Test files
│   ├── __init__.py
│   ├── test_caldav_client.py
│   ├── test_models.py
│   └── test_operations.py
└── docs/                   # Documentation
    ├── architecture.md
    └── project_structure.md
```

## File Descriptions

### Main Application (`main.py`)
- Entry point of the application
- Initializes components
- Starts the STDIO interface loop

### CalDAV Client (`src/caldav_client.py`)
- Handles connection to CalDAV server
- Authentication management
- Basic CRUD operations through the caldav library

### Data Models (`src/models/`)
- **Event Model** (`event.py`): Represents calendar events with title, description, start/end times, location, etc.
- **Journal Model** (`journal.py`): Represents journal entries with date, content, tags, etc.
- **Todo Model** (`todo.py`): Represents todo items with title, description, due date, completion status, priority, etc.

### Operations (`src/operations/`)
- **Event Operations** (`event_ops.py`): Full CRUD operations for events
- **Journal Operations** (`journal_ops.py`): Full CRUD operations for journals
- **Todo Operations** (`todo_ops.py`): Full CRUD operations for todos

### STDIO Interface (`src/stdio_interface.py`)
- Implements MCP protocol for STDIO communication
- Handles message parsing and response formatting
- Routes commands to appropriate operations

### Configuration Manager (`src/config_manager.py`)
- Loads and manages application configuration
- Handles credentials and server settings

### Error Handler (`src/error_handler.py`)
- Centralized error handling
- Logging functionality
- Error response formatting for MCP protocol

## Dependencies

The application requires:
- `caldav>=0.10.0`: For CalDAV protocol implementation
- `python-dateutil>=2.8.0`: For date/time parsing and manipulation
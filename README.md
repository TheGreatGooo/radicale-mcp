# MCP CalDAV STDIO Application

A Python-based MCP (Model Communication Protocol) application that provides CRUD operations for events, journals, and todos using the caldav Python library.

## Prerequisites

- Python 3.8 or higher
- `uv` (optional, for fast installation) or `pip`

## Dependencies

The required Python packages are listed in `pyproject.toml` and will be installed automatically:

- `caldav`
- `python-dateutil`
- `fastmcp`

## Installation Options

You can install the application using `uv` (recommended) or `pip`.

### Using uv (recommended)
```bash
uv pip install radicale-mcp
```

### Using pip
```bash
pip install radicale-mcp
```

### From source
```bash
git clone https://github.com/TheGreatGooo/radicale-mcp.git
cd radicale-mcp
uv pip install -e .
```

### Using uvx (run directly from GitHub)
```bash
uvx radicale-mcp@https://github.com/TheGreatGooo/radicale-mcp
```

## Features

- **MCP Protocol Support**: Communicates over STDIO using the Model Communication Protocol
- **CalDAV Integration**: Connects to any CalDAV server (like Radicale)
- **Full CRUD Operations**: Create, Read, Update, and Delete for events, journals, and todos
- **Standard Data Models**: Well-defined models for events, journals, and todos
- **Error Handling**: Comprehensive error handling and logging
- **Configuration Management**: Flexible configuration via files and environment variables

## Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌──────────────────┐
│   MCP Client    │    │  MCP CalDAV      │    │   CalDAV Server  │
│                 │    │  Application     │    │                  │
│  STDIO Input    │───▶│  (this app)      │───▶│  (e.g. Radicale) │
│  JSON Messages  │    │                  │    │                  │
│                 │◀───│                  │◀───│                  │
│  STDIO Output   │    │                  │    │                  │
└─────────────────┘    └──────────────────┘    └──────────────────┘
```

## Configuration

The application supports configuration through:
- Environment variables
- Configuration file (`config/settings.json`)

### Environment Variables
- `CALDAV_SERVER_URL`: CalDAV server URL (default: `http://localhost:5232`)
- `CALDAV_USERNAME`: Username for authentication (default: `user`)
- `CALDAV_PASSWORD`: Password for authentication (default: ``)
- `CALDAV_USE_SSL`: Whether to use SSL (default: `true`)
- `LOG_LEVEL`: Logging level (default: `INFO`)

### Configuration File
Create `config/settings.json`:
```json
{
  "server_url": "http://localhost:5232",
  "username": "user",
  "password": "",
  "use_ssl": true,
  "log_level": "INFO"
}
```

## Usage

The application runs as an MCP server by default. To start it:

```bash
python -m src.server
```

Or simply:

```bash
radicale_mcp
```

The application will listen on STDIO for MCP protocol messages. It supports the following methods:

### Event Operations
- `caldav.event.create`: Create a new event
- `caldav.event.read`: Read an existing event
- `caldav.event.update`: Update an existing event
- `caldav.event.delete`: Delete an event
- `caldav.event.list`: List all events

### Journal Operations
- `caldav.journal.create`: Create a new journal entry
- `caldav.journal.read`: Read an existing journal entry
- `caldav.journal.update`: Update an existing journal entry
- `caldav.journal.delete`: Delete a journal entry
- `caldav.journal.list`: List all journal entries

### Todo Operations
- `caldav.todo.create`: Create a new todo item
- `caldav.todo.read`: Read an existing todo item
- `caldav.todo.update`: Update an existing todo item
- `caldav.todo.delete`: Delete a todo item
- `caldav.todo.list`: List all todo items

## Example Request

```json
{
  "jsonrpc": "2.0",
  "id": "1",
  "method": "caldav.event.create",
  "params": {
    "title": "Team Meeting",
    "description": "Weekly team sync",
    "start_time": "2023-10-15T10:00:00",
    "end_time": "2023-10-15T11:00:00",
    "location": "Conference Room A"
  }
}
```

## Example Response

```json
{
  "jsonrpc": "2.0",
  "id": "1",
  "result": {
    "id": "event-12345",
    "status": "created"
  }
}
```

## Development

### Project Structure
```
radicale-mcp/
├── src/main.py                 # Main application entry point
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
└── docs/                   # Documentation
    ├── architecture.md
    ├── project_structure.md
    ├── data_models.md
    └── mcp_protocol.md
```

## FastMCP Integration

This application demonstrates how to integrate with the FastMCP library. The `src/server.py` file shows:

- How to create an MCP server instance
- How to define tools that can be called by MCP clients
- Integration with existing CalDAV functionality

To run the FastMCP server:
```bash
python -m server
```

## License

MIT
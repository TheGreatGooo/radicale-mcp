# MCP CalDAV STDIO Application

A Python-based MCP (Model Communication Protocol) application that provides CRUD operations for events, journals, and todos using the caldav Python library.

## Dependencies

This application requires the following Python packages:
- `caldav` - For CalDAV protocol support
- `python-dateutil` - For date/time parsing and manipulation

These dependencies are automatically managed through the package configuration.

## Installation with uv

This application can be installed and run using `uv` or `uvx`:

### Using uvx (no installation needed)
```bash
uvx caldav-mcp
```

### Using uv to install
```bash
uv pip install caldav-mcp
uvx caldav-mcp
```

### From source
```bash
git clone https://github.com/example/caldav-mcp.git
cd caldav-mcp
uv pip install -e .
uvx caldav-mcp
```

### Direct usage with uvx from GitHub
```bash
uvx github:example/caldav-mcp
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

## Installation

1. Clone or download this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
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

Run the application:
```bash
python main.py
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
└── docs/                   # Documentation
    ├── architecture.md
    ├── project_structure.md
    ├── data_models.md
    └── mcp_protocol.md
```

## License

MIT
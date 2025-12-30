# Data Models for MCP CalDAV Application

## Overview
This document describes the data models for events, journals, and todos that will be used in the MCP CalDAV application. These models will be used to represent calendar data in a standardized format that can be stored and retrieved from CalDAV servers.

## Event Model

### Properties
- `id`: Unique identifier for the event
- `title`: Title/subject of the event
- `description`: Detailed description of the event
- `start_time`: Start datetime of the event
- `end_time`: End datetime of the event
- `location`: Location of the event
- `attendees`: List of attendees (email addresses)
- `categories`: List of categories/tags
- `status`: Event status (confirmed, tentative, cancelled)
- `priority`: Priority level (1-9)
- `url`: URL associated with the event

### Operations
- Create: Initialize a new event with all required properties
- Read: Retrieve event properties
- Update: Modify existing event properties
- Delete: Remove the event from storage

## Journal Model

### Properties
- `id`: Unique identifier for the journal entry
- `date`: Date of the journal entry
- `title`: Title of the journal entry
- `content`: Main content of the journal entry
- `tags`: List of tags/categories
- `categories`: List of categories
- `priority`: Priority level (1-9)
- `url`: URL associated with the journal entry

### Operations
- Create: Initialize a new journal entry with all required properties
- Read: Retrieve journal entry properties
- Update: Modify existing journal entry properties
- Delete: Remove the journal entry from storage

## Todo Model

### Properties
- `id`: Unique identifier for the todo item
- `title`: Title/subject of the todo
- `description`: Detailed description of the todo
- `due_date`: Due date for the todo
- `completion_date`: Date when the todo was completed
- `status`: Completion status (pending, completed, cancelled)
- `priority`: Priority level (1-9)
- `categories`: List of categories/tags
- `url`: URL associated with the todo
- `percent_complete`: Percentage of completion (0-100)

### Operations
- Create: Initialize a new todo with all required properties
- Read: Retrieve todo properties
- Update: Modify existing todo properties
- Delete: Remove the todo from storage

## Model Implementation Considerations

### Data Mapping
Each model will need to map to the appropriate CalDAV components:
- **Events**: iCalendar VEVENT components
- **Journals**: iCalendar VJOURNAL components  
- **Todos**: iCalendar VTODO components

### Serialization/Deserialization
- Models should be able to serialize to and from iCalendar format
- Support for different date/time formats and timezones
- Proper handling of recurring events/journals/todos

### Validation
- Each model should include validation for required fields
- Date/time validation for temporal properties
- Range validation for priority levels (1-9)
- Format validation for URLs and email addresses

### Error Handling
- Graceful handling of missing or malformed data
- Clear error messages for invalid operations
- Consistent error reporting across all models
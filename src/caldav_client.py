"""
CalDAV Client for MCP CalDAV Application
Handles connection and communication with CalDAV server.
"""

import logging
from typing import Dict, Any, Optional
from datetime import datetime

# Import caldav library (dependency is declared in pyproject.toml)
import caldav

logger = logging.getLogger(__name__)

class CalDAVClient:
    """Client for connecting to and interacting with a CalDAV server."""
    
    def __init__(self, config_manager):
        """
        Initialize the CalDAV client.
        
        Args:
            config_manager: Configuration manager instance
        """
        self.config_manager = config_manager
        self.client = None
        self.connected = False
    
    def connect(self) -> bool:
        """
        Establish connection to the CalDAV server.
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            server_url = self.config_manager.get('server_url')
            username = self.config_manager.get('username')
            password = self.config_manager.get('password')
            use_ssl = self.config_manager.get('use_ssl', True)
            
            # Create connection
            if use_ssl:
                self.client = caldav.DAVClient(
                    server_url,
                    username=username,
                    password=password,
                    ssl_verify_cert=True
                )
            else:
                self.client = caldav.DAVClient(
                    server_url,
                    username=username,
                    password=password,
                    ssl_verify_cert=False
                )
            
            self.connected = True
            logger.info("Successfully connected to CalDAV server")
            return True
            
        except Exception as e:
            logger.error(f"Failed to connect to CalDAV server: {e}")
            self.connected = False
            return False
    
    def disconnect(self) -> None:
       """Close the connection to the CalDAV server."""
       if self.client:
           # In a real implementation, we would close the connection
           self.client = None
       self.connected = False
       logger.info("Disconnected from CalDAV server")
    
    def is_connected(self) -> bool:
        """
        Check if client is connected.
        
        Returns:
            True if connected, False otherwise
        """
        return self.connected
    
    def create_event(self, event_data: Dict[str, Any]) -> Optional[str]:
       """
       Create a new event in the CalDAV server.
       
       Args:
           event_data: Dictionary containing event data
           
       Returns:
           ID of created event or None if failed
       """
       if not self.connected:
           logger.error("Not connected to CalDAV server")
           return None
           
       try:
           # Get the principal and calendar
           principal = self.client.principal()
           calendar = principal.calendars()[0]  # Use first calendar
           
           # Create VEVENT
           vevent = caldav.vcal.VEVENT()
           vevent.add('summary', event_data.get('title', 'Untitled Event'))
           vevent.add('description', event_data.get('description', ''))
           vevent.add('dtstart', event_data.get('start_time'))
           vevent.add('dtend', event_data.get('end_time'))
           
           # Add other properties if available
           if 'location' in event_data:
               vevent.add('location', event_data['location'])
           if 'attendees' in event_data:
               vevent.add('attendee', event_data['attendees'])
           if 'status' in event_data:
               vevent.add('status', event_data['status'])
           
           # Create the event in the calendar
           new_event = calendar.save(vevent)
           
           # Return the event ID
           logger.info(f"Created event: {event_data.get('title', 'Unknown')}")
           return new_event.id
       except Exception as e:
           logger.error(f"Failed to create event: {e}")
           return None
    
    def read_event(self, event_id: str) -> Optional[Dict[str, Any]]:
       """
       Read an event from the CalDAV server.
       
       Args:
           event_id: ID of the event to read
           
       Returns:
           Dictionary containing event data or None if not found
       """
       if not self.connected:
           logger.error("Not connected to CalDAV server")
           return None
           
       try:
           # Get the principal and calendar
           principal = self.client.principal()
           calendar = principal.calendars()[0]  # Use first calendar
           
           # Retrieve the event by ID
           event = calendar.event(event_id)
           
           # Convert to dictionary format
           event_data = {
               "id": event_id,
               "title": event.vevent.get('summary', ''),
               "description": event.vevent.get('description', ''),
               "start_time": event.vevent.get('dtstart', ''),
               "end_time": event.vevent.get('dtend', ''),
               "location": event.vevent.get('location', ''),
               "status": event.vevent.get('status', '')
           }
           
           logger.info(f"Read event: {event_id}")
           return event_data
       except Exception as e:
           logger.error(f"Failed to read event: {e}")
           return None
    
    def update_event(self, event_id: str, event_data: Dict[str, Any]) -> bool:
       """
       Update an existing event in the CalDAV server.
       
       Args:
           event_id: ID of the event to update
           event_data: Dictionary containing updated event data
           
       Returns:
           True if successful, False otherwise
       """
       if not self.connected:
           logger.error("Not connected to CalDAV server")
           return False
           
       try:
           # Get the principal and calendar
           principal = self.client.principal()
           calendar = principal.calendars()[0]  # Use first calendar
           
           # Retrieve the event by ID
           event = calendar.event(event_id)
           
           # Update the event properties
           if 'title' in event_data:
               event.vevent.set('summary', event_data['title'])
           if 'description' in event_data:
               event.vevent.set('description', event_data['description'])
           if 'start_time' in event_data:
               event.vevent.set('dtstart', event_data['start_time'])
           if 'end_time' in event_data:
               event.vevent.set('dtend', event_data['end_time'])
           if 'location' in event_data:
               event.vevent.set('location', event_data['location'])
           if 'status' in event_data:
               event.vevent.set('status', event_data['status'])
           
           # Save the updated event
           event.save()
           
           logger.info(f"Updated event: {event_id}")
           return True
       except Exception as e:
           logger.error(f"Failed to update event: {e}")
           return False
    
    def delete_event(self, event_id: str) -> bool:
       """
       Delete an event from the CalDAV server.
       
       Args:
           event_id: ID of the event to delete
           
       Returns:
           True if successful, False otherwise
       """
       if not self.connected:
           logger.error("Not connected to CalDAV server")
           return False
           
       try:
           # Get the principal and calendar
           principal = self.client.principal()
           calendar = principal.calendars()[0]  # Use first calendar
           
           # Retrieve the event by ID
           event = calendar.event(event_id)
           
           # Delete the event
           event.delete()
           
           logger.info(f"Deleted event: {event_id}")
           return True
       except Exception as e:
           logger.error(f"Failed to delete event: {e}")
           return False
    
    def create_journal(self, journal_data: Dict[str, Any]) -> Optional[str]:
       """
       Create a new journal entry in the CalDAV server.
       
       Args:
           journal_data: Dictionary containing journal data
           
       Returns:
           ID of created journal or None if failed
       """
       if not self.connected:
           logger.error("Not connected to CalDAV server")
           return None
           
       try:
           # Get the principal and calendar
           principal = self.client.principal()
           calendar = principal.calendars()[0]  # Use first calendar
           
           # Create VJOURNAL
           vjournal = caldav.vcal.VJOURNAL()
           vjournal.add('summary', journal_data.get('title', 'Untitled Journal'))
           vjournal.add('description', journal_data.get('description', ''))
           vjournal.add('dtstart', journal_data.get('date'))
           
           # Add other properties if available
           if 'status' in journal_data:
               vjournal.add('status', journal_data['status'])
           
           # Create the journal entry in the calendar
           new_journal = calendar.save(vjournal)
           
           # Return the journal ID
           logger.info(f"Created journal: {journal_data.get('title', 'Unknown')}")
           return new_journal.id
       except Exception as e:
           logger.error(f"Failed to create journal: {e}")
           return None
    
    def read_journal(self, journal_id: str) -> Optional[Dict[str, Any]]:
       """
       Read a journal entry from the CalDAV server.
       
       Args:
           journal_id: ID of the journal entry to read
           
       Returns:
           Dictionary containing journal data or None if not found
       """
       if not self.connected:
           logger.error("Not connected to CalDAV server")
           return None
           
       try:
           # Get the principal and calendar
           principal = self.client.principal()
           calendar = principal.calendars()[0]  # Use first calendar
           
           # Retrieve the journal by ID
           journal = calendar.journal(journal_id)
           
           # Convert to dictionary format
           journal_data = {
               "id": journal_id,
               "title": journal.vjournal.get('summary', ''),
               "description": journal.vjournal.get('description', ''),
               "date": journal.vjournal.get('dtstart', ''),
               "status": journal.vjournal.get('status', '')
           }
           
           logger.info(f"Read journal: {journal_id}")
           return journal_data
       except Exception as e:
           logger.error(f"Failed to read journal: {e}")
           return None
    
    def update_journal(self, journal_id: str, journal_data: Dict[str, Any]) -> bool:
       """
       Update an existing journal entry in the CalDAV server.
       
       Args:
           journal_id: ID of the journal entry to update
           journal_data: Dictionary containing updated journal data
           
       Returns:
           True if successful, False otherwise
       """
       if not self.connected:
           logger.error("Not connected to CalDAV server")
           return False
           
       try:
           # Get the principal and calendar
           principal = self.client.principal()
           calendar = principal.calendars()[0]  # Use first calendar
           
           # Retrieve the journal by ID
           journal = calendar.journal(journal_id)
           
           # Update the journal properties
           if 'title' in journal_data:
               journal.vjournal.set('summary', journal_data['title'])
           if 'description' in journal_data:
               journal.vjournal.set('description', journal_data['description'])
           if 'date' in journal_data:
               journal.vjournal.set('dtstart', journal_data['date'])
           if 'status' in journal_data:
               journal.vjournal.set('status', journal_data['status'])
           
           # Save the updated journal
           journal.save()
           
           logger.info(f"Updated journal: {journal_id}")
           return True
       except Exception as e:
           logger.error(f"Failed to update journal: {e}")
           return False
    
    def delete_journal(self, journal_id: str) -> bool:
       """
       Delete a journal entry from the CalDAV server.
       
       Args:
           journal_id: ID of the journal entry to delete
           
       Returns:
           True if successful, False otherwise
       """
       if not self.connected:
           logger.error("Not connected to CalDAV server")
           return False
           
       try:
           # Get the principal and calendar
           principal = self.client.principal()
           calendar = principal.calendars()[0]  # Use first calendar
           
           # Retrieve the journal by ID
           journal = calendar.journal(journal_id)
           
           # Delete the journal
           journal.delete()
           
           logger.info(f"Deleted journal: {journal_id}")
           return True
       except Exception as e:
           logger.error(f"Failed to delete journal: {e}")
           return False
    
    def create_todo(self, todo_data: Dict[str, Any]) -> Optional[str]:
       """
       Create a new todo item in the CalDAV server.
       
       Args:
           todo_data: Dictionary containing todo data
           
       Returns:
           ID of created todo or None if failed
       """
       if not self.connected:
           logger.error("Not connected to CalDAV server")
           return None
           
       try:
           # Get the principal and calendar
           principal = self.client.principal()
           calendar = principal.calendars()[0]  # Use first calendar
           
           # Create VTODO
           vtodo = caldav.vcal.VTODO()
           vtodo.add('summary', todo_data.get('title', 'Untitled Todo'))
           vtodo.add('description', todo_data.get('description', ''))
           vtodo.add('priority', todo_data.get('priority', 5))
           
           # Add other properties if available
           if 'status' in todo_data:
               vtodo.add('status', todo_data['status'])
           if 'due_date' in todo_data:
               vtodo.add('due', todo_data['due_date'])
           if 'completed_date' in todo_data:
               vtodo.add('completed', todo_data['completed_date'])
           
           # Create the todo in the calendar
           new_todo = calendar.save(vtodo)
           
           # Return the todo ID
           logger.info(f"Created todo: {todo_data.get('title', 'Unknown')}")
           return new_todo.id
       except Exception as e:
           logger.error(f"Failed to create todo: {e}")
           return None
    
    def read_todo(self, todo_id: str) -> Optional[Dict[str, Any]]:
       """
       Read a todo item from the CalDAV server.
       
       Args:
           todo_id: ID of the todo item to read
           
       Returns:
           Dictionary containing todo data or None if not found
       """
       if not self.connected:
           logger.error("Not connected to CalDAV server")
           return None
           
       try:
           # Get the principal and calendar
           principal = self.client.principal()
           calendar = principal.calendars()[0]  # Use first calendar
           
           # Retrieve the todo by ID
           todo = calendar.todo(todo_id)
           
           # Convert to dictionary format
           todo_data = {
               "id": todo_id,
               "title": todo.vtodo.get('summary', ''),
               "description": todo.vtodo.get('description', ''),
               "priority": todo.vtodo.get('priority', 5),
               "status": todo.vtodo.get('status', ''),
               "due_date": todo.vtodo.get('due', ''),
               "completed_date": todo.vtodo.get('completed', '')
           }
           
           logger.info(f"Read todo: {todo_id}")
           return todo_data
       except Exception as e:
           logger.error(f"Failed to read todo: {e}")
           return None
    
    def update_todo(self, todo_id: str, todo_data: Dict[str, Any]) -> bool:
       """
       Update an existing todo item in the CalDAV server.
       
       Args:
           todo_id: ID of the todo item to update
           todo_data: Dictionary containing updated todo data
           
       Returns:
           True if successful, False otherwise
       """
       if not self.connected:
           logger.error("Not connected to CalDAV server")
           return False
           
       try:
           # Get the principal and calendar
           principal = self.client.principal()
           calendar = principal.calendars()[0]  # Use first calendar
           
           # Retrieve the todo by ID
           todo = calendar.todo(todo_id)
           
           # Update the todo properties
           if 'title' in todo_data:
               todo.vtodo.set('summary', todo_data['title'])
           if 'description' in todo_data:
               todo.vtodo.set('description', todo_data['description'])
           if 'priority' in todo_data:
               todo.vtodo.set('priority', todo_data['priority'])
           if 'status' in todo_data:
               todo.vtodo.set('status', todo_data['status'])
           if 'due_date' in todo_data:
               todo.vtodo.set('due', todo_data['due_date'])
           if 'completed_date' in todo_data:
               todo.vtodo.set('completed', todo_data['completed_date'])
           
           # Save the updated todo
           todo.save()
           
           logger.info(f"Updated todo: {todo_id}")
           return True
       except Exception as e:
           logger.error(f"Failed to update todo: {e}")
           return False
    
    def delete_todo(self, todo_id: str) -> bool:
       """
       Delete a todo item from the CalDAV server.
       
       Args:
           todo_id: ID of the todo item to delete
           
       Returns:
           True if successful, False otherwise
       """
       if not self.connected:
           logger.error("Not connected to CalDAV server")
           return False
           
       try:
           # Get the principal and calendar
           principal = self.client.principal()
           calendar = principal.calendars()[0]  # Use first calendar
           
           # Retrieve the todo by ID
           todo = calendar.todo(todo_id)
           
           # Delete the todo
           todo.delete()
           
           logger.info(f"Deleted todo: {todo_id}")
           return True
       except Exception as e:
           logger.error(f"Failed to delete todo: {e}")
           return False

"""
Journal Model for MCP CalDAV Application
Represents journal entries with all relevant properties.
"""

from typing import Dict, Any, List
from datetime import datetime
from models.base_model import BaseModel


class Journal(BaseModel):
    """Model representing a journal entry."""

    def __init__(
        self,
        date: datetime = None,
        title: str = "",
        content: str = "",
        tags: List[str] = None,
        categories: List[str] = None,
        priority: int = 5,
        url: str = "",
        **kwargs,
    ):
        """
        Initialize a Journal model.

        Args:
            date: Date of the journal entry
            title: Journal entry title
            content: Journal entry content
            tags: List of tags
            categories: List of categories
            priority: Priority level (1-9)
            url: URL associated with the journal entry
            **kwargs: Additional properties
        """
        super().__init__(**kwargs)

        self.date = date
        self.title = title
        self.content = content
        self.tags = tags or []
        self.categories = categories or []
        self.priority = priority
        self.url = url

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert journal to dictionary representation.

        Returns:
            Dictionary representation of the journal entry
        """
        return {
            "id": self.id,
            "date": self.date.isoformat() if self.date else None,
            "title": self.title,
            "content": self.content,
            "tags": self.tags,
            "categories": self.categories,
            "priority": self.priority,
            "url": self.url,
        }

    def from_dict(self, data: Dict[str, Any]) -> None:
        """
        Initialize journal from dictionary data.

        Args:
            data: Dictionary containing journal data
        """
        self.id = data.get("id", self.id)
        self.title = data.get("title", "")
        self.content = data.get("content", "")
        self.tags = data.get("tags", [])
        self.categories = data.get("categories", [])
        self.priority = data.get("priority", 5)
        self.url = data.get("url", "")

        # Handle datetime conversion
        date_str = data.get("date")
        if date_str:
            self.date = datetime.fromisoformat(date_str)
        else:
            self.date = None

    def to_ical(self) -> str:
        """
        Convert journal to iCalendar format.

        Returns:
            iCalendar string representation
        """
        # This is a simplified implementation
        # In a real implementation, this would use the caldav library properly
        ical = "BEGIN:VJOURNAL\n"
        ical += f"UID:{self.id}\n"
        ical += f"SUMMARY:{self.title}\n"
        ical += f"DESCRIPTION:{self.content}\n"
        if self.date:
            ical += f"DTSTAMP:{self.date.strftime('%Y%m%dT%H%M%S')}\n"
        ical += f"PRIORITY:{self.priority}\n"
        if self.url:
            ical += f"URL:{self.url}\n"
        ical += "END:VJOURNAL\n"
        return ical

    def from_ical(self, ical_str: str) -> None:
        """
        Initialize journal from iCalendar string.

        Args:
            ical_str: iCalendar string representation
        """
        # This is a simplified implementation
        # In a real implementation, this would parse the iCalendar properly
        pass

    def validate(self) -> bool:
        """
        Validate the journal data.

        Returns:
            True if valid, False otherwise
        """
        if not self.title:
            return False
        if self.priority < 1 or self.priority > 9:
            return False
        return True

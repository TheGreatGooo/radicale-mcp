"""
Base Model for MCP CalDAV Application
Provides common functionality for all data models.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any
import uuid


class BaseModel(ABC):
    """Abstract base class for all data models."""

    def __init__(self, **kwargs):
        """
        Initialize a model instance.

        Args:
            **kwargs: Model properties
        """
        # Generate unique ID if not provided
        if "id" not in kwargs or not kwargs["id"]:
            self.id = str(uuid.uuid4())
        else:
            self.id = kwargs["id"]

        # Set other properties
        for key, value in kwargs.items():
            if key != "id":
                setattr(self, key, value)

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert model to dictionary representation.

        Returns:
            Dictionary representation of the model
        """
        pass

    @abstractmethod
    def from_dict(self, data: Dict[str, Any]) -> None:
        """
        Initialize model from dictionary data.

        Args:
            data: Dictionary containing model data
        """
        pass

    @abstractmethod
    def to_ical(self) -> str:
        """
        Convert model to iCalendar format.

        Returns:
            iCalendar string representation
        """
        pass

    @abstractmethod
    def from_ical(self, ical_str: str) -> None:
        """
        Initialize model from iCalendar string.

        Args:
            ical_str: iCalendar string representation
        """
        pass

    def validate(self) -> bool:
        """
        Validate the model data.

        Returns:
            True if valid, False otherwise
        """
        # Default validation - can be overridden by subclasses
        return True

    def get_property(self, name: str, default: Any = None) -> Any:
        """
        Get a property value safely.

        Args:
            name: Property name
            default: Default value if property doesn't exist

        Returns:
            Property value or default
        """
        return getattr(self, name, default)

    def set_property(self, name: str, value: Any) -> None:
        """
        Set a property value.

        Args:
            name: Property name
            value: Property value
        """
        setattr(self, name, value)

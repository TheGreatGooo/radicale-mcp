#!/usr/bin/env python3
"""
MCP CalDAV STDIO Application
A Python-based MCP (Model Communication Protocol) application for CalDAV operations
that supports CRUD operations on events, journals, and todos.
"""

import sys
import logging
from stdio_interface import StdioInterface
from config_manager import ConfigManager

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def main():
    """Main entry point for the MCP CalDAV application."""
    logger.info("Starting MCP CalDAV application")

    try:
        # Initialize configuration manager
        config_manager = ConfigManager()

        # Initialize STDIO interface
        stdio_interface = StdioInterface(config_manager)

        # Start the STDIO loop
        stdio_interface.start()

    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Application error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()

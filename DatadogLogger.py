import logging
import os

from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v2.api.logs_api import LogsApi
from datadog_api_client.v2.model.http_log import HTTPLog
from datadog_api_client.v2.model.http_log_item import HTTPLogItem


class DatadogLogger:
    def __init__(self, service_name, ddsource='python', ddtags=None, hostname=None):
        """Initialize the Datadog logger."""
        # Configure Datadog client
        self.configuration = Configuration()
        self.service_name = service_name
        self.ddsource = ddsource
        self.ddtags = ddtags or ''
        self.hostname = hostname or os.uname()[1]  # Use the hostname of the machine

        # Set up the logger
        self.logger = logging.getLogger(service_name)
        self.logger.setLevel(logging.INFO)

        # Console handler
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        stream_formatter = logging.Formatter(
            '%(asctime)s — %(name)s — %(levelname)s — %(message)s'
        )
        stream_handler.setFormatter(stream_formatter)

        # Add stream handler to logger
        self.logger.addHandler(stream_handler)

        # Initialize Datadog API client
        self.api_client = ApiClient(self.configuration)
        self.logs_api = LogsApi(self.api_client)

    def log(self, message, status='info'):
        """Log a message to both console and Datadog."""
        # Create a log item
        log_item = HTTPLogItem(
            ddsource=self.ddsource,
            ddtags=self.ddtags,
            hostname=self.hostname,
            message=message,
            service=self.service_name,
            status=status
        )

        # Create the body for the log submission
        body = HTTPLog([log_item])

        # Send log to Datadog
        try:
            response = self.logs_api.submit_log(body=body)
        except Exception as e:
            self.logger.error(f"Failed to send log to Datadog: {str(e)}")

    def info(self, message):
        """Log an info message to both console and Datadog."""
        self.logger.info(message)
        self.log(message, status='info')

    def error(self, message):
        """Log an error message to both console and Datadog."""
        self.logger.error(message)
        self.log(message, status='error')

    def close(self):
        """Close the Datadog API client connection."""
        self.api_client.close()
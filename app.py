from DatadogLogger import DatadogLogger


def write_logs():
    """Test function to write logs to stdout and Datadog"""
    logger.info("This is a test message with INFO severity level")
    logger.error("This is a test message with ERROR severity level")


if __name__ == "__main__":

    # Set up Logger
    logger = DatadogLogger(service_name='test-app',
                           ddtags='env:poc,team:CloudOps')

    # Write test logs
    write_logs()

    # Close custom logger (DataDog client)
    logger.close()

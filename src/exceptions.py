class ConfigurationError(Exception):
    """Exception raised for errors in the configuration."""
    def __init__(self, message="Configuration Error occurred"):
        super().__init__(message)


class DatabaseConnectionError(Exception):
    """Exception raised for errors related to database connections."""
    def __init__(self, message="Database connection error"):
        super().__init__(message)

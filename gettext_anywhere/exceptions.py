class UnregisteredHandlerException(Exception):
    """
    Raised when the registry is unable to find a handler for a provided
    translations domain.
    """

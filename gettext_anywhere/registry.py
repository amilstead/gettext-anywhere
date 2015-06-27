from . import exceptions as ga_exc
from .handlers import core as core_handlers


_REGISTRY = {}


def clear():
    """Clears the registry."""
    _REGISTRY.clear()


def register_domain_handler(domain, handler, options=None):
    """
    Register a file handler for a given translations domain.

    :param domain: the translations domain.
    :param handler: a class inheriting from FileHandler.
    :param options: optional options dict for handler instantiation.
    """
    options = options or {}
    if not issubclass(handler, core_handlers.FileHandler):
        err = "File handlers must inherit " \
              "from: %s" % type(core_handlers.FileHandler)
        raise Exception(err)
    _handler = {
        "handler": handler,
        "options": options
    }
    _REGISTRY[domain] = _handler


def register_default_handler(handler, options=None):
    """
    Registers a handler for the default "messages" domain.

    :param handler: a class inheriting from FileHandler.
    :param options: optional options dict for handler instantiation.
    """
    register_domain_handler("messages", handler, options=options)


def get_domain_handler(domain):
    """
    Retrieve a handler for the provided domain.

    :param domain: the translations domain.
    :return: an instantiated file handler.
    """
    _handler = _REGISTRY.get(domain)
    if _handler is None:
        err = "Handler for domain: %s does not exist." % domain
        raise ga_exc.UnregisteredHandlerException(err)

    return _handler["handler"](domain, _handler["options"])

import contextlib
import copy
import gettext
import logging
import os

from . import registry
from .handlers import file as file_handlers


_patched = False
_original_gettext = {}
logger = logging.getLogger(__name__)


@contextlib.contextmanager
def open_file(domain, filename):
    """
    Context manager for opening files, similar to the built-in `open`.

    This function retrieves a file handler from the registry, opens it, yields
    the file handler, then closes the file handler when execution returns.

    :param domain: the translations domain.
    :param filename: the filename to open.
    """
    handler = None
    try:
        handler = registry.get_domain_handler(domain)
        handler.open(filename)
        yield handler
        handler.close()
    except Exception:
        logger.error(
            "%s for domain %s failed to open file: %s" % (
                type(handler),
                domain,
                filename
            )
        )
        raise


def _translation(domain, localedir=None, languages=None, class_=None,
                 fallback=False, codeset=None):
    """
    Patched version of gettext.translation.

    The major differences here are what is used to find and open files.

    Rather than using the built-in file opener (`open`), we retrieve a custom
    file handler from the registry and use it instead.

    :param domain: the translations domain.
    :param localedir: an optional locale directory path.
    :param languages: a list of languages to load.
    :param class_: the class used for Translations objects (see NullTranslations
        and GNUTranslations from the gettext module).
    :param fallback: the fallback for the translations object.
    :param codeset: a custom output charset for the translations file.
    :return: a gettext translations object.
    """
    if class_ is None:
        class_ = gettext.GNUTranslations

    handler = registry.get_domain_handler(domain)
    mofiles = handler.find(localedir, languages, all=1)

    if not mofiles:
        if fallback:
            return gettext.NullTranslations()
        raise IOError(
            gettext.ENOENT,
            'No translation file found for domain',
            domain
        )
    # Avoid opening, reading, and parsing the .mo file after it's been done
    # once.
    result = None
    for mofile in mofiles:
        key = (class_, os.path.abspath(mofile))
        t = gettext._translations.get(key)
        if t is None:
            with open_file(domain, mofile) as fp:
                t = gettext._translations.setdefault(
                    key,
                    class_(fp)
                )
        # Copy the translation object to allow setting fallbacks and
        # output charset. All other instance data is shared with the
        # cached object.
        t = copy.copy(t)
        if codeset:
            t.set_output_charset(codeset)
        if result is None:
            result = t
        else:
            result.add_fallback(t)
    return result


def patch():
    global _patched
    if not _patched:
        _patched = True
        _original_gettext.update({
            "translation": gettext.translation,
        })
        gettext.translation = _translation
        registry.register_domain_handler(
            "messages",
            file_handlers.RegularFileHandler
        )

def unpatch():
    global _patched
    for key, val in _original_gettext.iteritems():
        setattr(gettext, key, val)
    registry.clear()
    _patched = False

import gettext

from . import core


class RegularFileHandler(core.FileHandler):
    """
    Mimics the default gettext functionality.

    This handler's `open` function simply opens a file pointer.

    This handler's `close` function closes the file pointer.

    This handler's `read` function is a pass-through to file pointer's `read`.

    This handler's `find` function is a pass-through to gettext's `find`.
    """
    def __init__(self, *args, **kwargs):
        super(RegularFileHandler, self).__init__(*args, **kwargs)
        self._fp = None

    def find(self, localedir=None, languages=None, all=0):
        return gettext.find(self._domain, localedir, languages, all)

    def open(self, filename):
        self._fp = open(filename, 'rb')

    def read(self):
        return self._fp.read()

    def close(self):
        if self._fp is not None:
            self._fp.close()
        self._fp = None

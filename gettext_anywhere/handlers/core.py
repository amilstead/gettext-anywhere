class FileHandler(object):
    """
    A quasi File-like object super-class template.

    Any custom domain readers must inherit this class.

    NOTE: This is not exactly file-like, as it requires the implementation of
    an `open` function, where as true file objects perform `open` functions
    on instantiation.
    """

    def __init__(self, domain, options):
        """
        Initialize this class, setting the translations domain for the instance
        as well as a dictionary of custom options that may be required for some
        implementation details.

        :param domain: the translations domain.
        :param options: a dict of custom options for the instance.
        """
        self._domain = domain
        self._options = options

    def open(self, filename):
        """
        Required for opening a file.

        :param filename: the filename to use for opening.
        """
        raise NotImplementedError("Sub-class must implement this method.")

    def find(self, localedir=None, languages=None, all=0):
        """
        Finds translations file candidates that this handler can read.

        :param localedir: an optional localedir where translations are found.
        :param languages: which languages to search for.
        :param all: whether or not to read all found files, or just the first.
        :return: a list of file paths or a single file path.
        """
        raise NotImplementedError("Sub-class must implement this method.")

    def read(self):
        """
        Required for reading the file.

        :return: the contents of the file this handler represents.
        """
        raise NotImplementedError("Sub-class must implement this method.")

    def close(self):
        """
        This closes the file object this handler represents.
        """
        raise NotImplementedError("Sub-class must implement this method.")

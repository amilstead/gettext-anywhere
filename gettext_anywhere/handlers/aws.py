import gettext
import logging
import os

from boto.s3 import connection as s3_conn
from boto.s3 import key as s3_key

from . import core

LANGUAGE = "LANGUAGE"
LANG = "LANG"
LC_MESSAGES = "LC_MESSAGES"
LC_ALL = "LC_ALL"
DEFAULT_ENVVARS = [
    LANGUAGE, 
    LC_ALL, 
    LC_MESSAGES, 
    LANG
]


_default_localedir = os.path.join("locale")

logger = logging.getLogger(__name__)

class S3FileHandler(core.FileHandler):
    """
    A custom file handler to search for and load translations files from an S3
    bucket.

    The bucket name is pass through via the "options" argument to the core
    FileHandler's init function.

    The `find` function mimics the default gettext `find` but searches for
    file paths inside of an S3 bucket, rather than on the file system itself.

    The `open` function simply sets a filename for usage in the `read` function.

    The `read` function pulls file contents from an S3 bucket.

    The `close` function just nulls out the filename set by `open`.
    """

    def __init__(self, *args, **kwargs):
        """
        Pulls bucket name and an optional "default_localedir" from the options
        dictionary.

        Initializes empty filename and connection variables.
        """
        super(S3FileHandler, self).__init__(*args, **kwargs)
        self._bucket_name = self._options["bucket_name"]
        self._aws_access_key_id = self._options.get(
            "aws_access_key_id",
            os.environ.get("AWS_ACCESS_KEY_ID")
        )
        self._aws_secret_access_key = self._options.get(
            "aws_secret_access_key",
            os.environ.get("AWS_SECRET_ACCESS_KEY")
        )
        self._default_localedir = self._options.get(
            "default_localedir",
            _default_localedir
        )
        self._filename = None
        self._connection = None

    def _get_conn(self):
        """
        Open an S3 connection and caches on this instance.

        :return: the S3 connection.
        """
        if self._connection is None:
            self._connection = s3_conn.S3Connection(
                aws_access_key_id=self._aws_access_key_id,
                aws_secret_access_key=self._aws_secret_access_key
            )
        return self._connection

    def find(self, localedir=None, languages=None, all=0):
        """
        Mimic gettext.find almost exactly -- os.path.exists is replaced with
        assembling an S3 key and checking for its existence instead.

        :param localedir: an optional localedir where translations are found.
        :param languages: which languages to search for.
        :param all: whether or not to read all found files, or just the first.
        :return: a list of file paths or a single file path in S3.
        """
        conn = self._get_conn()
        bucket = conn.get_bucket(self._bucket_name)
        if localedir is None:
            localedir = self._default_localedir

        if languages is None:
            languages = []
            for envar in DEFAULT_ENVVARS:
                val = os.environ.get(envar)
                if val:
                    languages = val.split(":")
                    break

            if "C" not in languages:
                languages.append("C")
        nelangs = []
        for lang in languages:
            for nelang in getattr(gettext, "_expand_lang")(lang):
                if nelang not in nelangs:
                    nelangs.append(nelang)

        result = [] if all else None
        domain_mo = "%s.mo" % self._domain
        for lang in nelangs:

            if lang == "C":
                break

            mofile = os.path.join(
                localedir,
                lang,
                LC_MESSAGES,
                domain_mo
            )
            mofile_lp = os.path.join(
                "locale-langpack",
                lang,
                LC_MESSAGES,
                domain_mo
            )
            key = s3_key.Key(bucket=bucket, name=mofile)
            if key.exists():
                if all:
                    result.append(mofile)
                else:
                    return mofile

            key = s3_key.Key(bucket=bucket, name=mofile_lp)
            if key.exists():
                if all:
                    result.append(mofile_lp)
                else:
                    return mofile_lp
        return result

    def open(self, filename):
        """
        "Opens" a given S3 file.
        This just sets the _filename variable for usage in `read`.

        :param filename: the filename to 'open'.
        """
        self._filename = filename

    def read(self):
        """
        Get an S3 connection and attempt to read the file.

        If the file doesn't exist, return an iterable empty string and let
        core gettext blow up as it would on a regular empty file.

        :return: file contents or empty string if not found.
        """
        conn = self._get_conn()
        bucket = conn.get_bucket(self._bucket_name)
        key = s3_key.Key(bucket=bucket, name=self._filename)
        if key.exists():
            return key.get_contents_as_string()
        return ""

    def close(self):
        """
        Clear the _filename variable.
        """
        self._filename = None



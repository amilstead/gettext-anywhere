# gettext-anywhere #

This is a python library for registering arbitrary file handlers that can read gettext files from any source location, not just the local file system.

By default, gettext reads directly from the file system rather than providing extended functionality for reading from any type of file system.

In the web application world -- it can be advantageous to update your translation catalogs without requiring a full re-deploy, since they would likely have to be re-compiled and saved onto a deployed application instance's file system.

## Installation ##

Install using pip and/or virtualenv:

    virtualenv <virtualenvs>/my-project
    pip install gettext-anywhere

Or easy_install:

    easy_install gettext-anywhere

### Optional Dependencies ###
This package includes an [S3FileHandler](gettext_anywhere/handlers/aws.py) out of the box, which relies on the [boto](https://pypi.python.org/pypi/boto) library.

If you want to use the S3FileHandler, you must install `boto` into your python runtime.

To install boto, use pip and/or virtualenv:

    pip install boto

Or easy_install:

    easy_install boto

## Usage ###
This package patches gettext's `translation` functionality in order to allow for discovering message catalogs that do not exist on a local file system.

As a result, after a registration command is performed, no additional usage of the library is necessary.

Simply call the function that's right for you inside the [registry](gettext_anywhere/registry.py) module and go on about your business.

### Handler Registration ###
Handler registration is performed on a domain by domain basis.

To register a handler for the default domain ("messages") one would do the following:

    from gettext_anywhere import registry

    registry.register_default_handler(
        my_handler_class,
        options={'options': 'dict'}
    )

To register a handler for a custom domain, one would do the following:

    from gettext_anywhere import registry

    registry.register_domain_handler(
        'my-translations-domain',
        my_handler_class,
        options={'options': 'dict'}
    )

### Provided Handlers ###
#### RegularFileHandler ####
**NOTE**: The RegularFileHandler is the default file handler in the event that no other handlers have been registered.

The [RegularFileHandler](gettext_anywhere/handlers/file.py) mimics the default gettext behavior.

It uses the core [FileHandler](gettext_anywhere/handlers/core.py) interface to open a file object for reading as well as shadows its `find` command down to default gettext's `find` function.

#### S3FileHandler ####
The [S3FileHandler](gettext_anywhere/handlers/aws.py) relies on the `boto` library to access contents inside an S3 bucket in AWS.

The options for an S3FileHandler are:

* `bucket_name`: The name of the S3 bucket to access.
* `default_localedir`: An optional locale directory inside the S3 bucket where translations are stored (it will look in the root of the bucket by default).
* `aws_access_key_id`: AWS access key (defaults to `AWS_ACCESS_KEY_ID` environment variable).
* `aws_secret_access_key`: AWS secret key (defaults to `AWS_SECRET_ACCESS_KEY` environment variable).

### Writing a Handler ###
Writing a handler is simple -- it is a class which must inherit the core [FileHandler](gettext_anywhere/handlers/core.py) and must implement four functions:

* `open(self, filename)`: This function should open the provided file and cache its file pointer (or contents) on itself.
* `find(self, localedir=None, languages=None, all=0)`: This function should return a single file path or list of file paths for use by `open` and `read` for gettext translation objects. **These file paths are your <domain>.mo files**.
* `read(self)`: Read the file contents and return them as an iterable.
* `close(self)`: Close the file that was opened (and probably read) using `open`.

See [S3FileHandler](gettext_anywhere/handlers/aws.py) for an example of a custom file handler implementation.

## Examples ##

Checkout the [examples](examples) directory.

A quick one would be:

    from gettext_anywhere import registry
    from gettext_anywhere.handlers import aws
    registry.set_default_handler(
        aws.S3FileHandler,
        options={
            "bucket_name": "my-bucket",
            "aws_access_key_id": <my-access-key-id>,
            "aws_secret_access_key": <my-secret-access-key>
        }
    )

    ...

    import gettext
    spanish = gettext.translation("messages", languages=["es_ES"])
    print spanish.gettext("Some translated string!")

## Contributing ##
* For the repository.
* Make changes.
* Submit a pull request.

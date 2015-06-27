import argparse
import gettext
import locale

from gettext_anywhere import registry
from gettext_anywhere.handlers import aws as aws_handlers


def main(domain, lang):
   t = gettext.translation(domain, languages=[lang])
   print t.gettext("Test translation.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--bucket-name",
        type=str,
        required=True
    )
    parser.add_argument(
        "--domain",
        type=str,
        default="messages"
    )
    parser.add_argument(
        "--lang",
        type=str,
        default="de_DE"
    )
    args = parser.parse_args()

    options = {
        "bucket_name": args.bucket_name
    }
    if args.domain != "messages":
        registry.register_domain_handler(
            args.domain,
            aws_handlers.S3FileHandler,
            options=options
        )
    else:
        registry.register_default_handler(
            aws_handlers.S3FileHandler,
            options=options
        )

    main(args.domain, args.lang)


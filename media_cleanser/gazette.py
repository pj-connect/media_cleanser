# @see: https://www.crummy.com/software/BeautifulSoup/bs4/doc
# @see: https://github.com/mozilla/readability
# @see: https://github.com/cure53/DOMPurify
# @see: https://github.com/Distributive-Network/PythonMonkey
# @see: https://lxml.de/
# @see: https://docs.python.org/3/py-modindex.html#

from bs4 import BeautifulSoup
from lxml import etree
import json
from urllib.parse import urlparse, parse_qs, urlencode

import gc
import argparse
import re
import io
import os.path as path
import shutil
import sys
from importlib import resources

global verbose  # TODO: implement verbose
verbose = False

media_list = """
Supported medias:

    + montrealgazette.com
    + ottawacitizen.com
    + financialpost.com
"""


def extract(elt):
    if elt is not None:
        elt.extract()


def lxml_extract(elt):
    if elt is not None:
        for e in elt:
            e.getparent().remove(e)


def xml_pp(elt):
    """
    Debug strings:

        print(etree.tostring(dom))
        print(soup.prettify())
    """
    if elt is not None:
        for e in elt:
            print(etree.tostring(e))


def cleanse_gazette(media: str, file_in: io.TextIOWrapper, file_out: str = None):
    """
    Use a json file with xpath rules for elements extractions
    """

    with file_in as f:

        soup = BeautifulSoup(file_in, 'lxml')  # using both BS4 and LXML may be overkill
        dom = etree.HTML(str(soup))

        with resources.path('resources.data.rules', f"{media}.json") as f2:
            with open(f2, 'r', encoding='utf-8') as json_data:
                metadata = json.load(json_data)

        for rule in metadata["rules"]:
            html = dom.xpath(rule)
            if len(html) == 0:
                print(f"Rule yeild no results : {rule}")
            else:
                lxml_extract(html)

        if file_out is None:
            f.seek(0)
            f.write(etree.tostring(dom, pretty_print=True).decode())
            f.truncate()
            f.close()
        else:
            with open(file_out, 'w', encoding="utf-8") as f3:
                soup.encode("utf8")
                f3.write(etree.tostring(dom, pretty_print=True).decode())
                f3.close()


def main():

    def read_write_file(filename: str) -> dict:  # Originally used as a type constructor for argument -f|--file
        if path.isfile(filename) and not path.islink(filename):
            return {"filename": filename, "stream": io.open(filename, 'r+', encoding='UTF-8')}
        else:
            print(f"File does not exist : {filename}")
            exit(1)

    def backup(file_in: io.TextIOWrapper):
        with open(f"{file_in.name}.backup", 'w', encoding="utf-8") as dest:
            shutil.copyfileobj(file_in, dest)
            file_in.seek(0)
            dest.close()

    gc.enable()

    # @see: https://realpython.com/command-line-interfaces-python-argparse/
    parser = argparse.ArgumentParser(
        prog='gazette',
        description="""
        Cleanse media(s) readable webpage of clutters.
        """,
        epilog='v1.0.2',
        add_help=True
    )

    parser.add_argument(
        '-l', '--list', action='store_true',
        help="""Displays a list of supported medias"""
    )

    parser.add_argument(
        '-v', '--verbose', action='store_true',
        help="""Set verbosity to on."""
    )

    subparser = parser.add_subparsers()
    cleanse_subparser = subparser.add_parser('cleanse', help='The cleanse command to decluter the readability webpage')

    group = cleanse_subparser.add_argument_group('inputs', """Specify the input data to be cleansed.""")
    exlusive_group = group.add_mutually_exclusive_group(required=True)  # Allmost useless mutually exclusive group

    exlusive_group.add_argument(
        '-f', '--file',
        type=str,
        help="""Path to a file to be cleanse. iF -o | --out is not specified, the changes a made in place and makes a backup before changes."""
    )

    exlusive_group.add_argument(  # Check if url validation is possible ; @see: https://yarl.aio-libs.org/en/latest/
        '-u', '--url',
        help="""Provide an url instead of a file."""
    )

    cleanse_subparser.add_argument(
        '-m', '--media',
        required=True,
        default="montrealgazette",
        help="""Specifiy media (ex. : montrealgazette)."""
    )

    cleanse_subparser.add_argument(
        '-o', '--out',
        type=str,
        help="""Path for the cleansed content to an output file."""
    )

    args = parser.parse_args()

    global verbose
    verbose = args.verbose

    if args.list:
        print(media_list)
        exit(0)

    if args.url is None and args.file is None:  # obselete
        print("No input specified. Use -f | --file, -u | --url")
        exit(1)

    if args.url is not None:
        print("This feature is not impeented yet")
        exit(1)

    if args.media.lower() in ["ottawacitizen", "montrealgazette",  "financialpost"]:
        if args.url is None and args.file is not None:
            with open(args.file, 'r+', encoding="utf-8") as file:
                if args.out is None:
                    backup(file)
                cleanse_gazette(args.media, file, args.out)
        else:
            print(f"Media not supported: {args.media}")

    gc.collect()


if __name__ == "__main__":

    # calling main function
    main()

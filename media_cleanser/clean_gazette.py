# @see: https://www.crummy.com/software/BeautifulSoup/bs4/doc
# @see: https://github.com/mozilla/readability
# @see: https://github.com/Distributive-Network/PythonMonkey
# @see: https://lxml.de/

from bs4 import BeautifulSoup
from lxml import etree

import gc
import argparse
from urllib.parse import urlparse, parse_qs, urlencode
import re
import io


def read_write_file(filename: str):
    return io.open(filename, 'r+', encoding='UTF-8')


def extract(elt):
    if elt is not None:
        elt.extract()


def lxml_extract(elt):
    if elt is not None:
        for e in elt:
            e.getparent().remove(e)


def xml_pp(elt):
    if elt is not None:
        for e in elt:
            print(etree.tostring(e))


def clean_montreal_gazette(file, in_place: bool = True):

    with file as f:

        soup = BeautifulSoup(file, 'lxml')  # using both BS4 and LXML may be overkill
        dom = etree.HTML(str(soup))

        lxml_extract(dom.xpath("//img[@aria-labelledby='wire-company-name']"))
        lxml_extract(dom.xpath("//nav[@id='account-menu']"))
        lxml_extract(dom.xpath("//nav[@id='sidebar']"))
        lxml_extract(dom.xpath("//nav[@data-aqa='nav-breadcrumb']"))
        lxml_extract(dom.xpath("//div[@data-widget='newsletter']"))
        lxml_extract(dom.xpath("//nav[@id='secondary-nav']"))
        lxml_extract(dom.xpath("//section[@id='article-block']"))
        lxml_extract(dom.xpath("//section[@data-carousel-type='list']"))
        lxml_extract(dom.xpath("//section[starts-with(@id, 'ad__inner')]"))
        lxml_extract(dom.xpath("//div[starts-with(@id, 'ad__inner')]"))

        f.seek(0)
        f.write(etree.tostring(dom, pretty_print=True).decode())
        f.truncate()


def clean_gazette(file, in_place: bool = True):
    """
    Stud for future website support
    """

    with file as f:

        soup = BeautifulSoup(file, 'lxml')

        f.seek(0)
        f.write(str(soup))
        f.truncate()


def main():

    gc.enable()

    # @see: https://realpython.com/command-line-interfaces-python-argparse/
    parser = argparse.ArgumentParser(
        prog='clean-gazette',
        description="""

        Cleanse montreal gazette readable webpage of clutters.

        Supported media:

            + montrealgazette.com
            + ottawacitizen.com
        """,
        epilog='v1.0.1',
        add_help=True
    )

    group = parser.add_argument_group('Input', """Specify the input data to be cleansed.""")
    exlusive_group = group.add_mutually_exclusive_group(required=True)

    exlusive_group.add_argument(  # TODO: Make a backup file
        '-f', '--file',
        type=read_write_file,
        help="""Path to a file to be cleanse. iF -o | --out is not specified, the changes a made in place and makes a backup before changes."""
    )

    exlusive_group.add_argument(
        '-u', '--url',
        help="""Provide an url instead of a file. If -o | --out is not specified, output is printed to stdout."""
    )

    parser.add_argument(
        '-m', '--media',
        required=False, help="""Support for other media (ex. : ottawacitizen)."""
    )

    parser.add_argument(
        '-o', '--out',
        type=read_write_file,
        help="""Path to a cleansed output file. If -o | --out is not specified, output is printed to stdout."""
    )

    parser.add_argument(
        '-v', '--verbose', action='store_true',
        help="""Set verbosity to on."""
    )

    args = parser.parse_args()

    if args.url is None and args.file is None:
        print("No input specified. Use -f | --file, -u | --url")
        exit(1)

    if args.url is not None:
        print("This feature is not impeented yet")
        exit(1)

    match args.media:
        case "financialpost": # useless for now ; https://financialpost.com/real-estate/canada-affordability-crisis-build-new-homes
            clean_gazette(args.file)
        case "montrealgazette" | _:
            clean_montreal_gazette(args.file)

    gc.collect()


if __name__ == "__main__":

    # calling main function
    main()

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

import argparse

import subapi

import os

from . import __version__
from dateutil.parser import parse
from prettytable import PrettyTable
from termcolor import colored


def args_parse():
    parser = argparse.ArgumentParser(usage="-h for full usage")
    parser.add_argument(
        '-V', '--version', action='version', version=__version__)
    parser.add_argument('query', help='search string', nargs='+')
    parser.add_argument(
        '-n', dest="maxnumber", help="maximum number of results", type=int)
    parser.add_argument(
        '-lang', dest="language", help="language code of subtitles")
    parser.add_argument(
        '--subscene', action="store_true", help="search subscene")
    parser.add_argument(
        '--opensubtitles', action="store_true", help="search opensubtitles")
    args = parser.parse_args()
    return args


def pretty_print(data):
    output = PrettyTable(["I", "Lang", "Release", "Date"])
    output.align = "l"
    output.reversesort = True
    for item in data:
        index = colored(item, 'red')
        lang = colored(data[item]['lang'], 'yellow', 'on_grey')
        dt = parse(data[item]['date'])
        date = colored(dt.strftime('%d/%m/%Y'), 'blue')
        release = colored(data[item]["movie"].encode('utf-8').strip(), 'green')
        output.add_row([index, lang, release, date])
    print output


def main():
    try:
        args = args_parse()
        query = " ".join(args.query)
        language = args.language if args.language else 'en'
        maxnumber = args.maxnumber if args.maxnumber else 10
        if args.subscene:
            results = subapi.search(
                'subscene', query, language, maxnumber)
        elif args.opensubtitles:
            results = subapi.search(
                'opensubtitles', query, language, maxnumber)
        data = dict(enumerate(results, start=1))
        pretty_print(data)
        choice = raw_input("Choose subtitle to download : \t")
        dldir = os.getcwd()
        subapi.download('opensubtitles', data[int(choice)], dldir)
    except KeyboardInterrupt:
        print "Exiting"
        sys.exit(0)

if __name__ == '__main__':
    main()

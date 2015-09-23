#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

import argparse

from dateutil.parser import parse
from prettytable import PrettyTable
from sabertooth import opensubs
from termcolor import colored


def args_parse():
    parser = argparse.ArgumentParser(usage="-h for full usage")
    parser.add_argument('query', help='source directory', nargs='+')
    parser.add_argument(
        '-n', dest="maxnumber", help="update database", type=int)
    parser.add_argument('-lang', dest="language", help="update database")
    args = parser.parse_args()
    return args


def pretty_print(data):
    output = PrettyTable(["I", "Lang", "Release", "Date"])
    output.align = "l"
    output.sortby = "Date"
    output.reversesort = True
    for item in data:
        index = colored(item, 'red')
        lang = colored(data[item]['lang'], 'yellow', 'on_grey')
        dt = parse(data[item]['date'])
        date = colored(dt.strftime('%d/%m/%Y'), 'blue')
        release = colored(data[item]["movie"].encode('utf-8'), 'green')
        output.add_row([index, lang, release, date])
    print output


def main():
    try:
        args = args_parse()
        results = opensubs().query(
            " ".join(args.query), args.maxnumber, args.language)
        data = dict(enumerate(results))
        pretty_print(data)
        choice = raw_input("Choose subtitle to download : \t")
        opensubs().download_subtitle(data[int(choice)])
    except KeyboardInterrupt:
        print "Exiting"
        sys.exit(0)

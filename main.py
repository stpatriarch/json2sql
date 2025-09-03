#!/usr/bin/env python3

# Գործիքը կոչված է օգնել վերափոխել json֊ը sqlite3 ֆայլի։

import argparse
from src.modules import SqliteData
from src.modules import JsonModify

def convert(args):

    # init input json file input file -> ifile
    ifile = JsonModify(file=args.input)
    ifile._connect
    ifile = ifile.json_normalize()

    # prepare output file. output file -> ofile
    ofile = SqliteData(js_file=ifile, name=args.input, table=args.table)
    ofile.create()
    ofile.insert()

def main():
    parser = argparse.ArgumentParser(description="ԱՅՍ ԳՈՐԾԻՔԸ ԿՈՉՎԱԾ Է ՕԳՆԵԼ ՎԵՐԱՓՈԽԵԼ(ԿՈՆՎԵՐՏԱՑԻԱ) JSON֊Ը SQLITE3 ՖԱՅԼԻ։")
    parser.add_argument('--input', '-i', required=True, help='json ֆայլի ճանապարհ')
    parser.add_argument('--table', '-t', required=True, help='SQL աղյուսակի անուն')

    args = parser.parse_args()
    convert(args=args)


if __name__ == '__main__':
    main() 
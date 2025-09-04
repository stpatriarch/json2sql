#!/usr/bin/env python3

# Գործիքը կոչված է օգնել վերափոխել json֊ը sqlite3 ֆայլի։

import argparse
from json2sql.modules import SqliteData, JsonModify

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
    parser = argparse.ArgumentParser(description="ԱՅՍ ԳՈՐԾԻՔԸ ԿՈՉՎԱԾ Է ՕԳՆԵԼ ՎԵՐԱՓՈԽԵԼ JSON֊Ը SQL DB ՖԱՅԼԻ։" \
    "\n THIS TOOL HELPS TO CONVERT JSON FILE TO SQL DB.")
    parser.add_argument('--input', '-i', required=True, help='json ֆայլի ճանապարհ | json file path')
    parser.add_argument('--table', '-t', required=True, help='SQL աղյուսակի անուն | SQL column name')

    args = parser.parse_args()
    convert(args=args)


if __name__ == '__main__':
    main()
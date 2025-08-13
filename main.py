#!/usr/bin/env python3

# Գործիքը կոչված է օգնել վերափոխել json֊ը sqlite3 ֆայլի։

import argparse
from include.sqlite_engine import SqliteData
from include.json_engine import JsonModify



def main():
    parser = argparse.ArgumentParser(description="ԱՅՍ ԳՈՐԾԻՔԸ ԿՈՉՎԱԾ Է ՕԳՆԵԼ ՎԵՐԱՓՈԽԵԼ(ԿՈՆՎԵՐՏԱՑԻԱ) JSON֊Ը SQLITE3 ՖԱՅԼԻ։")
    subparsers = parser.add_subparsers(dest='command', required=True)

    convert_parser = subparsers.add_parser('convert', help='վերափոխման հրաման')
    convert_parser.add_argument('--input', '-i', required=True, help='json ֆայլի ճանապարհ')
    convert_parser.add_argument('--table', '-t', required=True, help='SQL աղյուսակի անուն')
    # convert_parser.add_argument('--db', '-d', required=True, help='Файл SQLite-базы')
    help_parser = subparsers.add_parser('info', help='ավելի ըմդարձակ տեղեկություն')

    convert_parser.set_defaults(func=convert)
    help_parser.set_defaults(func=help_)

    args = parser.parse_args()
    args.func(args)

def help_(args=None):
    print(''' ''')


def convert(args):
    j_file = JsonModify(file=args.input)
    j_file._connect
    j_f = j_file.json_normalize()
    # j_file.json
    sql = SqliteData(js_file=j_f, name=args.input, table=args.table)
    # print(type(next(iter(sql.json.keys()))[0]))
    # # for rows in sql.json.values():
    # #     for row in rows:
    # #         keys = ", ".join(key for key in row)
    # # keys_ = ', '.join({key for rows in sql.json.values() for row in rows for key in row})
    # # print(keys_)
    sql.create()
    sql.insert()
    # json_to_sqlite(args.input, args.table, args.db)

if __name__ == '__main__':
    main() 
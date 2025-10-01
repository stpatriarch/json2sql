#!/usr/bin/env python3

import argparse

def is_json(file: str) -> str:
    if not file.lower().endswith('.json'):
        raise argparse.ArgumentTypeError('Ֆայլը պետք է լինի json | File must be a json')
    return file

def parser():
    parser = argparse.ArgumentParser(description="ԱՅՍ ԳՈՐԾԻՔԸ ԿՈՉՎԱԾ Է ՕԳՆԵԼ ՎԵՐԱՓՈԽԵԼ JSON֊Ը SQL DB ՖԱՅԼԻ։" \
    "\n THIS TOOL HELPS TO CONVERT JSON FILE TO SQL DB.")
    subparsers = parser.add_subparsers(dest='engine', required=True)

    sqlite_parser = subparsers.add_parser('sqlite', help='sqlite շարժիչ | sqlite engine')
    
    sqlite_parser.add_argument('--input', '-i', required=True, type=is_json, help='json ֆայլի ճանապարհ | json file path')
    sqlite_parser.add_argument('--table', '-t', required=True, help='SQL աղյուսակի անուն | SQL column name')

    postgres_parser = subparsers.add_parser('postgres', help='postgres շարժիչ | postgres engine')
    postgres_parser.add_argument('--input', '-i', required=True, type=is_json, help='json ֆայլի ճանապարհ | json file path')

    postgres_parser.add_argument("--host", default="localhost", help="Բազզայի հոսթը | Base host")
    postgres_parser.add_argument("--user", default="postgres", help="Բազզայի օգտատերը | Base user")
    postgres_parser.add_argument("--password", default="postgres", help="Բազզայի գաղտնաբառը | base password")
    postgres_parser.add_argument("--port", type=int, default=5432, help="Հոսթի պորտը | Host port")

    postgres_parser.add_argument("--name", default="postgres", help="Բազզայի անունը | Base name")
    postgres_parser.add_argument('--table', '-t', required=True, help='SQL աղյուսակի անուն | SQL column name')

    mysql_parser = subparsers.add_parser('mysql', help='mysql շարժիչ | mysql engine')
    mysql_parser.add_argument('--input', '-i', required=True, type=is_json, help='json ֆայլի ճանապարհ | json file path')

    mysql_parser.add_argument("--host", default="localhost", help="Բազզայի հոսթը | Base host")
    mysql_parser.add_argument("--user", default="root", help="Բազզայի օգտատերը | Base user")
    
    mysql_parser.add_argument("--port", type=int, default=3306, help="Հոսթի պորտը | Host port")

    mysql_parser.add_argument("--name", default="myql", help="Բազզայի անունը | Base name")
    mysql_parser.add_argument('--table', '-t', required=True, help='SQL աղյուսակի անուն | SQL column name')

    
    
    

    return parser.parse_args()
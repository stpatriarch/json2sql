#!/usr/bin/env python3

# Գործիքը կոչված է օգնել վերափոխել json֊ը sqlite3 ֆայլի կամ գրանցել դրանք տրված postgres, mysql սերվերների ՏԲ-ում։
# Инструмент предназначен для преобразования JSON в файл SQLite3 или для записи данных в БД указанных серверов PostgreSQL и MySQL.
# The tool is designed to convert JSON into an SQLite3 file or to insert the data into a database on specified PostgreSQL or MySQL servers.

from json2sql.modules.json import JsonModCore
from json2sql.modules.sql import EngineFacotory
from json2sql.tools import create_parser
from rich.console import Console


info_message = Console(style='green bold')

def main():
    parser = create_parser()
    args = parser.parse_args()

    inputfile = JsonModCore(path=args.input).json_normalize()
    outfile = None

    if inputfile:

        outfile = EngineFacotory(input_file=inputfile, args=args).create()
    
    if outfile:

        outfile.insert()
        info_message.print(' Converted Succesfully \U00002705')

if __name__ == '__main__':
    main()

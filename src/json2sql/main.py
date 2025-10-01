#!/usr/bin/env python3

# Գործիքը կոչված է օգնել վերափոխել json֊ը sqlite3 ֆայլի կամ գրանցել դրանք տրված postgres, mysql սերվերների ՏԲ-ում։
# Инструмент предназначен для преобразования JSON в файл SQLite3 или для записи данных в БД указанных серверов PostgreSQL и MySQL.
# The tool is designed to convert JSON into an SQLite3 file or to insert the data into a database on specified PostgreSQL or MySQL servers.


from json2sql.modules import JsonModify, SqliteEngine, PostgresEngine, MysqlEngine
from json2sql.tools import parser




def main():
    args = parser()

    # init input json file input file -> ifile
    inputfile = JsonModify(file=args.input).json_normalize()


    if args.engine in ('sqlite',):
        outfile = SqliteEngine(js_file=inputfile, 
                                   dbname=args.input, table=args.table)

    elif args.engine in ('postgres',):
        outfile = PostgresEngine(js_file=inputfile, 
                                   host=args.host, user=args.user, 
                                   password=args.password, dbname=args.name, 
                                   table=args.table, port=args.port)
        
    elif args.engine in ('mysql',):
        outfile = MysqlEngine(js_file=inputfile, 
                                   host=args.host, user=args.user, 
                                   password=args.password, dbname=args.name, 
                                   table=args.table, port=args.port)
        
    outfile.insert()
    print(' Converted Succesfully \U00002705')




if __name__ == '__main__':
    main()

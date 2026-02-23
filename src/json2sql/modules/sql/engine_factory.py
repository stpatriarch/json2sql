#!/usr/bin/env python3

from .sql_engine import SqliteEngine, PostgresEngine, MysqlEngine
from argparse import Namespace

class EngineFacotory:
    """
    Factory class for creating SQL engine instances based on CLI arguments.
    """

    def __init__(self, input_file: tuple, args: Namespace) -> None:
        """
        Initialize the engine factory with input JSON data and CLI arguments.

        :param input_file: JSON data and its structure type.
        :type input_file: tuple
        :param args: Parsed CLI arguments.
        :type args: armgpars.Namespace
        """

        self.input_file = input_file
        self.args = args
        self.engine = args.engine

    def create(self):
        """
        Instantiate and return the SQL engine correspanding to the selected type.

        :return: An instance of the requested SQL engine or ``None`` if unsupported. 
        """

        if self.engine in ('sqlite',):
            return SqliteEngine(js_file=self.input_file, 
                                   dbname=self.args.input, table=self.args.table)
        

        elif self.engine in ('postgres',):
            return PostgresEngine(js_file=self.input_file, 
                                   host=self.args.host, user=self.args.user, 
                                   password=self.args.password, dbname=self.args.name, 
                                   table=self.args.table, port=self.args.port)


        elif self.engine in ('mysql',):
            return MysqlEngine(js_file=self.input_file, 
                                   host=self.args.host, user=self.args.user, 
                                   password=self.args.password, dbname=self.args.name, 
                                   table=self.args.table, port=self.args.port)

        else:
            return None


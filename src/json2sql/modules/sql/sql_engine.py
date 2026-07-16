#!/usr/bin/env python3

import sqlite3
import psycopg
import pymysql
from abc import ABC, abstractmethod
from .sql_data_types import SqlEngineAcceptType
from .sql_type_mapping import PLACEHOLDERS
from typing import Any


class SqlEngine(ABC, SqlEngineAcceptType):

    """
    Class acts as a base class for all sql engines.
    Providing common logic and mandatory implementation 
    of some functions in inherited classes.
    """

    def __init__(self, engine: str, js_file: tuple, table: str) -> None:
        """
        Initialize engine type, JSON data, table name to performing table creation.

        :param engine: Supported engine name.
        :type engine: str
        :param js_file: JSON data and internal conditional group.
        :type js_file: tuple
        :param table: Table name to creation.
        :type table: str
        """

        super().__init__(engine=engine)
        self.engine: str = engine

        self.table = table

        self.json = js_file[0]
        self.j_type = js_file[1]

    @abstractmethod
    def connection(self, *args, **kwargs) -> Any:
        """
        Performs operations assosiated with read and write to DB.
        """
        pass

    def create(self) -> None:
        """
        Creates a db table in connected database.

        :return: Cursor object resulting from the executed query.
        """

        columns = ', '.join(f"{name_} {type_}" for name_, type_ in self.define_types(json=self.json, ident=self.j_type).items())
        table = f"""
            CREATE TABLE IF NOT EXISTS {self.table} ({columns})
               """
           
        return self.connection(table)
    

    def insert(self) -> None:
        """
        The execution of the create function prepare keys placeholders and inserts a data to database.

        :return: Cursor object resulting from the executed query.
        """
        self.create()

        order_by_this: list | tuple = self.prepare_json_by_group

        keys = ", ".join(order_by_this)

        placeholder =  ", ".join([str(PLACEHOLDERS.get(self.engine))] * len(order_by_this))

        query = f'INSERT INTO {self.table} ({keys}) VALUES ({placeholder})'


        if self.values:

            for value in self.values:
                self.connection(query, values=value)


    @property
    def prepare_json_by_group(self) -> list | tuple:
        """
        Preparing a JSON data based on its internal conditional group.

        :return: Ordered sequence object based on its structure.
        """

        if self.j_type in ('dict_of_list_of_dict', 'dict_of_dict'):

            array_ = next(iter(self.json.values()), [])
            file_sample = array_[0] if isinstance(array_, list) else next(iter(self.json.values()))
            order_by_this =  ('id', *file_sample)

            for id, column in self.json.items():
                if isinstance(column, dict):
                    self.values.append((id, *(column.get(k) for k in column.keys())))
                
                elif isinstance(column, list):
                    for row in column:
                        self.values.append((id, *(row.get(k) for k in row.keys())))

        elif self.j_type in ('list_of_dict',):

            order_by_this = list(self.json[0].keys())
            self.values = [tuple(d[k] for k in order_by_this) for d in self.json]

        # incase flaten_dict
        else:

            order_by_this = list(self.json.keys())
            self.values = [tuple(self.json[k] for k in order_by_this)]

        return order_by_this



class SqliteEngine(SqlEngine):
    """
    Class provides connection support for Sqlite.
    """

    def __init__(self, js_file: tuple, dbname: str, table: str) -> None:
        
        """
        Initialize JSON data, database name and table name for SQLite
        database creation and data insertion.

        :param js_file: Normalized JSON data and its internal conditional group.
        :type js_file: tuple
        :param dbname: SQLite database file name.
        :type table: str
        :param table: Table name to be created.
        :type table: str
        """
        super().__init__('sqlite', js_file, table)

        self.db = dbname.split('.')[0] 

        self.connect = None

        self.values: list = []


    def open_(self) -> None:
        """
        Check the database connection status and open it if necessary.
        """
        if self.connect is None:

            self.connect = sqlite3.connect(f"{self.db}.db")


    def connection(self, content: str, values: list  | None = None) -> sqlite3.Cursor:
        """
        Performs operations assosiated with write to DB.

        :param content: Perfroms a database query.
        :type content: str
        :param values: Optional data to be written to the database.
        :type values: list | None
        :return: Cursor object resulting from the executed query.
        """      
        self.open_()

        if self.connect is None:
        
            raise RuntimeError('Database connection was not established')

        with self.connect:
            self.connect.row_factory = sqlite3.Row
            cursor = self.connect.cursor()
            cursor.execute(content, values or [])
            return cursor


class PostgresEngine(SqlEngine):
    """
    Class provides connection support for PostgreSql.
    """
    
    def __init__(self, js_file: tuple, host: str, user: str,  password: str, dbname: str, table: str,  port: int) -> None:
        """
        Initialize JSON data, database connection parameters and table name for PostgreSQL
        database connection and data insertion.

        :param js_file: Normalized JSON data and its internal conditional group.
        :type js_file: tuple
        :param host: Database host.
        :type host: str
        :param user: Database user name.
        :type user: str
        :param password: Database user password.
        :type password: str
        :param dbname: PostgreSQL database name.
        :type dbname: str
        :param table: Table name to be created.
        :type table: str
        :param port:  Database port number.
        :type port: int
        """

        self.host = host
        self.user = user
        self.password = password
        self.dbname = dbname
        self.port = port


        super().__init__('postgresql', js_file, table)

        self.connect = None
        self.values: list = []

    def open_(self) -> None:
        """
        Check the database connection status and open it if necessary.
        """

        if self.connect is None or self.connect.closed:

            self.connect = psycopg.connect(
                    host=self.host, 
                    user=self.user, 
                    password=self.password,  
                    dbname=self.dbname, 
                    port=self.port)

    def connection(self, content: str, values: list | None = None) -> psycopg.Cursor:
        """
        Performs operations assosiated with write to DB.

        :param content: Perfroms a database query.
        :type content: str
        :param values: Optional data to be written to the database.
        :type values: list | None
        :return: Cursor object resulting from the executed query.
        """      

        self.open_()

        if self.connect is None:

            raise RuntimeError('Database connection was not established')
        

        with self.connect.cursor() as cursor:
 
            cursor.execute(content, values or [])  # type: ignore
        self.connect.commit()

        return cursor


class MysqlEngine(SqlEngine):
    """
    Class provides connection support for Mysql.
    """
 
    def __init__(self, js_file: tuple, host: str, user: str,  password: str, dbname: str, table: str,  port: int,) -> None:
        """
        Initialize JSON data, database connection parameters and table name for MySQL
        database connection and data insertion.

        :param js_file: Normalized JSON data and its internal conditional group.
        :type js_file: tuple
        :param host: Database host.
        :type host: str
        :param user: Database user name.
        :type user: str
        :param password: Database user password.
        :type password: str
        :param dbname:  MySQL database name.
        :type dbname: str
        :param table: Table name to be created.
        :type table: str
        :param port:  Database port number.
        :type port: int
        """

        self.js_file = js_file
        self.host = host
        self.user = user
        self.password = password
        self.dbname = dbname
        self.table = table
        self.port = port

        self.connect = None
        self.values: list = []

        super().__init__('mysql', js_file, table)
    
    def open_(self) -> None:
        """
        Check the database connection status and open it if necessary.
        """

        if self.connect is None or not self.connect.open:

            self.connect = pymysql.connect(
                    host=self.host, 
                    user=self.user, 
                    password=self.password, 
                    database=self.dbname, 
                    port=self.port)

    def connection(self, content: str, values: list | None = None) -> pymysql.cursors.Cursor:
        """
        Performs operations assosiated with write to DB.

        :param content: Perfroms a database query.
        :type content: str
        :param values: Optional data to be written to the database.
        :type values: list | None
        :return: Cursor object resulting from the executed query.
        """      

        self.open_()

        if self.connect is None:
            raise RuntimeError('Database connection was not established')

        with self.connect.cursor() as cursor:
 
            cursor.execute(content, values or [])
        self.connect.commit()
        return cursor



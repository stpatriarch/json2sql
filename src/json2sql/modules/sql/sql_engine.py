#!/usr/bin/env python3

import sqlite3
import psycopg
import pymysql
from abc import ABC, abstractmethod
from json2sql.modules.sql import SqlEngineAcceptType, PLACEHOLDERS




class SqlEngine(ABC):

    """
    Class acts as a base class for all sql engines.
    Providing common logic and mandatory implementation 
    of some functions in inherited classes.
    """

    @abstractmethod
    def connection(self) -> None:
        pass

    def create(self) -> None:

            columns = ', '.join(f"{name_} {type_}" for name_, type_ in self.engine.define_types(json=self.json, ident=self.j_type).items())
            table = f"""
            CREATE TABLE IF NOT EXISTS {self.table} ({columns})
               """
           
            return self.connection(table)
    

    def insert(self) -> None:

        self.create()

        order_by_this: list[str] = self.prepare_json_by_group

        keys = ", ".join(order_by_this)

        placeholder =  ", ".join([PLACEHOLDERS.get(self._engine)] * len(order_by_this))

        query = f'INSERT INTO {self.table} ({keys}) VALUES ({placeholder})'


        if self.values:

            for value in self.values:
                self.connection(query, values=value)


    @property
    def prepare_json_by_group(self) -> list:

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

        else:

            order_by_this = list(self.json.keys())
            self.values = [tuple(self.json[k] for k in order_by_this)]

        return order_by_this



class SqliteEngine(SqlEngine):

    """
    Class provides connection support for Sqlite.
    Makes a connection
    Create a table
    Data record
    """

    engine = SqlEngineAcceptType('sqlite')

    def __init__(self, js_file: dict, dbname: str, table: str) -> None:

        self.db = dbname.split('.')[0] # համանուն դբ ֆայլի գեներացիայի համար։ Առանց հավելալյալ սիմվոլների անուն․դբ։
        self.json = js_file[0]
        self.j_type = js_file[1]
        self.table = table
        self.connect = sqlite3.connect(f"{self.db}.sql")

        self._engine: str = 'sqlite'
        self.values: str = []

    def connection(self, content: str, values=False) -> sqlite3.Cursor:

        with self.connect:
            self.connect.row_factory = sqlite3.Row
            cursor = self.connect.cursor()
            cursor.execute(content, values or [])
            return cursor


class PostgresEngine(SqlEngine):

    """
    Class provides connection support for PostgreSql.
    Makes a connection
    Create a table
    Data record
    """
    engine = SqlEngineAcceptType('postgresql')
    
    def __init__(self, js_file: dict, host: str, user: str,  password: str, dbname: str, table: str,  port: str,) -> None:

        self.json = js_file[0]
        self.j_type = js_file[1]
        self.table = table
        self.connect = psycopg.connect(host=host, user=user, password=password,  dbname=dbname, port=port)

        self._engine: tuple[str, str] = ('postgresql', 'mysql')
        self.values: str = []

    def connection(self, content: str, values=False) -> None:

        with self.connect.cursor() as cursor:
 
            cursor.execute(content, values or [])
        self.connect.commit()


class MysqlEngine(SqlEngine):

    """
    Class provides connection support for Mysql.
    Makes a connection
    Create a table
    Data record
    """
    engine = SqlEngineAcceptType('mysql')
    
    def __init__(self, js_file: dict, host: str, user: str,  password: str, dbname: str, table: str,  port: str,) -> None:

        self.json = js_file[0]
        self.j_type = js_file[1]

        self.table = table
        self.connect = pymysql.connect(host=host, user=user, password=password, database=dbname, port=port)

        self._engine: tuple[str, str] = ('postgresql', 'mysql')
        self.values: str = []

    def connection(self, content: str, values=False) -> psycopg.Cursor:

        with self.connect.cursor() as cursor:
 
            cursor.execute(content, values or [])
        self.connect.commit()




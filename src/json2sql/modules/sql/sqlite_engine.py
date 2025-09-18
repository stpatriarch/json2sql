#!/usr/bin/env python3

import sqlite3
from json2sql.modules import SqlEngineAcceptType




class SqliteEngine:

    engine = SqlEngineAcceptType('sqlite')

    def __init__(self, js_file: dict, name: str, table: str) -> None:
        self.db = name.split('.')[0] # համանուն դբ ֆայլի գեներացիայի համար։ Առանց հավելալյալ սիմվոլների անուն․դբ։
        self.json = js_file[0]
        self.j_type = js_file[1]
        self.table = table
        self.connection = sqlite3.connect(f"{self.db}.db")
        self.values: str = []

    def _connection(self, content: str, values=False) -> sqlite3.Cursor:

        with self.connection:
            self.connection.row_factory = sqlite3.Row
            cursor = self.connection.cursor()
            cursor.execute(content, values or [])
            return cursor

    def create(self) -> None:

            columns = ', '.join(f"{name_} {type_}" for name_, type_ in self.engine.define_types(json=self.json, ident=self.j_type).items())
            table = f"""
            CREATE TABLE IF NOT EXISTS {self.table} ({columns})
               """
           
            return self._connection(table)


    def insert(self) -> None:

        self.create()

        order_by_this: list[str] = self.prepare_json_group

        keys = ", ".join(order_by_this)

        placeholder =  ", ".join(['?'] * len(order_by_this))

        query = f'INSERT INTO {self.table} ({keys}) VALUES ({placeholder})'


        if self.values:

            for value in self.values:
                self._connection(query, values=value)

    @property
    def prepare_json_group(self) -> list:

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
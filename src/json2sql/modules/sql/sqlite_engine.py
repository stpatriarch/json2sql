#!/usr/bin/env python3

import sqlite3
from abc import ABC, abstractmethod
from json2sql.tools import define_types


class SqliteData():

    def __init__(self, js_file: dict, name: str, table: str)-> None:
        self.db = name.split('.')[0] # համանուն դբ ֆայլի գեներացիայի համար։ Առանց հավելալյալ սիմվոլների անուն․դբ։
        self.json = js_file[0]
        self.j_type = js_file[1]
        self.table = table
        self.connection = sqlite3.connect(f"{self.db}.db")     

    def _connection(self, content: str, values=False)-> sqlite3.Cursor:

        with self.connection:
            self.connection.row_factory = sqlite3.Row
            cursor = self.connection.cursor()
            cursor.execute(content, values or [])
            return cursor

    def create(self)-> None:

            columns = ', '.join(f"{name_} {type_}" for name_, type_ in define_types(data=self.json, j_type=self.j_type).items())
            table = f"""
            CREATE TABLE IF NOT EXISTS {self.table} ({columns})
               """
            print('columns', columns)
            return self._connection(table)


    def insert(self)-> None:

        values = []
        if self.j_type in ('dict_of_list_of_dict', 'dict_of_dict'):

            array_ = next(iter(self.json.values()), [])
            file_sample = array_[0] if isinstance(array_, list) else next(iter(self.json.values()))
            order_by_this =  ('id', *file_sample)

            for id, column in self.json.items():
                if isinstance(column, dict):
                    values.append((id, *(column.get(k) for k in column.keys())))
                
                elif isinstance(column, list):
                    for row in column:
                        values.append((id, *(row.get(k) for k in row.keys())))

        elif self.j_type in ('list_of_dict','list_of_dict_branched'):
            print(self.j_type)
            if self.j_type in ('list_of_dict_branched',):
                order_by_this = list(self.json.keys())

                v = [tuple(self.json[k] for k in order_by_this)]
                # values = [tuple(self.json[k] for k in order_by_this)]
            else:
                order_by_this = list(self.json[0].keys())
                values = [tuple(d[k] for k in order_by_this) for d in self.json]

                
            print(order_by_this, 'order_by_this')
            print('self.json', self.json)
            print(self.j_type)
            
            print('values', values)
        

        else:

            order_by_this = list(self.json.keys())
            print(order_by_this)
            values = [tuple(self.json[k] for k in order_by_this)]

        keys = ", ".join(order_by_this)

        placeholder =  ", ".join(['?'] * len(order_by_this))

        query = f'INSERT INTO {self.table} ({keys}) VALUES ({placeholder})'


        if values:
            print(values)
            print(self.j_type)


            for item in values:
                self._connection(query, values=item)



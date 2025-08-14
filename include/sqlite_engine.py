#!/usr/bin/env python3

import sqlite3
import json
from abc import ABC, abstractmethod
from include.tools import define_types

class DB_Mngr(ABC):

    @abstractmethod
    def _connection():
        pass
    

class SqliteData(DB_Mngr):

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
           
            return self._connection(table)


    def insert(self)-> None:

        values = []
        if self.j_type in ('dict_of_list_of_dicts', 'dict_of_dict'):

            array_ = next(iter(self.json.values()), [])
            file_sample = array_[0] if isinstance(array_, list) else next(iter(self.json.values()))
            order_by_this =  ('id', *file_sample) # list(next(iter(self.json.values()))[0])
            print(order_by_this, '--orderbythis')

            for id, column in self.json.items():
                if isinstance(column, dict):
                    values.append((id, *(column.get(k) for k in column.keys())))
                
                elif isinstance(column, list):
                    for row in column:
                        values.append((id, *(row.get(k) for k in row.keys())))
            
            print(values, '--Values')
        else:

            order_by_this = list(self.json.keys())
            values = [tuple(self.json[k] for k in order_by_this)]

        keys = ", ".join(order_by_this)

        placeholder =  ", ".join(['?'] * len(order_by_this))

        print(keys)
        print(placeholder)
        print(self.j_type)
        print(order_by_this)

        query = f'INSERT INTO {self.table} ({keys}) VALUES ({placeholder})'

        print(values)
        if values:

            for item in values:
                self._connection(query, values=item)



    



class JsonData(DB_Mngr):
    
    def __init__(self, name: str)-> object:
        self.name = name
        self._connection()

    def _connection(self)-> dict:

        with open(f"{self.js}", encoding="utf-8") as file:
            data = json.load(file)

        return data
    
    
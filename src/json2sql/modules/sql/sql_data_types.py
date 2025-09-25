#!/usr/bit/evn python3

from json2sql.modules.sql import SQL_TYPES as sql_types
from json2sql.tools import NotSupportedMixin

class SqlEngineAcceptType(NotSupportedMixin):
    """"
    Class defining accaptable data types
    for different SQL engines, for constructing
    right queries.
    ---
    sqlite: Sqlite Engine
    postgresql: PostgreSql Engine
    myslq: MySql engine
    ---
    """
    acceptable_engines: tuple[str, str, str] = ('sqlite', 'postgresql', 'mysql')


    def __init__(self, engine: str) -> None:
        
        self.engine: str = engine if engine in self.acceptable_engines else self.unsupported_engine(engine=engine)



    def define_types(self, json: dict, ident: str) -> dict:

        extracted_types = {}

        if ident in ('dict_of_list_of_dict', 'dict_of_dict',):

            array_ = next(iter(json.values()), [])
            file_sample = array_[0] if isinstance(array_, list) else next(iter(json.values()))
            id_ = next(iter(json.keys()))
            extracted_types['id'] = sql_types[self.engine].get(type(id_))

        elif ident in ('list_of_dict'):

            file_sample = next(iter(json))

        else:

            file_sample = json

        for name, type_ in file_sample.items():
            sql_type = sql_types[self.engine].get(type(type_))

            extracted_types[name] = sql_type
        
        return extracted_types
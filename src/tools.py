#!/usr/bin/env python3
def array_type(array_):

    if isinstance(array_, list):
        return array_[0]
    elif isinstance(array_, dict):
        return next(iter(array_.values()))
    else:
        return None
    

def define_types(data: dict, j_type: str )-> dict:

    extracted_types = {}

    types_d = {
        int: 'INTEGER', bool: 'INTEGER', float: 'REAL', str: 'TEXT',
        bytes: 'BLOB', bytearray: 'BLOB', type(None): 'NULL',
    }
    
    if j_type in ('dict_of_list_of_dict', 'dict_of_dict'):

        array_ = next(iter(data.values()), [])
        file_sample = array_[0] if isinstance(array_, list) else next(iter(data.values()))
        id_ = next(iter(data.keys()))
        extracted_types['id'] = types_d.get(type(id_))

    elif j_type in ('list_of_dict'):

        file_sample = next(iter(data))

    else:

        file_sample = data

    for name, type_ in file_sample.items():
        sql_type = types_d.get(type(type_))

        extracted_types[name] = sql_type
        
    return extracted_types


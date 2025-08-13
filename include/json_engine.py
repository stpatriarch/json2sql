#!/usr/bin/env python3

from curses import resetty
import json
import re


class JsonModify:

    def __init__(self, file):
        
        self.file = file
        self.json = self._connect
        
        self.js_struct = self.define_json_struct


    def json_normalize(self):

        if self.js_struct in ('flaten_dict', 'list_of_dicts', 'dict_of_dict', 'dict_of_list_of_dicts'):

            if self.js_struct == 'flaten_dict' or 'list_of_dicts':
                return self.json, self.js_struct
            elif self.js_struct == 'dict_of_dict':
                return self.flatten_dict(self.json)



    def flatten_dict(self, dct, parent_key='', sep='_'):
        item = {}
        
        for key, value in dct.items():
            new_key = f'{parent_key}{sep}{key}' if parent_key else key
            if isinstance(value, dict):
                item.update(self.flatten_dict(value, new_key, sep=sep))
            else:
                item[new_key] = value
        return item



    @property
    def define_json_struct(self)-> str:

        if isinstance(self.json, dict):

            if any(isinstance(v, list) and  all(isinstance(i, dict) for i in v) for v in self.json.values()):
                return 'dict_of_list_of_dicts'
    
            elif any(isinstance(i, dict) for i in self.json.values()):
                return 'dict_of_dict'
    
            elif all(not isinstance(v, (list, dict)) for v in self.json.values()):
                return 'flaten_dict'

        

        if isinstance(self.json, list):
            if all(isinstance(item, dict)for item in self.json):
                return 'list_of_dicts'
        
            elif all(isinstance(item, (str, int, float, bool, type(None))) for item in self.json):
                return 'flaten_list'

        raise ValueError("undef type")


    

    @property
    def _connect(self):
        with open(f"{self.file}", encoding='utf-8') as file:
            data = json.load(file)
        
        return data



if __name__ == '__main__':
    js = JsonModify('base_data.json')
    js._connect
    json_ = js.flatten_dict(js.json)
    print(json_)
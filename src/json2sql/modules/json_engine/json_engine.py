#!/usr/bin/env python3

import json
from json2sql.tools import NotSupportedJsonMixin
from json2sql.modules.json_engine import DctofDct, DctofLstofDcts, LstofDct, ACCEPTABLE_TYPES


class JsonModify(NotSupportedJsonMixin):

    def __init__(self, file):
        
        self.file = file
        self.json = self._connect
        
        self.js_struct = self.define_json_struct

     
    


    def json_normalize(self):

        if self.js_struct in ACCEPTABLE_TYPES:

            if self.js_struct in ('list_of_dicts'):
                return LstofDct(self.json).initialization
            
            elif self.js_struct in ('dict_of_dict'):
                if self.is_branched:
                    return DctofDct(self.json).initialization
                
                return self.json, self.js_struct
            
            elif self.js_struct in ('dict_of_list_of_dicts'):
                
                return DctofLstofDcts(self.json).initialization
        else:
            raise self.unsupported_type(self.js_struct)



    @property
    def is_branched(self) -> bool:
        
        for v in self.json.values():
            if any(isinstance(j, (list, dict)) for j in v.values()):
                return True
        return False
    




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

        raise self.unsupported_type(self.json)


    

    @property
    def _connect(self):
        with open(f"{self.file}", encoding='utf-8') as file:
            data = json.load(file)
        
        return data

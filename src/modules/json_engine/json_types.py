#!/usr/bin/env python3

from collections import defaultdict

class JsonTypeIdentifer:
    
    def __init__(self, json):
        self.json = json
        self.combined_data = defaultdict(list)


    def initialization(self):
        raise NotImplementedError

    def json_standardize(self, dct, parent_key='', sep='_'):

        item = {}
        
        for key, value in dct.items():
            new_key = f'{parent_key}{sep}{key}' if parent_key else key
            
            if isinstance(value, dict):
                item.update(self.json_standardize(value, new_key, sep=sep))
            else:
                item[new_key] = value

        return item
    
    def calibrate(self, input):

        for k, v in input.items():

            if isinstance(v, dict):
                self.calibrate(v)  
            elif isinstance(v, list):
                input[k] = ', '.join(map(str, v))

        return input


class DctofDct(JsonTypeIdentifer):


    @property  
    def initialization(self):

        if self.is_branched:
            return self.json_standardize(self.calibrate(self.json)), 'dict_of_dict_branched'
        
        return self.json, 'dict_of_dict'
    
    @property
    def is_branched(self) -> bool:

        for v in self.json.values():
            if any(isinstance(j, (list, dict)) for j in v.values()):
                return True
        return False
        

class DctofLstofDcts(JsonTypeIdentifer):
    
    
    def json_standardize(self, dct, parent_key='', sep='_'):

        item = {}

        for key, value in dct.items():
            new_key = f'{parent_key}{sep}{key}' if parent_key else key
            
            if isinstance(value, list):
                for i in value:
                    for key, value in i.items():
                        self.combined_data[key].append(value)
                item.update(self.combined_data)     
            else:
                item[new_key] = value
        
        return self.calibrate(item)

    @property
    def initialization(self):
        
        value_type = next(iter(self.json.values()))
        
        if isinstance(value_type,(list, dict)):
            return self.json, 'dict_of_list_of_dict'
        return self.json_standardize(self.json), 'dict_of_list_of_dicts'


class LstofDct(JsonTypeIdentifer):

    @property
    def initialization(self):

        return self.json, 'list_of_dict'

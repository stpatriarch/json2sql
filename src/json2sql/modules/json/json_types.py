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

    @property
    def is_branched(self) -> bool:
        if isinstance(self.json, dict):

            for v in self.json.values():
                if any(isinstance(j, (list, dict)) for j in v.values()):
                    return True
            return False

        if isinstance(self.json, list):
            for item in self.json:
                if any(isinstance(v, (list, dict)) for v in item.values()):
                        return True
                return False
                
class DctofDct(JsonTypeIdentifer):


    @property  
    def initialization(self):

        if self.is_branched:
            return self.json_standardize(self.calibrate(self.json)), 'dict_of_dict_branched'
        
        return self.json, 'dict_of_dict'
    

        

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

    def json_standardize(self, dct, parent_key = '', sep = '_'):

        item = {}
        
        for i in dct:
            for key, value in i.items():
                new_key = f'{parent_key}{sep}{key}' if parent_key else key
            
                if isinstance(value, list):
                    item.update(self.json_standardize(value, new_key, sep=sep))
                
                elif isinstance(value, dict):
                    item.update(super().json_standardize(value, new_key, sep=sep))
                else:
                    self.combined_data[new_key].append(value,)
        print(item)
        return {k: tuple(v) for k, v in self.combined_data.items()}


    @property
    def initialization(self) -> tuple:
        if self.is_branched:
            return self.json_standardize(self.json), 'list_of_dict_branched'

        return self.json, 'list_of_dict'

#!/usr/bin/env python3

from collections import defaultdict
from abc import ABC, abstractmethod


class JsonTypeProcessor(ABC):
    """
    The class processes internal conditional JSON types and
    performs standartization and initialization.
    """
    
    def __init__(self, json: dict) -> None:
        """
        Initialize JSON data for standardization.

        :param json: JSON data to be standardized.
        :type json: dict 
        """
        
        self.json = json
        self.combined_data = defaultdict(list)

    
    def calibrate(self, input_: dict) -> dict:
        """
        Recursively process branched JSON data by
        converting list values into comma-separated strings.
        
        :param input_: Dictionary to be calibaration.
        :type input_: dict
        :return: Calibrated Dictionary.
        """

        for k, v in input_.items():

            if isinstance(v, dict):
                self.calibrate(v)  
            elif isinstance(v, list):
                input_[k] = ', '.join(map(str, v))

        return input_

    @property
    def is_branched(self) -> bool:
        """
        Check whether the JSON structure is branched.

        :return: 'True' if the JSON is branched, otherwise 'False'.
        """

        for v in self.json.values():
            if any(isinstance(j, (list, dict)) for j in v.values()):
                return True
        return False


    @property
    @abstractmethod
    def initialization(self) -> tuple: 
        """
        initialize and normalize JSON data based on its structure.
        """
        pass

class DictofDict(JsonTypeProcessor):
    """
    Perform standardization and initialization
    for ``dict_of_dict`` structures, including branched variants.
    """

    def json_standardize(self, dct: dict, parent_key: str='', sep: str='_') -> dict:
        """
        Recursively flatten a nested JSON dictionary by 
        concatenating keys.

        :param dct: Dictionary to be standardized.
        :type dct: dict
        :param parent_key: Prefix for nested keys.
        :type parent_key: str
        :param sep: Key separator.
        :type sep: str
        :return: Flatten Dictionary.
        """

        item = {}
        
        for key, value in dct.items():
            new_key = f'{parent_key}{sep}{key}' if parent_key else key
            
            if isinstance(value, dict):
                item.update(self.json_standardize(value, new_key, sep=sep))
            else:
                item[new_key] = value

        return item

    @property  
    def initialization(self) -> tuple:
        """
        initialize and normalize JSON data based on its structure.

        :return: Standardized dictionary and its internal conditional type.
        """

        if self.is_branched:
            return self.json_standardize(self.calibrate(self.json)), 'dict_of_dict_branched'
        
        return self.json, 'dict_of_dict'
        

class DictofListofDict(JsonTypeProcessor): 
    """
    Perform standardization and initialization
    for ``dict_of_list_of_dict`` structures, including branched variants.
    """
    
    def json_standardize(self, dct: dict, parent_key: str='', sep: str='_') -> dict:
        """
        Recursively flatten a nested json dictionary by 
        concatenating keys.

        :param dct: Dictionary to be standardized.
        :type dct: dict
        :param parent_key: Prefix for nested keys.
        :type parent_key: str
        :param sep: Key separator.
        :type sep: str
        :return: Flatten Dictionary.
        """

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
    def initialization(self) -> tuple: 
        """
        initialize and normalize JSON data based on its structure.

        :return: Standardized dictionary and its internal conditional type.
        """

        value_type = next(iter(self.json.values()))
        
        if isinstance(value_type,(list, dict)):

            return self.json, 'dict_of_list_of_dict'

        return self.json_standardize(self.json), 'dict_of_list_of_dict_branched'

class ListofDict(JsonTypeProcessor):
    """
    Perform standardization and initialization
    for ``list_of_dict`` structures, including branched variants.
    """

    @property
    def initialization(self) -> tuple:
        """
        initialize and normalize JSON data based on its structure.

        :return: Standardized dictionary and its internal conditional type.
        """

        return self.json, 'list_of_dict'

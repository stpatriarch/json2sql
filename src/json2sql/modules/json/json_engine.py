#!/usr/bin/env python3

import json
from pathlib import Path

from json2sql.tools import NotSupportedMixin
from .json_types import DictofDict, DictofListofDict, ListofDict


ACCEPTABLE_TYPES = ('list_of_dict', 
                    'dict_of_dict', 
                    'dict_of_list_of_dict')


class JsonModCore(NotSupportedMixin):
    """
    Class manages all operations related to the JSON file. 
    """

    def __init__(self, path: str) -> None:
        """
        Initialize a JSON file path.

        :param file: Path to the JSON file.
        :type file: str
        """
        super().__init__()
        self._path = path

    @property
    def _json(self):
        return self._connect(self._path)

    @property
    def js_define(self):
        return self.define_json_struct(self._json)

    def json_normalize(self) -> tuple | None:
        """
        Detect the JSON structure type and normalize it using the appropriate
        transformation class.

        :return: Normalized JSON data and its structure type, or ``None``.
        """
        js_struct = self.js_define

        match js_struct:

            case 'list_of_dict':
                return ListofDict(self._json).initialization 

            case 'dict_of_dict':
                return DictofDict(self._json).initialization

            case 'dict_of_list_of_dict':
                return DictofListofDict(self._json).initialization
    


    def define_json_struct(self, data: dict | list) -> str:
        """
        Determine the JSON structure type and return its conditional name.

        :return: Conditional name of the detected JSON structure.
        :raises unsupported_type: If the JSON structure type is not supported.
        """


        if isinstance(data, dict):

            if any(isinstance(v, list) and  all(isinstance(i, dict) for i in v) for v in data.values()):
                return 'dict_of_list_of_dict'
    
            elif any(isinstance(i, dict) for i in data.values()):
                return 'dict_of_dict'
    
            elif all(not isinstance(v, (list, dict)) for v in data.values()):
                return 'flaten_dict'
 

        if isinstance(data, list):
            if all(isinstance(item, dict) for item in data):
                return 'list_of_dict'

        raise self.unsupported_type(type(data).__name__)



    def _connect(self, path) -> dict:
        """
        Load a non-empty JSON file and return its content.

        :return: Parses JSON data as a dictionary.
        :raises FileNotFoundError: If the file does not exist.
        :raises ValueError: If the JSON file is invalid or empty.
        """
        file_path = Path(path)

        if not file_path.is_file():
            self.warn_message.print(f"File not found: {path}")
            raise FileNotFoundError(f"File not found: {path}")

        try:
            content = file_path.read_text(encoding='utf-8').strip()
            if not content:
                self.warn_message.print("JSON file is empty")
                raise ValueError("JSON file is empty")
            return json.loads(content)
        
        except json.JSONDecodeError as er:
            self.warn_message.print(f"\n JSON file is invalid: {er}\U0000274E \n")
            raise ValueError(f"\n JSON file is invalid: {er}\U0000274E \n") from er

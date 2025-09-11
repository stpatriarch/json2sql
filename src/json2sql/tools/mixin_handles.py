#!/usr/bin/env python3

class FileError(Exception):
    pass

class NotSupportedJsonMixin:
    def unsupported_type(self, type) -> None:
        
        if not isinstance(type, str):
            raise FileError(f'Unsupported data type -> {type.__class__}')
        raise FileError(f'Unsupported file type -> {type}')
    

    def empty_json_handle(self) -> None:
        raise FileError('Json file is empty')
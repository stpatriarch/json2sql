  #!/usr/bin/env python3

from typing import NoReturn
from rich.console import Console


class FileError(Exception):
    """
    Raised when an unsupported or invalid file type is encountered.
    """
    pass


class EngineError(Exception):
    """
    Raised when an unsupported database engine is requested.
    """
    pass


class NotSupportedMixin:
    """
    Mixin that provides helpers for raising standardized
    unsupported-type and unsupported-engine errors.
    """
    def __init__(self) -> None:

        self.warn_message = Console(style='red bold')


    def unsupported_type(self, data_type) -> NoReturn:
        """
        Raise an error for unsupported JSON or file structure types.

        :param data_type: Internal conditional type or file type identifier.
        :type data_type: str
        :raises FileError: Always raised for unsupported types.
        """
        if not isinstance(data_type, str):

            self.warn_message.print(f'Unsupported data type -> {data_type.__class__}')
            raise FileError(f'Unsupported data type -> {data_type.__class__}')
        
        self.warn_message.print(f'Unsupported file type -> {data_type}')
        raise FileError(f'Unsupported file type -> {data_type}')
    
    
    def unsupported_engine(self, engine) -> NoReturn:
        """
        Raise an error for unsupported database engines.

        :param engine: Engine name.
        :type engine: str
        :raises EngineError: Always raised for unsupported engines.
        """
        self.warn_message.print(f'Unsupported engine -> {engine}')
        raise EngineError(f'Unsupported engine -> {engine}')


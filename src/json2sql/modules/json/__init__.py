#!/usr/bin/env python3

from .json_types import DctofDct, DctofLstofDcts, LstofDct

ACCEPTABLE_TYPES = ('list_of_dicts', 
                    'dict_of_dict', 
                    'dict_of_list_of_dicts')

__all__ = ['DctofDct', 'DctofLstofDcts', 'LstofDct', 'ACCAPTABLE_TYPES']
import pytest
from json2sql.modules.json.json_types import DictofDict, ListofDict, DictofListofDict

@pytest.fixture
def list_of_dict():
    return [
            {"k_1": 1, "k_2": "v_1"},
            {"k_3": 1, "k_4": "v_1"}
            ]


@pytest.fixture
def dict_of_dict():
   return {
           "k_1": {
               "k_1_1": 21, "k_1_2": 40},
           
           "k_2": {
               "k_2_1": 21, "k_2_2": 40},
           }

@pytest.fixture
def dict_of_dict_branched():
   return {
           "k_1": {
               "k_1_1": 21, "k_1_2": 40,
               "k_1_3": {
                   "k_3_1": 21, "k_3_2": 40}
               },
           
           "k_2": ['value_0', 'value_1']


           }



@pytest.fixture
def dict_of_list_of_dict():

    return {
            "key_0": [
                {"key_0_1": "val_1", "key_0_2": 600}, 
                {"key_1_1": "val_1", "key_1_2": 600}
                ],
            
            "key_1": [
                {"key_1_1": "val_1", "key_1_2": 600}
                ]
            }



def test_dict_of_dict_initialization(dict_of_dict):
    process = DictofDict(dict_of_dict)
    result = process.initialization
    normalized_json, json_type = result

    assert isinstance(result, tuple)
    assert json_type == 'dict_of_dict'
    assert normalized_json == dict_of_dict


def test_dict_of_dict_brached_initialization(dict_of_dict_branched):
    process = DictofDict(dict_of_dict_branched)
    result = process.initialization
    normalized_json, json_type = result

    assert isinstance(result, tuple)
    assert json_type == 'dict_of_dict_branched'
    assert normalized_json == {'k_1_k_1_1': 21, 
                               'k_1_k_1_2': 40, 
                               'k_1_k_1_3_k_3_1': 21, 
                               'k_1_k_1_3_k_3_2': 40, 
                               'k_2': 'value_0, value_1'
                               }
    


def test_list_of_dict_initialization(list_of_dict):
    process = ListofDict(list_of_dict)
    result = process.initialization
    normalized_json, json_type = result


    assert isinstance(result, tuple)
    assert json_type == 'list_of_dict'
    assert normalized_json == list_of_dict 


def test_dict_of_list_of_dict_initialization(dict_of_list_of_dict):
    process = DictofListofDict(dict_of_list_of_dict)
    result = process.initialization
    normalized_json, json_type = result


    assert isinstance(result, tuple)
    assert json_type == 'dict_of_list_of_dict'
    assert normalized_json == dict_of_list_of_dict 


def test_dict_of_dict_calibrate(dict_of_dict_branched):
    process = DictofDict(dict_of_dict_branched)

    result = process.calibrate(dict_of_dict_branched)
    
    assert isinstance(result, dict)
    assert result == {
            'k_1': {
                'k_1_1': 21, 'k_1_2': 40, 'k_1_3': {
                    'k_3_1': 21, 'k_3_2': 40}}, 
            'k_2': 'value_0, value_1'
            }


def test_is_branched_returns_false(dict_of_dict):

    process = DictofDict(dict_of_dict)
    
    result = process.is_branched

    assert isinstance(result, bool)
    assert not result

def test_is_branched_returns_true(dict_of_dict_branched):

    process = DictofDict(dict_of_dict_branched)
    
    result = process.is_branched

    assert isinstance(result, bool)
    assert result


def test_dict_of_dict_json_standartize(dict_of_dict):
    flat_dict = {"k_1": 1, "k_2": "v_1"} 

    process = DictofDict(dict_of_dict)
    result_0 = process.json_standardize(dct=dict_of_dict)
    result_1 = process.json_standardize(dct=flat_dict)
   
    assert result_0 == {'k_1_k_1_1': 21, 
                        'k_1_k_1_2': 40, 
                        'k_2_k_2_1': 21, 
                        'k_2_k_2_2': 40}

    assert result_1 == flat_dict

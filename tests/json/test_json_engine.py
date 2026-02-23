import pytest
from json2sql.modules.json.json_engine import JsonModCore

@pytest.fixture
def json_core(tmp_path):
    def _core_factory(content: str):
        file = tmp_path / 'test.json'
        file.write_text(content)
        return JsonModCore(str(file))
    return _core_factory


def test_define_json_struct(json_core):
    json_types = {
            '{"4850001006466": [{"key_1": "val_1", "key_2": 600, "key_3": 0.91}]}': 'dict_of_list_of_dicts',
            '{"k_1": {"k_1_1": 21, "k_1_2": 40}, "k_2": {"k_2_1": 22, "k_2_2": 38}}': 'dict_of_dict',
            '{"k_1": 123,"k_2": [{"k_2_1": "v_2_1", "k_2_2": 2},{"k_2_3": "v_2_3", "k_2_4": 1}]}': 'dict_of_list_of_dicts',
            '[{"k_1": 1, "k_2": "v_1", "k_3": "v_2", "k_4": 30, "k_5": true}]': 'list_of_dicts' 
            }



def test_json_normalize(json_core):

    json_types = {
            '{"key": [{"key_1": "val_1", "key_2": 600}]}': 'dict_of_list_of_dict',
            '{"k_1": 123,"k_2": [{"k_2_1": "v_2_1", "k_2_2": 2}]}': 'dict_of_list_of_dict_branched',
            '{"k_1": {"k_1_1": 21, "k_1_2": 40}}': 'dict_of_dict',
            '[{"k_1": 1, "k_2": "v_1"}]': 'list_of_dict' 
            }

    for js, expacted in json_types.items():
        core = json_core(js)
        result = core.json_normalize()
        print(result)

        assert result[1] == expacted






import pytest
import json
from pathlib import Path
from json2sql.tools.mixin_handles import FileError
from json2sql.modules.json.json_engine import JsonModCore


@pytest.fixture
def json_core(tmp_path):
    def _core_factory(content: str):
        file = tmp_path / 'test.json'
        file.write_text(content)
        return JsonModCore(str(file))
    return _core_factory


def test_json_normalize_DictofDict(json_core, monkeypatch):
    
    class MockDictofDict:

        def __init__(self, _) -> None:
            pass

        @property
        def initialization(self):
            return ('dict_of_dict',)

    monkeypatch.setattr('json2sql.modules.json.json_engine.DictofDict', MockDictofDict) 

    core = json_core('{"k_1": {"k_1_1": 21, "k_1_2": 40}}')

    result = core.json_normalize()

    assert result == ('dict_of_dict',)


def test_json_normalize_ListofDict(json_core, monkeypatch):
    
    class MockListofDict:

        def __init__(self, _) -> None:
            pass

        @property
        def initialization(self):
            return ('list_of_dict',)

    monkeypatch.setattr('json2sql.modules.json.json_engine.ListofDict', MockListofDict) 

    core = json_core('[{"k_1": 1, "k_2": "v_1"}]')

    result = core.json_normalize()

    assert result == ('list_of_dict',)


def test_json_normalize_DictofListofDict(json_core, monkeypatch):
    
    class MockDictofListofDict:

        def __init__(self, _) -> None:
            pass

        @property
        def initialization(self):
            return ('dict_of_list_of_dict',)

    monkeypatch.setattr('json2sql.modules.json.json_engine.DictofListofDict', MockDictofListofDict) 

    core = json_core('{"key": [{"key_1": "val_1", "key_2": 600}]}')

    result = core.json_normalize()

    assert result == ('dict_of_list_of_dict',)



def test_define_json_struct(json_core):

    json_types = {
            '{"key": [{"key_1": "val_1", "key_2": 600}]}': 'dict_of_list_of_dict',
            '{"k_1": 123,"k_2": "val_2", "k_2_1": "v_2_1", "k_2_2": 2}': 'flaten_dict',
            '{"k_1": {"k_1_1": 21, "k_1_2": 40}}': 'dict_of_dict',
            '[{"k_1": 1, "k_2": "v_1"}]': 'list_of_dict' 
            }

    
    for js, expacted in json_types.items():
        core = json_core(js)
        data = json.loads(js)
        result = core.define_json_struct(data)

        assert expacted == result

def test_define_json_struct_unsupported_exception(json_core, monkeypatch):

    calls = []

    core = json_core('{"key": [{"key_1": "val_1", "key_2": 600}]}')

    data = [1, 2, 3, 4, 5]

    def unsupported_call(type_):
        calls.append(type_)
        raise FileError(type_)   

    monkeypatch.setattr(core, 'unsupported_type', unsupported_call)

    with pytest.raises(FileError):
        
        core.define_json_struct(data)

    assert calls == ['list']
 

def test__connect_file_not_found_exeption(json_core, monkeypatch):
    calls = []
    mock_path = 'path_to_file'

    core = json_core('{"key": [{"key_1": "val_1", "key_2": 600}]}')

    monkeypatch.setattr(core.warn_message, 'print', lambda msg: calls.append(('print', msg)))
    monkeypatch.setattr(Path, "is_file", lambda _: False) 

    with pytest.raises(FileNotFoundError):
        core._connect(path=mock_path)
    
    assert calls == [('print', 'File not found: path_to_file')]


def test__connect_empty_json_exeption(json_core, monkeypatch):
    calls = []
    mock_path = 'path_to_file'

    core = json_core('{}')

    monkeypatch.setattr(core.warn_message, 'print', lambda msg: calls.append(('print', msg)))
    monkeypatch.setattr(Path, "is_file", lambda _: True) 
    monkeypatch.setattr(Path, "read_text", lambda *_, **__: " ")

    with pytest.raises(ValueError):
        core._connect(path=mock_path)

    assert calls == [('print', 'JSON file is empty')]


def test__connect_valid_json(json_core, monkeypatch):

    mock_path = 'path_to_file'

    core = json_core('{}')

    monkeypatch.setattr(Path, "is_file", lambda _: True) 
    
    monkeypatch.setattr(Path, "read_text", lambda *_, **__: '{"key": [{"key_1": "val_1", "key_2": 600}]}')
    
    result = core._connect(path=mock_path)
    assert result == {'key': [{'key_1': 'val_1', 'key_2': 600}]}


def test__connect_invalid_json(json_core, monkeypatch):
    calls = []

    mock_path = 'path_to_file'

    core = json_core('{}')

    monkeypatch.setattr(Path, "is_file", lambda _: True) 

    monkeypatch.setattr(Path, "read_text", lambda *_, **__: '{invalid_json}')
    monkeypatch.setattr(core.warn_message, 'print', lambda msg: calls.append(('print', msg)))

    with pytest.raises(ValueError) as exc:
        core._connect(mock_path)

    assert "JSON file is invalid" in calls[0][1]
    assert "JSON file is invalid" in str(exc.value)
    

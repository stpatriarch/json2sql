import json
import pytest
from unittest.mock import MagicMock
from json2sql.modules.sql.sql_data_types import SqlEngineAcceptType
from json2sql.tools.mixin_handles import EngineError


@pytest.fixture
def sql_engine():
    def engine_factory(engine):
        return SqlEngineAcceptType(engine=engine)
    yield engine_factory


@pytest.fixture
def type_data():
    def type_factory(engine_type):

        types_idents = {
                'dict_of_list_of_dict': '{"key": [{"key_1": 600, "key_2": true, "key_3": 3.1, "key_4": null}]}',
                'dict_of_dict': '{"k_1": {"key_1": 600, "key_2": true, "key_3": 3.1, "key_4": null}}',
                'list_of_dict': '[{"key_1": "val_1", "key_2": true, "key_3": 3.1, "key_4": null, "key_5": 600}]' 
            }
        
        engine = SqlEngineAcceptType(engine=engine_type)


        for ident, data in types_idents.items():
            yield ident, engine.define_types(json=json.loads(data), ident=ident)
    return type_factory

def test_unsupported_engine(sql_engine, monkeypatch):
    warn_mock = MagicMock()

    monkeypatch.setattr("json2sql.tools.mixin_handles.Console", lambda **kwargs: warn_mock)

    with pytest.raises(EngineError) as exc:
        sql_engine('MongoDB')

    warn_mock.print.assert_called_once_with("Unsupported engine -> MongoDB")
    assert "Unsupported engine -> MongoDB" in str(exc.value)


def test_sqlite_type_indentification(type_data):
    expected = {
            'dict_of_list_of_dict': {'id': 'TEXT', 'key_1': 'INTEGER', 'key_2': 'INTEGER', 'key_3': 'REAL', 'key_4': 'NULL'},
            'dict_of_dict': {'id': 'TEXT', 'key_1': 'INTEGER', 'key_2': 'INTEGER', 'key_3': 'REAL', 'key_4': 'NULL'},
            'list_of_dict': {'key_1': 'TEXT', 'key_2': 'INTEGER', 'key_3': 'REAL', 'key_4': 'NULL', 'key_5': 'INTEGER'}
            }
    for ident, result in type_data('sqlite'):

        assert result == expected[ident]


def test_postgres_type_indentification(type_data):
    expected = {
            'dict_of_list_of_dict': {'id': 'TEXT', 'key_1': 'INTEGER', 'key_2': 'BOOLEAN', 'key_3': 'REAL', 'key_4': 'NULL'},
            'dict_of_dict': {'id': 'TEXT', 'key_1': 'INTEGER', 'key_2': 'BOOLEAN', 'key_3': 'REAL', 'key_4': 'NULL'},
            'list_of_dict': {'key_1': 'TEXT', 'key_2': 'BOOLEAN', 'key_3': 'REAL', 'key_4': 'NULL', 'key_5': 'INTEGER'}
            }
    for ident, result in type_data('postgresql'):

        assert result == expected[ident]

def test_mysql_type_indentification(type_data):
    expected = {
            'dict_of_list_of_dict': {'id': 'TEXT', 'key_1': 'INT', 'key_2': 'TINYINT(1)', 'key_3': 'DOUBLE', 'key_4': 'NULL'},
            'dict_of_dict': {'id': 'TEXT', 'key_1': 'INT', 'key_2': 'TINYINT(1)', 'key_3': 'DOUBLE', 'key_4': 'NULL'},
            'list_of_dict': {'key_1': 'TEXT', 'key_2': 'TINYINT(1)', 'key_3': 'DOUBLE', 'key_4': 'NULL', 'key_5': 'INT'}
            }
    for ident, result in type_data('mysql'):

        assert result == expected[ident]


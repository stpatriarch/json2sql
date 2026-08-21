import argparse
import pytest
from unittest.mock import patch
from json2sql.modules.sql.engine_factory import EngineFactory 
from json2sql.modules.sql.sql_engine import SqliteEngine


@pytest.fixture
def engine_factory():
    def _factory(args):

        data_struct = ({"item": [{"key_1": "val_1", "key_2": 600}]}, 'dict_of_list_of_dict')

        return EngineFactory(input_file=data_struct, args=args)
    return _factory


def tests_factory_for_sqlite(engine_factory):

    args = argparse.Namespace(engine="sqlite", input='file.json', table='table_name')
    
    factory = engine_factory(args)

    engine_instanse = factory.create()
    
    assert isinstance(engine_instanse, SqliteEngine)

def test_factory_for_postgres(engine_factory):

    args = argparse.Namespace(
            engine="postgres",
            host="localhost",
            user="postgres",
            password="secret",
            name="database_name",
            table="table_name",
            port=5432,
            )

    
    with patch("json2sql.modules.sql.engine_factory.PostgresEngine") as postgres_mock:
        
        factory = engine_factory(args)

        engine_instanse = factory.create()
    
        postgres_mock.assert_called_once_with(
                js_file=factory.input_file, 
                host="localhost",
                user="postgres",
                password="secret",
                dbname="database_name",
                table="table_name",
                port=5432
                )

        assert engine_instanse == postgres_mock.return_value


def test_factory_for_mysql(engine_factory):

    args = argparse.Namespace(
            engine="mysql",
            host="localhost",
            user="mysql",
            password="secret",
            name="database_name",
            table="table_name",
            port=3306
            )

    
    with patch("json2sql.modules.sql.engine_factory.MysqlEngine") as mysql_mock:
        
        factory = engine_factory(args)

        engine_instanse = factory.create()
    
        mysql_mock.assert_called_once_with(
                js_file=factory.input_file, 
                host="localhost",
                user="mysql",
                password="secret",
                dbname="database_name",
                table="table_name",
                port=3306
                )
        
        assert engine_instanse == mysql_mock.return_value


def test_not_supported_engine(engine_factory):

    args = argparse.Namespace(engine="MongoDB", input='file.json', table='table_name')
    
    factory = engine_factory(args)

    engine_instanse = factory.create()
    assert engine_instanse is None


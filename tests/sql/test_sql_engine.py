import pytest
from unittest.mock import MagicMock, patch
import sqlite3
from json2sql.modules.sql.sql_engine import MysqlEngine, PostgresEngine, SqlEngine, SqliteEngine


@pytest.fixture
def mock_engine():

    class MockEngine(SqlEngine):

        def __init__(self, js_file: tuple, table: str='test_table') -> None:

            super().__init__('sqlite', js_file, table=table)
            
            self.values = []
            self.executed = [] 

            
        def connection(self, content, values=None):

            self.executed.append((content, values))
            return content
        
    return MockEngine


@pytest.fixture
def sqlite_engine(tmp_path):

    tmp_file = tmp_path / 'test.db'

    js_data = ({"item": [{"key_1": "val_1", "key_2": 600}]}, 'dict_of_list_of_dict')

    engine = SqliteEngine(js_file=js_data, dbname=str(tmp_file), table='test_table')
    
    yield engine



@pytest.fixture
def postgres_engine_mock():
    with patch("json2sql.modules.sql.sql_engine.psycopg.connect") as mock_connect:

        mock_cursor = MagicMock()
        mock_connection = MagicMock()

        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
        mock_connect.return_value = mock_connection

        js_data = ({"item": [{"key_1": "val_1", "key_2": 600}]}, 'dict_of_list_of_dict')

        engine = PostgresEngine(
            js_file=js_data,
            host="localhost",
            user="postgres",
            password="secret",
            dbname="test_db",
            table="test_table",
            port=5432)
    
        yield engine, mock_cursor, mock_connection, mock_connect


json_types = {
            '{"key": [{"key_1": "val_1", "key_2": 600}]}': 'dict_of_list_of_dict',
            '{"k_1": 123,"k_2": "val_2", "k_2_1": "v_2_1", "k_2_2": 2}': 'flaten_dict',
            '{"k_1": {"k_1_1": 21, "k_1_2": 40}}': 'dict_of_dict',
            '[{"k_1": 1, "k_2": "v_1"}]': 'list_of_dict' 
            }


@pytest.fixture
def mysql_engine_mock():
    with patch("json2sql.modules.sql.sql_engine.pymysql.connect") as mock_connect:

        mock_cursor = MagicMock()
        mock_connection = MagicMock()

        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
        mock_connect.return_value = mock_connection

        js_data = ({"item": [{"key_1": "val_1", "key_2": 600}]}, 'dict_of_list_of_dict')

        engine = MysqlEngine(
            js_file=js_data,
            host="localhost",
            user="mysql",
            password="secret",
            dbname="test_db",
            table="test_table",
            port=3306)
    
        yield engine, mock_cursor, mock_connection, mock_connect

def test_create_sql_generation(mock_engine):
    
    js_data = ({"key_1": {"key_1_1": 21, "key_1_2": 40}}, 'dict_of_dict')
    
    engine = mock_engine(js_data)

    engine.create()
    query = engine.executed[0][0]

    assert 'CREATE TABLE IF NOT EXISTS test_table' in query 
    assert 'key_1_2' in query
    assert 'key_1_1' in query


def test_prepare_json_by_group_for_dict_of_dict(mock_engine):

    js_data = ({"key_1": {"key_1_1": 21, "key_1_2": 40}}, 'dict_of_dict')
    
    engine = mock_engine(js_data)

    preparated = engine.prepare_json_by_group

    assert isinstance(preparated, tuple)
    assert preparated == ('id', 'key_1_1', 'key_1_2')



def test_prepare_json_by_group_for_dict_of_list_of_dict(mock_engine):

    js_data = ({"item": [{"key_1": "val_1", "key_2": 600}]}, 'dict_of_list_of_dict')
    
    engine = mock_engine(js_data)

    preparated = engine.prepare_json_by_group

    assert isinstance(preparated, tuple)
    assert preparated == ('id', 'key_1', 'key_2')


def test_prepare_json_by_group_for_list_of_dict(mock_engine):

    js_data = ([{"key_1": 1, "key_2": "val_1"}], 'list_of_dict')
    
    engine = mock_engine(js_data)

    preparated = engine.prepare_json_by_group

    assert isinstance(preparated, list)
    assert preparated == ['key_1', 'key_2']


def test_prepare_json_by_group_for_flaten_dict(mock_engine):

    js_data = ({"key_1": 123,"key_2": "val_2", "key_2_1": "val_2_1", "key_2_2": 2}, 'flaten_dict')
    
    engine = mock_engine(js_data)

    preparated = engine.prepare_json_by_group

    assert isinstance(preparated, list)
    assert preparated == ['key_1', 'key_2', 'key_2_1', 'key_2_2']


def test_data_insertation_process(mock_engine):

    js_data = ({"item": [{"key_1": "val_1", "key_2": 600}]}, 'dict_of_list_of_dict')

    engine = mock_engine(js_data)

    engine.insert()
        
    query, values = engine.executed[1]

    assert 'INSERT INTO test_table' in query
    assert '(id, key_1, key_2) VALUES (?, ?, ?)' in query
    assert ('item', 'val_1', 600) == values

 
def test_sqlite_closed_connection(sqlite_engine, monkeypatch):

    engine = sqlite_engine

    monkeypatch.setattr(engine, 'open_', lambda: None)
    
    with pytest.raises(RuntimeError) as excinfo:

       engine.connection('SELECT * FROM test_table')
       
    assert 'Database connection was not established' in str(excinfo.value)

    
def test_sqlite_connection(sqlite_engine):
    
    engine = sqlite_engine

    engine.insert()

    cur = engine.connection('SELECT * FROM test_table')
    result = cur.fetchall()

    assert len(result) == 1
    assert result[0]['id'] == 'item'
    assert result[0]['key_1'] == 'val_1'
    assert result[0]['key_2'] == 600

def test_sqlite_connection_open_(sqlite_engine):

    engine = sqlite_engine

    assert engine.connect is None
    engine.open_()
    assert engine.connect is not None
    assert isinstance(engine.connect, sqlite3.Connection)

    
def test_postgres_connection(postgres_engine_mock):
    
    engine, mock_cursor, mock_connection, _= postgres_engine_mock

    engine.connection(
            "INSERT INTO test_table (id, key_1, key_2) VALUES (%s, %s, %s)",
            ["item", "val_1", 600]
            )
    
    mock_cursor.execute.assert_called_once_with(
            "INSERT INTO test_table (id, key_1, key_2) VALUES (%s, %s, %s)",
            ["item", "val_1", 600]
            )
    
    mock_connection.commit.assert_called_once()
    assert engine.connect is mock_connection

def test_postgres_closed_connection_exeption(postgres_engine_mock, monkeypatch):

    engine, *_ = postgres_engine_mock

    engine.connect = None

    monkeypatch.setattr(engine, "open_", lambda: None)
   

    with pytest.raises(RuntimeError) as exc:
        engine.connection(
            "INSERT INTO test_table (id, key_1, key_2) VALUES (%s, %s, %s)",
            ["item", "val_1", 600]
            )

    assert 'Database connection was not established' in str(exc.value)


def test_postgres_connection_opening(postgres_engine_mock):

    engine, _, mock_connection, _, = postgres_engine_mock

    assert engine.connect is None

    engine.open_()

    assert engine.connect is mock_connection



def test_mysql_connection(mysql_engine_mock):
    
    engine, mock_cursor, mock_connection, _= mysql_engine_mock 

    engine.connection(
            "INSERT INTO test_table (id, key_1, key_2) VALUES (%s, %s, %s)",
            ["item", "val_1", 600]
            )
    
    mock_cursor.execute.assert_called_once_with(
            "INSERT INTO test_table (id, key_1, key_2) VALUES (%s, %s, %s)",
            ["item", "val_1", 600]
            )
    
    mock_connection.commit.assert_called_once()
    assert engine.connect is mock_connection
    
    
def test_mysql_closed_connection_exeption(mysql_engine_mock, monkeypatch):

    engine, *_ = mysql_engine_mock

    engine.connect = None

    monkeypatch.setattr(engine, "open_", lambda: None)
   

    with pytest.raises(RuntimeError) as exc:
        engine.connection(
            "INSERT INTO test_table (id, key_1, key_2) VALUES (%s, %s, %s)",
            ["item", "val_1", 600]
            )

    assert 'Database connection was not established' in str(exc.value)


def test_mysql_connection_opening(mysql_engine_mock):

    engine, _, mock_connection, _, = mysql_engine_mock

    assert engine.connect is None

    engine.open_()

    assert engine.connect is mock_connection

import argparse
import pytest
from json2sql.tools import create_parser, is_json


def test_is_json_json():
    
    instance = is_json('file.json')

    assert instance == 'file.json'


def test_is_json_not_json():

    with pytest.raises(argparse.ArgumentTypeError) as error:

        is_json('file.txt')
       
    assert 'Ֆայլը պետք է լինի json | File must be a json' == str(error.value)


@pytest.mark.parametrize('engine', ['sqlite', 'postgres', 'mysql'])
def test_supported_engine_parsers(engine):

    parser = create_parser()

    args = parser.parse_args([
        engine,
        '--input', 'file.json',
        '--table', 'users'
        ])
    
    assert args.engine == engine
    assert args.input == 'file.json'
    assert args.table == 'users'

def test_postgres_parser_defaults():


    parser = create_parser()

    args = parser.parse_args([
        'postgres',
        '--input', 'file.json',
        '--table', 'users'
        ])

    assert args.host == 'localhost'
    assert args.user == 'postgres'
    assert args.password == 'postgres'
    assert args.port == 5432
    assert args.name == 'postgres'


def test_mysql_parser_defaults():


    parser = create_parser()

    args = parser.parse_args([
        'mysql',
        '--input', 'file.json',
        '--table', 'users'
        ])

    assert args.host == 'localhost'
    assert args.user == 'root'
    assert args.password == 'rootroot'
    assert args.port == 3306
    assert args.name == 'mysql'


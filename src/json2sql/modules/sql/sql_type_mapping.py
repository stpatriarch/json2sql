SQL_TYPES = {
    "sqlite": {
        int: 'INTEGER',
        bool: 'INTEGER',
        float: 'REAL',
        str: 'TEXT',
        bytes: 'BLOB',
        bytearray: 'BLOB',
        type(None): 'NULL',
    },
    "postgresql": {
        int: 'INTEGER',
        bool: 'BOOLEAN',
        float: 'REAL',
        str: 'TEXT',
        bytes: 'BYTEA',
        bytearray: 'BYTEA',
        type(None): 'NULL',
    },
    "mysql": {
        int: 'INT',
        bool: 'TINYINT(1)',
        float: 'DOUBLE',
        str: 'TEXT',
        bytes: 'BLOB',
        bytearray: 'BLOB',
        type(None): 'NULL',
    }
}

PLACEHOLDERS = {
    'sqlite': '?',
    ('postgresql', 'mysql'): '%s',
}

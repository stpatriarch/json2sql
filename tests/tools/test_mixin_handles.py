import pytest
from json2sql.tools.mixin_handles import EngineError, FileError, NotSupportedMixin


@pytest.fixture
def mixin():
    return NotSupportedMixin()


def test_unsuppored_data_type(mixin, monkeypatch):

    data = [1, 2, 3, 4, 5]
    
    monkeypatch.setattr(mixin.warn_message, 'print', lambda _: None)
    with pytest.raises(FileError) as error:

        mixin.unsupported_type(data)

    assert "Unsupported data type -> <class 'list'>" == str(error.value)


def test_unsuppored_file_type(mixin, monkeypatch):

    data = 'file.json'
    
    monkeypatch.setattr(mixin.warn_message, 'print', lambda _: None)
    with pytest.raises(FileError) as error:

        mixin.unsupported_type(data)

    assert "Unsupported file type -> file.json" == str(error.value)

def test_unsuppored_engine(mixin, monkeypatch):

    engine = 'MongoDB'
    
    monkeypatch.setattr(mixin.warn_message, 'print', lambda _: None)
    with pytest.raises(EngineError) as error:

        mixin.unsupported_engine(engine)

    assert "Unsupported engine -> MongoDB" == str(error.value)

import pytest
from contextlib import contextmanager
from scope import SymbolsTable, Entry


@contextmanager
def table_context(add_entry=True):
    st = SymbolsTable('testing')
    e = Entry('var1', 'id', 'variable', 'testing', 'integer', None)
    if add_entry: st.add_entry(e)
    try:
        yield st, e
    finally:
        pass


def test_entry_exists():
    with table_context() as (st, entry):
        result = st.entry_exists('var1')
        assert result == True


def test_add_entry():
    with table_context() as (st, entry):
        result = st['var1']

        assert result == entry
        with pytest.raises(Exception):
            st.add_entry(e)


def test_get_entrys():
    with table_context() as (st, entry):
        result = st.get_entrys()

        assert entry in result
        assert len(result) == 1

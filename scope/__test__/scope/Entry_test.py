import pytest
from scope import Entry


def test_create_entry():
    lexema, token, category, = 'var1', 'id', 'variable'
    scope, _type, value = 'global', 'integer', 3
    entry = Entry(lexema, token, category, scope,
                  _type, value)

    assert entry.lexema == lexema
    assert entry.token == token
    assert entry.category == category
    assert entry.scope == scope
    assert entry.type == _type
    assert entry.value == value

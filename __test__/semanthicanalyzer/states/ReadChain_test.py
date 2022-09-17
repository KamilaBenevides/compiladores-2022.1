import pytest, io, sys
from semanthicanalyzer.states import ReadChain
from scope import ScopeManager, Entry

token_list = [['read', 'reserved'], ['(', 'delimiter'], ['a', 'id'],
              [',', 'delimiter'], ['b', 'id'], [',', 'delimiter'],
              ['c', 'id'], [')', 'delimiter'], [';', 'delimiter']
             ]

sm = ScopeManager()
gbl = sm['global']
a = Entry('a', 'id', 'variable', 'global', 'integer', None)
b = Entry('b', 'id', 'variable', 'global', 'integer', None)
c = Entry('c', 'id', 'variable', 'global', 'integer', None)
gbl.add_entry(a)
gbl.add_entry(b)
gbl.add_entry(c)


def test_read():
    sys.stdin = io.StringIO('1\n2\n3')
    index = [0]
    read_chain = ReadChain(sm, token_list, index)

    read_chain.exec()
    sys.stdin = sys.__stdin__

    assert a.value == 1
    assert b.value == 2
    assert c.value == 3

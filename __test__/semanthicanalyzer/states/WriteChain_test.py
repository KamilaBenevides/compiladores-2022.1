import pytest, io, sys
from semanthicanalyzer.states import WriteChain
from scope import ScopeManager, Entry

token_list = [['write', 'reserved'], ['(', 'delimiter'], ['a', 'id'],
              ['b', 'id'], ['c', 'id'], [')', 'delimiter'],
              [';', 'delimiter']
             ]

sm = ScopeManager()
gbl = sm['global']
a = Entry('a', 'id', 'variable', 'global', 'integer', 1)
b = Entry('b', 'id', 'variable', 'global', 'integer', 2)
c = Entry('c', 'id', 'variable', 'global', 'integer', 3)
gbl.add_entry(a)
gbl.add_entry(b)
gbl.add_entry(c)


def test_write():
    out_stream = io.StringIO()
    sys.stdout = out_stream
    index = [0]
    write_chain = WriteChain(sm, token_list, index)

    write_chain.exec()
    sys.stdout = sys.__stdout__
    out_stream.seek(0)  # Retorna o arquivo para o início
    result = out_stream.read()

    assert result == '1 2 3 \n'


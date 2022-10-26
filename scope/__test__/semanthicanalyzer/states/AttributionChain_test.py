import pytest
from semanthicanalyzer.states import AttributionChain
from scope import ScopeManager, Entry

# var := a + 2 * 4 - b / c
token_list = [['id', 'id'], [':=', 'attribution'], ['a', 'id'], ['+', 'operador'], ['2', 'intnum'],
              ['*', 'operador'], ['0', 'intnum'], ['-', 'operador'],
              ['b', 'id'], ['/', 'operador'], ['c', 'id'], [';', 'delimiter']
             ]

sm = ScopeManager()
gbl = sm['global']
# 5 + 2 * 0 - 200 // 3 = -4
_id = Entry('id', 'id', 'variable', 'global', 'integer', None)
_id_bool = Entry('id_bool', 'id', 'variable', 'global', 'boolean', None)
gbl.add_entry(_id)
gbl.add_entry(_id_bool)
gbl.add_entry(Entry('a', 'id', 'variable', 'global', 'integer', 5))
gbl.add_entry(Entry('b', 'id', 'variable', 'global', 'integer', 10))
gbl.add_entry(Entry('c', 'id', 'variable', 'global', 'integer', 3))

def test_attribution():
    index = [0]
    attr_chain = AttributionChain(sm, token_list, index)
    value = attr_chain.exec()

    token_list[0][0] = 'id_bool'
    index = [0]
    attr_chain2 = AttributionChain(sm, token_list, index)
    value2 = attr_chain2.exec()
    
    assert _id.value == -4
    assert _id_bool.value == 1

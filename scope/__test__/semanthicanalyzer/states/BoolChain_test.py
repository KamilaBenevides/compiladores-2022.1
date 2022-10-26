import pytest
from semanthicanalyzer.states import BoolChain
from scope import ScopeManager, Entry

# a and b )
token_list = [['a', 'id'], ['and', 'boolean1'], ['b', 'id'], [')', 'delimiter'],
             ]

# a and b or not not c and not d )
token_list2 = [['not', 'boolean2'], ['not', 'boolean2'], ['a', 'id'], 
               ['and', 'boolean1'], ['not', 'boolean2'], 
               ['b', 'id'], [')', 'delimiter']
              ]

token_list3 = [['a', 'id'], ['and', 'boolean1'], ['b', 'id'], ['or', 'boolean1'],
               ['c', 'id'], ['or', 'boolean1'], ['not', 'boolean2'], ['d', 'id'],
               [')', 'delimiter'],
              ]

sm = ScopeManager()
gbl = sm['global']
gbl.add_entry(Entry('a', 'id', 'variable', 'global', 'boolean', 1))
gbl.add_entry(Entry('b', 'id', 'variable', 'global', 'boolean', 0))
gbl.add_entry(Entry('c', 'id', 'variable', 'global', 'boolean', 1))
gbl.add_entry(Entry('d', 'id', 'variable', 'global', 'boolean', 0))


def test_expression():
    index = [[0], [0], [0]]
    bool_chain = BoolChain(sm, token_list, index[0])
    bool_chain2 = BoolChain(sm, token_list2, index[1])
    bool_chain3 = BoolChain(sm, token_list3, index[2])

    value = bool_chain.exec()
    value2 = bool_chain2.exec()
    value3 = bool_chain3.exec()
    
    assert value == 0 
    assert value2 == 1
    assert value3 == 1
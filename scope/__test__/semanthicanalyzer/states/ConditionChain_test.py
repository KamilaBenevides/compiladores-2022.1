import pytest
from semanthicanalyzer.states import ConditionChain
from scope import ScopeManager, Entry

# a and b )
token_list = [['a', 'id'], ['and', 'boolean1'], 
             ['b', 'id'], [')', 'delimiter']]

# c + 2 = 3 ) 
token_list2 = [['c', 'id'], ['+', 'operador'], ['2', 'intnum'],
              ['=', 'relacao'], ['3', 'intnum'], 
              [')', 'delimiter']]

sm = ScopeManager()
glb = sm['global']
a = Entry('a', 'id', 'variable', 'global', 'boolean', 1)
b = Entry('b', 'id', 'variable', 'global', 'boolean', 1)
c = Entry('c', 'id', 'variable', 'global', 'integer', 1)
glb.add_entry(a)
glb.add_entry(b)
glb.add_entry(c)

def test_relational():
    index = [[0], [0]]
    rel_chain = ConditionChain(sm, token_list, index[0])
    rel_chain2 = ConditionChain(sm, token_list2, index[1])

    value = rel_chain.exec()
    value2 = rel_chain2.exec()

    assert value == 1
    assert value2 == 1
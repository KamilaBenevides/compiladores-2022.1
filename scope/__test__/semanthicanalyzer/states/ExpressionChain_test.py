import pytest
from semanthicanalyzer.states import ExpressionChain
from scope import ScopeManager, Entry

# a + 2 * 4 - b / c
token_list0 = [['a', 'id'], ['+', 'operador'], ['2', 'intnum'],
              ['*', 'operador'], ['0', 'intnum'], ['-', 'operador'],
              ['b', 'id'], ['/', 'operador'], ['c', 'id'], [';', 'delimiter']
             ]
token_list1 = [['4', 'intnum'],[';', 'delimiter']]
token_list2 = [['d', 'id'], [';', 'delimiter']]
token_list3 = [['d', 'id'], ['+', 'operador'], ['2', 'intnum'], [';', 'delimiter']]
token_list4 = [['2', 'intnum'], ['+', 'operador'], ['d', 'id'], [';', 'delimiter']]

sm = ScopeManager()
gbl = sm['global']
# 5 + 2 * 0 - 200 // 3 = -4
gbl.add_entry(Entry('a', 'id', 'variable', 'global', 'integer', 5))
gbl.add_entry(Entry('b', 'id', 'variable', 'global', 'integer', 10))
gbl.add_entry(Entry('c', 'id', 'variable', 'global', 'integer', 3))
gbl.add_entry(Entry('d', 'id', 'variable', 'global', 'boolean', 1))


def test_expression():
    index = [[0], [0], [0], [0], [0]]
    exp_chain0 = ExpressionChain(sm, token_list0, index[0])
    exp_chain1 = ExpressionChain(sm, token_list1, index[1])
    exp_chain2 = ExpressionChain(sm, token_list2, index[2])
    exp_chain3 = ExpressionChain(sm, token_list3, index[3])
    exp_chain4 = ExpressionChain(sm, token_list4, index[4])

    value0 = exp_chain0.exec()
    value1 = exp_chain1.exec()
    value2 = exp_chain2.exec()

    assert value0 == -4
    assert value1 == 4
    assert value2 == 1
    with pytest.raises(Exception):
        value3 = exp_chain3.exec()
        value4 = exp_chain4.exec()

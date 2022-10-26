import pytest
from semanthicanalyzer.states import RepeatChain
from syntaticanalyzer import JumpIndex
from scope import ScopeManager, Entry

repeat_jump = JumpIndex(small_jump=5, big_jump=0, jump_big=True)

token_list = [['repeat', 'reserved'], 
                    ['aux', 'id'], [':=', 'attribution'], ['5', 'intnum'], [';', 'delimiter'],
              ['until', 'reserved', repeat_jump], ['(', 'delimiter'], ['entrada', 'id'], 
              ['>', 'relacao'], ['aux', 'id'], [')', 'delimiter'], [';', 'delimiter']
             ]

sm = ScopeManager()
glb = sm['global']
e1 = Entry('entrada', 'id', 'variable', 'global', 'integer', 10)
e2 = Entry('aux', 'id', 'variable', 'global', 'integer', 5)

glb.add_entry(e1)
glb.add_entry(e2)

def test_repeat():
    index = [[5], [5]]
    rp_chain = RepeatChain(sm, token_list, index[0])
    rp_chain2 = RepeatChain(sm, token_list, index[1])

    rp_chain.exec()
    e1.value = -10
    rp_chain2.exec()

    assert index[0][0] == 11
    assert index[1][0] == 0 

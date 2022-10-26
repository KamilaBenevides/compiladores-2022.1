import pytest
from semanthicanalyzer.states import WhileChain
from syntaticanalyzer import JumpIndex
from scope import ScopeManager, Entry

while_jump = JumpIndex(small_jump=0, big_jump=13, jump_big=True)

token_list = [['while', 'reserved', while_jump], ['(', 'delimiter'], ['entrada', 'id'],
              ['>', 'relacao'], ['aux', 'id'], [')', 'delimiter'], ['do', 'reserved'],
              ['begin', 'reserved'],
                    ['aux', 'id'], [':=', 'attribution'], ['5', 'intnum'], [';', 'delimiter'],
              ['end', 'reserved'], [';', 'delimiter']
             ]

sm = ScopeManager()
glb = sm['global']
e1 = Entry('entrada', 'id', 'variable', 'global', 'integer', 10)
e2 = Entry('aux', 'id', 'variable', 'global', 'integer', 0)

glb.add_entry(e1)
glb.add_entry(e2)

def test_while():
    index = [[0], [0]]
    while_chain = WhileChain(sm, token_list, index[0])
    while_chain2 = WhileChain(sm, token_list, index[1])

    while_chain.exec()
    e1.value = -10
    while_chain2.exec()

    assert index[0][0] == 7
    assert index[1][0] == 13

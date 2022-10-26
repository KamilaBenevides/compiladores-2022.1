import pytest
from semanthicanalyzer.states import IfChain
from syntaticanalyzer import JumpIndex
from scope import ScopeManager, Entry

if_jump = JumpIndex(small_jump=0, big_jump=12, jump_big=True)
else_jump = JumpIndex(small_jump=13, big_jump=19, jump_big=True)

token_list = [['if', 'reserved', if_jump], ['(', 'delimiter'], ['entrada', 'id'],
              ['>', 'relacao'], ['aux', 'id'], [')', 'delimiter'], ['then', 'reserved'],
              ['begin', 'reserved'],
                    ['aux', 'id'], [':=', 'attribution'], ['5', 'intnum'], [';', 'delimiter'],
              ['end', 'reserved'],
              ['else', 'reserved', else_jump], ['begin', 'reserved'],
                    ['aux', 'id'], [':=', 'attribution'], ['10', 'intnum'], [';', 'delimiter'],
              ['end', 'reserved'], [';', 'delimiter']]

sm = ScopeManager()
glb = sm['global']
e1 = Entry('entrada', 'id', 'variable', 'global', 'integer', 10)
e2 = Entry('aux', 'id', 'variable', 'global', 'integer', 0)

glb.add_entry(e1)
glb.add_entry(e2)

def test_if():
    index = [[0], [0]]
    if_chain = IfChain(sm, token_list, index[0])
    if_chain2 = IfChain(sm, token_list, index[1])

    if_chain.exec()
    e1.value = -10
    if_chain2.exec()

    assert index[0][0] == 7
    assert index[1][0] == 12

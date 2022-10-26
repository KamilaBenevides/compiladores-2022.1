import pytest
from semanthicanalyzer.states import ForChain
from syntaticanalyzer import JumpIndex, TOKEN_POS_INDEX
from scope import ScopeManager, Entry

"""
    for entrada := 0 to aux + 2 do 
        begin 
        outra_var := 5;
        end;
"""
for_jump = JumpIndex(small_jump=0, big_jump=15, jump_big=True)
end_jump = JumpIndex(small_jump=15, big_jump=0, jump_big=True)
token_list = [['for', 'reserved', for_jump], 
              ['entrada', 'id'], [':=', 'attribution'], ['0', 'intnum'], ['to', 'reserved'], 
              ['aux', 'id'], ['+', 'operador'], ['2', 'intnum'], ['do', 'reserved'],
              ['begin', 'reserved'],
                    ['outra_var', 'id'], [':=', 'attribution'], ['5', 'intnum'], [';', 'delimiter'],
              ['end', 'reserved', end_jump], [';', 'delimiter']
             ]

sm = ScopeManager()
glb = sm['global']
e1 = Entry('entrada', 'id', 'variable', 'global', 'integer', None)
e2 = Entry('aux', 'id', 'variable', 'global', 'integer', 8)

glb.add_entry(e1)
glb.add_entry(e2)

def test_for():
    index = [[0], [0]]
    for_chain = ForChain(sm, token_list, index[0])
    for_chain2 = ForChain(sm, token_list, index[1])

    for_chain.exec()
    e2.value = -10
    for_chain2.exec()

    assert index[0][0] == 9 # for verdadeiro
    assert index[1][0] == 15 # for falso
    assert token_list[14][TOKEN_POS_INDEX].big_jump_index == 4  # testar big jump do end
    assert token_list[4][TOKEN_POS_INDEX].small_jump_index == 1. # testar jumpindex do to
    assert token_list[4][TOKEN_POS_INDEX].big_jump_index == 15
import pytest
from contextlib import contextmanager
from scope import ScopeManager, SymbolsTable, Entry

@contextmanager
def manager_context(*args, **kwargs):
    """
    provides scope scope_manager with one registered scope besides global
    """
    sm = ScopeManager()
    scope = sm.create_scope('teste_scope', **kwargs)
    try:
        yield sm, scope
    finally:
        pass


def test_create_scope():
    with manager_context() as (sm, scope):
        s1 = sm.create_scope('teste2', register=False)
        s2 = sm.create_scope('test3', push=True)

        top = sm.get_stack_top()

        assert sm['teste_scope'] == scope, f'{scope.scope_name} scope shoudld be registered.'
        assert top == s2, f'{s2.scope_name} scope should be on top.'
        with pytest.raises(KeyError):
            sm['teste2']


def test_push_in_stack():
    with manager_context() as (sm, scope):
        sm.push_in_stack(scope)
        top = sm.get_stack_top()

        assert scope == top, f'{scope.scope_name} scope should be on top'

def test_stack():
    with manager_context(push=True) as (sm, scope):
        top = sm.get_stack_top()
        name = sm.get_stack_top_name()
        pop1 = sm.pop_stack()
        pop2 = sm.pop_stack()
        pop3 = sm.pop_stack()

        assert scope == top, f'It should be {scope.scope_name} scope'
        assert scope.scope_name == name, f'It should be {scope.scope_name}'
        assert scope == pop1, f'It should be {scope.scope_name} scope'
        assert sm['global'] == pop2, 'It should be global scope'
        assert sm['global'] == pop3, "ScopeManager should't remove global scope on pop"


def test_get_in_stack_from_top():
    with manager_context(push=True) as (sm, scope):
        s1 = sm.create_scope('teste2', push=True)

        c = sm.get_in_stack_from_top(1)
        c1 = sm.get_in_stack_from_top(2)

        assert scope == c
        assert sm['global'] == c1


def test_search_identifier():
    with manager_context(push=True) as (sm, scope):
        _global = sm['global']
        g1 = Entry('gvar1', 'id', 'variable', 'global', 'integer', 3)
        g2 = Entry('var2', 'id', 'variable', 'global', 'integer', 4)
        _global.add_entry(g1)
        _global.add_entry(g2)

        s1_entry1 = Entry('var1', 'id', 'variable', 'es1', 'boolean', 1)
        s1_entry2 = Entry('var2', 'id', 'variable', 'es1', 'integer', 5)
        scope.add_entry(s1_entry1)
        scope.add_entry(s1_entry2)

        scope2 = sm.create_scope('es2', push=True)
        s2_entry1 = Entry('var1', 'id', 'variable', 'es1', 'boolean', 1)
        scope2.add_entry(s2_entry1)

        id1 = sm.search_identifier('var1')
        id2 = sm.search_identifier('var2')
        id3 = sm.search_identifier('gvar1')

        print(id1)
        assert id1 == s2_entry1
        print(id2)
        assert id2 == s1_entry2
        print(id3)
        assert id3 == g1


from .SymbolsTable import SymbolsTable

class ScopeManager(object):
  def __init__(self):
    self.scopes = {'global': SymbolsTable('global')}
    self.scope_stack = [self.scopes['global']]

  def create_scope(self, name, register=True, push=False):
    """Cria um novo escopo

    register = True - salva a referencia do novo escopo
    push     = True - adiciona o novo escopo à pilha
    """
    s = SymbolsTable(name)
    if register:
      self.scopes[name] = s
    if push:
      self.push_in_stack(s)
    return s

  def __getitem__(self, key):
    return self.scopes[key]

  def push_in_stack(self, scope):
    self.scope_stack.append(scope)

  def pop_stack(self):
    if len(self.scope_stack) == 1: # caso so reste o escopo global na pilha
      return self.scope_stack[0]
    return self.scope_stack.pop()

  def get_stack_top(self):
    top = self.scope_stack[len(self.scope_stack) - 1]
    return top

  def get_stack_top_name(self):
    top = self.get_stack_top()
    return top.scope_name

  def get_in_stack_from_top(self, index):
    top = self.scope_stack[len(self.scope_stack) - 1 - index]
    return top

  def search_identifier(self, name): # retorna o objeto Entry que é a linha na tabela de simbolos 
    top_scope = self.get_stack_top()
    if top_scope.entry_exists(name):
      id = top_scope[name]
      return id
    id = self.__search_identifier_in_other_scopes(name)
    if id is None:
      raise Exception(f'Identifier not found {name}.')
    return id

  def __search_identifier_in_other_scopes(self, name):
    id = None
    top_scope = self.get_stack_top()
    for i in range(len(self.scope_stack)-2, -1, -1):  # começa do topo - 1
      current_scope = self.scope_stack[i]
      if current_scope.scope_name != top_scope.scope_name:
        if current_scope.entry_exists(name):
          id = current_scope[name]
          break
    return id

  def __str__(self):
    s = ''
    for scope in self.scopes.values():
      s += str(scope) + '\n\n'
    return s

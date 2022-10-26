from .ScopeManager import ScopeManager

class StateMachine(object):
  def __init__(self):
    self.state = "initial_state";
    self.scope_manager = ScopeManager()
  
  def input(self, input):
    lexeme, token = input
    self.run(lexeme, token)
  
  def run(self, lexeme, token):

    if self.state is "initial_state":
      if lexeme == 'procedure' or lexeme == 'function':
        self.state = "change_scope"
      elif lexeme == 'begin':
        self.scope_manager.pop_stack()
      elif lexeme == 'var':
        self.state = "var_declaration"
      
    elif self.state is "var_declaration":
      if lexeme == ',':
        continue
      elif lexeme == ':':
        self.state = "get_var_type"
      else: # <id>
        scope = self.scope_manager.get_stack_top()
        self.action_buffer.append(
          (scope.add_entry, {
            'lexema': lexeme,
            'token' : token,
            'category': 'variable',
            'scope': scope.scope,
            'type': None,
            'value': None,
          })
        )

    elif self.state is "get_var_type":
      while len(self.action_buffer) > 0:
        function, arg = self.action_buffer.pop()
        arg['type'] = lexeme
        function(arg)
      self.state = "prepare_more_var_declaration"


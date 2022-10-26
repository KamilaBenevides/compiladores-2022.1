from scope import Entry, BEGIN_ENTRY_NAME, END_ENTRY_NAME
import re

class SymbolsHandler(object):
  def __init__(self, scope_manager):
    self.scope_manager = scope_manager
    self.previous_scope_name = ''
    self.current_scope_name = 'global'
    self.__next_action = self.__analyze # estado a ser executado no momento
    self.action_buffer = []
    self.routine_token = None
    self.parameter_index = 0

  def analyze(self, _token):
    """
    Executa a máquina de estado, recebe um token e muda o estado atual da máquina (self.__next_action)
    """
    self.__next_action(_token)

  def __analyze(self, _token):
    """
    Estado inicial e estado final da maquina de estado.
    """
    try:
      symbol, token = _token
    except ValueError:
      symbol, token, token_pos = _token
    if symbol == 'procedure' or symbol == 'function':
      self.routine_token = _token
      self.__next_action = self.__change_scope
    elif symbol == 'begin':
      self.scope_manager.pop_stack()
    elif symbol == 'var':
      self.__next_action = self.__var_declaration

  def __change_scope(self, _token):
    """
    Estado intermediário da maquina de estado, que trata procedimento e funcao
    """
    symbol, token = _token
    scope_name = self.scope_manager.get_stack_top_name() + '-' + symbol
    scope = self.scope_manager.create_scope(scope_name, push=True)
    #self.scope_manager.push_in_stack(scope)
    self.__add_begin_end_indexes_to_scope(scope)
    self.__next_action = self.__prepare_parameter_declaration
    previous_scope = self.scope_manager.get_in_stack_from_top(1)
    previous_scope.add_entry(Entry(symbol, token, '', previous_scope.scope_name, None))

  def __add_begin_end_indexes_to_scope(self, scope):
      jump_index = self.routine_token[2]
      scope.add_entry(
        Entry(BEGIN_ENTRY_NAME, 'id', 'variable',
              scope.scope_name, 'integer',jump_index.small_jump_index)
      )
      scope.add_entry(
        Entry(END_ENTRY_NAME, 'id', 'variable',
              scope.scope_name, 'integer', jump_index.big_jump_index)
      )

  def __prepare_parameter_declaration(self, _token):
    """
    Estado intermediário da maquina de estado, que prepara para receber os parametros, caso haja
    """
    if _token[0] == '(':
      self.__next_action = self.__parameter_declaration
    elif _token[0] == ':' or _token[0] ==';':  # se entrar significa que é uma função ou procedimento sem parametros
      self.__end_routine(_token)

  def __parameter_declaration(self, _token):
    """
    Estado intermediário da maquina de estado, que trata declaração de parametros
    """
    index = str(int(self.parameter_index))
    self.__var_declaration(_token, 'parameter', index) # trata a declaração de variaveis dentro dos parametros
    self.parameter_index += .5
    if _token[0] == ':': # se terminou a declaracao das variaveis, altera o estado de get_var_type para get_parameters_type
      self.__next_action = self.__get_parameters_type # seta o tipo das variaveis declaradas

  def __get_parameters_type(self, _token):
    if _token[0] == ';':
      self.__next_action = self.__parameter_declaration
    elif _token[0] == ')':
      self.__next_action = self.__end_routine
      self.parameter_index = 0
    else:  # li o tipo do argumento
      self.__get_var_type(_token)
      self.__next_action = self.__get_parameters_type

  def __end_routine(self, _token):
    previous_scope = self.scope_manager.get_in_stack_from_top(1)  # nome do escopo onde a rotina está sendo declarada
    scope_name = self.scope_manager.get_stack_top_name().split('-')[-1]
    entry = previous_scope[scope_name]  # o escopo atual tem o mesmo nome da rotina
    if _token[0] == ';': # so pode ser procedimento
      entry.category = 'procedure'
    elif _token[0] == ':': #so poder ser funcao
      entry.category = 'function'
      entry.type = 'integer' # todas as funcoes sao inteiras
    self.__next_action = self.__analyze

  def __prepare_more_var_declaration(self, _token):
    if _token[0] in ['procedure', 'function']: # acabou a declaração de variaveis e tem rotina
      self.routine_token = _token
      self.__next_action = self.__change_scope
    elif _token[0] == 'begin':  # acabou a declaração de variáveis e não tem rotina
      self.scope_manager.pop_stack()
      self.__next_action = self.__analyze 
    elif _token[1] == 'id': # comecou outra declaracao de variaveis
      self.__var_declaration(_token)
      self.__next_action = self.__var_declaration

  def __var_declaration(self, _token, category='variable', index=''):
    """
    Estado intermediário da maquina de estado, que trata declaracao de variaveis normais
    """
    symbol, token = _token
    if symbol == ',':
      return
    elif symbol == ':':
      self.__next_action = self.__get_var_type
    else: # li <id>
      scope = self.scope_manager.get_stack_top()
      e = Entry(symbol, token, category + index , scope.scope_name, None, None)
      self.action_buffer.append((scope.add_entry, e))

  def __get_var_type(self, _token):
    """Estado intermediário da maquina de estado.

      Esse estado esvazia o action_buffer. Nele ficam armazenadas
      as informações das variaveis declaradas e a função para adicioná-las
      ao seu respectivo escopo. A adicão ao escopo é feita nesta função, após
      se saber o tipo dessas variáveis
    """
    symbol = _token[0]
    while len(self.action_buffer) > 0:
      function, entry = self.action_buffer.pop()
      entry.type = symbol
      function(entry)
    self.__next_action = self.__prepare_more_var_declaration


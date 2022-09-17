from .LexicalBuffer import LexicalBuffer
from utils.Exceptions import LexicalError

class Lexical(object):

  def __init__(self, file):
    self.file = file
    self.tokens = []
    self.buffer = LexicalBuffer()
    self.line = 0
    self.pos = 0

  def __add_buffer_to_tokens(self, group : str):
    self.tokens.append([str(self.buffer), group])

  def __add_to_tokens(self, symbol, group : str):
    self.tokens.append([str(symbol), group])

  def __handle_buffer(self):
    if len(self.buffer) == 0: return

    if self.buffer.is_number(): # se for um numero
      self.__add_buffer_to_tokens('intnum')

    elif self.buffer.is_word(): # se for palavra
      if self.buffer.is_boolean_one(): # verifica se eh op boolean1
        self.__add_buffer_to_tokens('boolean1')
      elif self.buffer.is_boolean_two(): # verifica se eh op boolean2
        self.__add_buffer_to_tokens('boolean2')
      elif self.buffer.is_reserved_word(): # ou se eh palavra reservada
        self.__add_buffer_to_tokens('reserved')
      elif self.buffer.is_id(): # ou se eh um identificador
        self.__add_buffer_to_tokens('id')
      else:
        raise LexicalError(f"Invalid identifier '{self.buffer}' at position {self.pos + 1}, line {self.line}")
    self.buffer.clean()

  def __is_compose_delimiter(self, line_buffer):
    current_symbol = LexicalBuffer(line_buffer[self.pos])
    if self.pos + 1 < len(line_buffer):
      compose = current_symbol + line_buffer[self.pos + 1]
      if compose.is_compose_delimiter():
        if compose.is_relational():
          self.__add_to_tokens(compose, 'relacao')
        else:
          self.__add_to_tokens(compose, 'attribution')
        self.pos += 1
        return True
    return False

  def __split(self, line_buffer):
    current_symbol = LexicalBuffer(line_buffer[self.pos])
    if current_symbol.is_white_space():
      self.__handle_buffer()

    elif current_symbol.is_delimiter():
      self.__handle_buffer()
      if not self.__is_compose_delimiter(line_buffer):
        if current_symbol.is_operator():
          self.__add_to_tokens(current_symbol, 'operador')
        elif current_symbol.is_relational():
          self.__add_to_tokens(current_symbol, 'relacao')
        else:
          self.__add_to_tokens(current_symbol, 'delimiter')

    elif current_symbol.is_valid():
      self.buffer += current_symbol

    else:
      raise LexicalError(f'Invalid symbol at position {self.pos + 1}, line {self.line}')

  def split(self):
    while True:
      line_buffer = self.file.readline()
      if line_buffer == '': break
      self.line += 1
      while (self.pos < len(line_buffer)):
        self.__split(line_buffer)
        self.pos += 1
      self.pos = 0
    return self.tokens

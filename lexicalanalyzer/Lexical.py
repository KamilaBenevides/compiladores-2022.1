from .LexicalBuffer import LexicalBuffer
from utils.Exceptions import LexicalError

class Lexical(object):

  def __init__(self, file):
    self.file = file
    self.tokens = []
    self.buffer = LexicalBuffer()
    self.line = 0
    self.pos = 0

  def __addBufferToTokens(self, group : str):
    self.tokens.append([str(self.buffer), group])

  def __addToTokens(self, symbol, group : str):
    self.tokens.append([str(symbol), group])

  def __handleBuffer(self):
    if len(self.buffer) == 0: return

    if self.buffer.isNumber():
      self.__addBufferToTokens('intnum')

    elif self.buffer.isWord():
      if self.buffer.isBooleanTwo():
        self.__addBufferToTokens('boolean2')
      elif self.buffer.isBooleanOne():
        self.__addBufferToTokens('boolean1')
      elif self.buffer.isReservedWord():
        self.__addBufferToTokens('reserved')
      elif self.buffer.isId():
        self.__addBufferToTokens('id')
      else:
        raise LexicalError(f"Invalid identifier '{self.buffer}' at position {self.pos + 1}, line {self.line}")
    self.buffer.clean()

  def __isComposeDelimiter(self, line_buffer):
    current_symbol = LexicalBuffer(line_buffer[self.pos])
    if self.pos + 1 < len(line_buffer):
      compose = current_symbol + line_buffer[self.pos + 1]
      if compose.isComposeDelimiter():
        if compose.isRelational():
          self.__addToTokens(compose, 'relacao')
        else:
          self.__addToTokens(compose, 'attribution')
        self.pos += 1
        return True
    return False

  def __split(self, line_buffer):
    current_symbol = LexicalBuffer(line_buffer[self.pos])
    if current_symbol.isWhiteSpace():
      self.__handleBuffer()

    elif current_symbol.isDelimiter():
      self.__handleBuffer()
      if not self.__isComposeDelimiter(line_buffer):
        if current_symbol.isOperator():
          self.__addToTokens(current_symbol, 'operador')
        elif current_symbol.isRelational():
          self.__addToTokens(current_symbol, 'relacao')
        else:
          self.__addToTokens(current_symbol, 'delimiter')

    elif current_symbol.isValid():
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

import re

__all__ = ['LexicalBuffer']


class LexicalBuffer(object):
  alphabet_pattern = re.compile(r'^[a-z\d]$')
  word_pattern = re.compile(r'^[a-z\d]*$')

  id_pattern = re.compile(r'^[a-z][a-z\d]*$')
  delimiter_pattern = re.compile(r'^[:;,\.()+\-*/=><]$')

  white_space_pattern = re.compile(r'[ \n\t]')
  compose_delimiter_pattern = re.compile(r'^[:<>]=$|^[=<]>$')

  booleans_one = ['and', 'or']
  booleans_two = ['not']
  reserved_words = ['program', 'begin', 'end', 'var', 'integer', 
                    'boolean', 'procedure', 'function', 'read', 
                    'write', 'for', 'to', 'do', 'repeat', 'until', 
                    'while', 'if', 'then','else']
  relationals = ['<', '>', '=', '<>', '<=', '>=']
  operators = ['+', '-', '*', '/']

  def __init__(self, string : str=''):
    self.__buffer = string

  def clean(self) -> None:
    self.__buffer = ''
  
  def is_word(self) -> bool:
    return bool(self.word_pattern.match(self.__buffer))

  def is_number(self) -> bool:
    return bool(self.__buffer.isdigit())

  def is_id(self) -> bool:
    return bool(self.id_pattern.match(self.__buffer))

  def is_delimiter(self) -> bool:
    return  bool(self.delimiter_pattern.match(self.__buffer))

  def is_compose_delimiter(self) -> bool:
    return bool(self.compose_delimiter_pattern.match(self.__buffer))

  def is_white_space(self) -> bool:
    return bool(self.white_space_pattern.match(self.__buffer))

  def is_boolean_one(self) -> bool:
    return self.__buffer in self.booleans_one

  def is_boolean_two(self) -> bool:
    return self.__buffer in self.booleans_two

  def is_reserved_word(self) -> bool:
    return self.__buffer in self.reserved_words

  def is_relational(self) -> bool:
    return self.__buffer in self.relationals

  def is_operator(self) -> bool:
    return self.__buffer in self.operators

  def is_valid(self) -> bool:
    return bool(self.alphabet_pattern.match(self.__buffer))

  def __str__(self):
    return self.__buffer[:]

  def __len__(self):
    return len(self.__buffer)

  def __add__(self, buffer):
    if type(buffer) != str:
      buffer = str(buffer)
    self.__buffer += buffer
    return self

  def __iadd__(self, buffer):
    if type(buffer) != str:
      buffer = str(buffer)
    self.__buffer += buffer
    return self

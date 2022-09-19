import re

__all__ = ['LexicalBuffer']


class LexicalBuffer(object):
  booleansTwo = ['and', 'or']
  booleansOne = ['not']
  reservedWords = ['program', 'begin', 'end', 'var', 'integer', 'array',
                    'boolean', 'procedure', 'function', 'read', 
                    'write', 'for', 'to', 'do', 'repeat', 'until', 
                    'while', 'if', 'then','else']
  relationals = ['<', '>', '=', '<>', '<=', '>=', 'in']
  operators = ['+', '-', '*', '/']

  alphabetPattern = re.compile(r'^[A-z\d]$')
  wordPattern = re.compile(r'^[A-z\d]*$')
  idPattern = re.compile(r'^[A-z][A-z\d]*$')
  delimiterPattern = re.compile(r'^[:;,\.()+\-*/=><]$')
  whiteSpacePattern = re.compile(r'[ \n\t]')
  composeDelimiterPattern = re.compile(r'^[:<>]=$|^[=<]>$')


  def __init__(self, string : str=''):
    self.__buffer = string

  def clean(self) -> None:
    self.__buffer = ''
  
  def isWord(self) -> bool:
    return bool(self.wordPattern.match(self.__buffer))

  def isNumber(self) -> bool:
    return bool(self.__buffer.isdigit())

  def isId(self) -> bool:
    return bool(self.idPattern.match(self.__buffer))

  def isDelimiter(self) -> bool:
    return  bool(self.delimiterPattern.match(self.__buffer))

  def isComposeDelimiter(self) -> bool:
    return bool(self.composeDelimiterPattern.match(self.__buffer))

  def isWhiteSpace(self) -> bool:
    return bool(self.whiteSpacePattern.match(self.__buffer))

  def isBooleanOne(self) -> bool:
    return self.__buffer in self.booleansTwo

  def isBooleanTwo(self) -> bool:
    return self.__buffer in self.booleansOne

  def isReservedWord(self) -> bool:
    return self.__buffer in self.reservedWords

  def isRelational(self) -> bool:
    return self.__buffer in self.relationals

  def isOperator(self) -> bool:
    return self.__buffer in self.operators

  def isValid(self) -> bool:
    return bool(self.alphabetPattern.match(self.__buffer))

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

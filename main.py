from sys import path as sys_path, argv
from utils import Path

main_path = str(Path().script_dir())
sys_path.append(main_path)

from lexicalanalyzer import Lexical
from syntaticanalyzer import Syntatic

if main_path[len(main_path) - 1] != '/':
  main_path += '/'


def main(file_path=main_path+'teste.dpr', output_early=True):
  file = argv[1] if len(argv) > 1 else file_path
  with open(file, 'r') as file:
    tokens = Lexical(file).split()
    print('Análise Léxica bem sucedida! A lista de tokens gerados está disponível no arquivo ListTokens.txt')
    scope_manager = Syntatic(tokens).parse()
    print('Análise Sintática bem sucedida. A tabela de símbolos está disponível no arquivo symbols-table.log')
    if output_early: generate_output(tokens, scope_manager)
  return tokens, scope_manager

def generate_output(tokens, scope_manager):
    print_tokens(tokens)
    print_table(scope_manager)


def print_tokens(tokens):
  with open(main_path + 'ListTokens.txt', 'w') as log:
    for i in tokens:
      log.write("[")
      for c in i:
        log.write(str(c) + ', ')
      log.write("],\n")
      
def print_table(table):
  with open(main_path + 'symbols-table.log', 'w') as log:
    log.write(str(table))

if __name__ == '__main__':
  main(output_early=True)
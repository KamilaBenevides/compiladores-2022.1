BEGIN_ENTRY_NAME = '!begin'
END_ENTRY_NAME = '!end'

class SymbolsTable(object):
    def __init__(self, scope_name):
        self.items = {} # tabela de simbolos
        self.scope_name = scope_name # escopo dessa tabela
        self.columns_names = ['lexema', 'token', 'category', 'scope', 'type', 'value']

    def add_entry(self, item):
        """
        adiciona um item a tabela de simbolos
        item: item que iremos adicionar
        obs.: informações sobre item está em SymbolsHandler
        """
        name = item.lexema
        if self.entry_exists(name):
            raise Exception(f'DuplicatedIdentifierError: Identifier {name} duplicated.')
        self.items[name] = item

    def get_entrys(self):
        return self.items.values()

    def entry_exists(self, key):
        return key in self.items.keys()
    
    def copy(self):
        new_table = SymbolsTable(self.scope_name)
        for entry in self.items.values():
            new_table.add_entry(entry.copy())
        return new_table

    def __getitem__(self, key):
        return self.items[key]

    def __str__(self):
        s = ''
        for column in self.columns_names: # imprime uma linha com o nome das colunas
            s += f'{column:-^16}'
        s += '\n'
        for entry in self.items.values():
            s += str(entry)
            s += '\n'
        return s

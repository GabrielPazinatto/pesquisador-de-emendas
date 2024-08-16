from Hash import Hash
from Load import Loader

import pickle
import table_maker as tm

_MAIN_FILE_PATH = "Amendments.bin"

class Searcher(Loader):
    
    def __init__(self) -> None:
        super().__init__()
        
    def search_by_function(self):

        main_file = open(_MAIN_FILE_PATH, 'rb')

        print("Entre com o nome da função: ")
        function_name = input() 

        if function_name not in self.functions_pointers.keys():
            print("Função inválida.")
            return
        
        pointers = self.functions_pointers[function_name]

        amendments = []
        for pointer in pointers:
            main_file.seek(pointer)     #offset no arquivo principal 
            amendments.append(pickle.load(main_file)) #carrega do arquivo principal
        
        quantity = 0
        total_value = 0

        cols = ['Ano', 'Autor', 'Valor', 'Área', 'Estado']
        rows = []
        for a in amendments:
            quantity += 1
            total_value += a[self.indices['value']]
            rows.append([str(a[self.indices['year']]),a[self.indices['author']], f"{round(a[self.indices['value']], 3)}", 
                         a[self.indices['function']], a[self.indices['state']]])
            
        totals_cols = ["Quantidade", "Valor Total", "Área"]
        totals_rows = [[f"{quantity:,}" ,f"{round(total_value, 3):,}", function_name]]
        
        print(tm.make_table(totals_cols, totals_rows, scaling=2))
        
    def search_by_author(self):
        
        main_file = open(_MAIN_FILE_PATH, 'rb')
        
        print("Entre com o nome do parlamentar: ")
        author_name = input()
        
        amendments_addr = self.authors_record.search_by_prefix(author_name)
        
        if amendments_addr == None:
            print("Nome não consta.\n")
            return

        amendments = []
        for address in amendments_addr:
            main_file.seek(address)
            amendments.append(pickle.load(main_file))
            
        cols = ['Ano', 'Autor', 'Valor', 'Área', 'Estado']
        rows = []

        total_value = 0
        quantity = 0
        
        for a in amendments:
            quantity += 1
            total_value += a[self.indices['value']]
            rows.append([str(a[self.indices['year']]),a[self.indices['author']], 
                         f"{round(a[self.indices['value']], 3)}", a[self.indices['function']], a[self.indices['state']]])
        
        for row in tm.make_table(cols,rows).split('\n'):
            print(row)
            
        totals_cols = ["Quantidade", "Valor Total"]
        totals_rows = [[f"{quantity:,}" ,f"{round(total_value, 3):,}"]]
        
        print(tm.make_table(totals_cols, totals_rows, scaling=2))
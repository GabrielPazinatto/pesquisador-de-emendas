from Hash import Hash
from Load import Loader

import pickle
import table_maker as tm

_MAIN_FILE_PATH = "Amendments.bin"

class Searcher(Loader):
    
    def __init__(self) -> None:
        super().__init__()

################################################################################################

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

##############################################################################################################################
        
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

####################################################################################################################################

    def search_by_local(self):
        
        main_file = open(_MAIN_FILE_PATH, 'rb')

        print("Entre com o nome da localidade: ")
        local_name = input()

        if local_name not in self.states_record.keys():
            print("Localidade inválida")
            return
        
        pointers = self.states_record[local_name]
        
        amendments = []

        for address in pointers:
            print(address)
            main_file.seek(address)
            amendments.append(pickle.load(main_file))

        cols = ['Ano', 'Autor', 'Valor', 'Área', 'Estado']
        rows = []

        total_value = 0  #total gasto nessa localidade
        quantity = 0     #total de emendas nessa localidade

        for a in amendments:
            print(a[self.indices['value']])
            quantity += 1
            total_value += a[self.indices['value']]
            rows.append([str(a[self.indices['year']]),a[self.indices['author']], 
                         f"{round(a[self.indices['value']], 3)}", a[self.indices['function']], a[self.indices['state']]])
        
     #   for row in tm.make_table(cols,rows).split('\n'):
     #       print(row)
            
     #   totals_cols = ["Quantidade", "Valor Total"]
     #   totals_rows = [[f"{quantity:,}" ,f"{round(total_value, 3):,}"]]
        
     #   print(tm.make_table(totals_cols, totals_rows, scaling=2))

######################################################################################################################################

    def show_total_by_year(self):

        main_file = open(_MAIN_FILE_PATH, 'rb')
        
        valor_por_ano = Hash()
        
        while True:
            try:
                emenda = pickle.load(main_file)

                if valor_por_ano[str(emenda[self.indices['year']])] == None:
                    valor_por_ano[str(emenda[self.indices['year']])] = [emenda[self.indices['value']], 1]

                else:
                    valor_por_ano[str(emenda[self.indices['year']])][0] += emenda[self.indices['value']]
                    valor_por_ano[str(emenda[self.indices['year']])][1] += 1

            except EOFError:
                break  

        cols = ['Ano', 'Valor', 'Quantidade']
        rows = []
        
        for key in valor_por_ano.keys():
            rows.append([f"{key}", f"{round(valor_por_ano[key][0], 3):,}", f"{valor_por_ano[key][1]}"]) #ano, valor, quantidade
            
        for row in tm.make_table(cols,rows).split('\n'):
            print(row)
        
##################################################################################################################################

    def show_total_by_function(self):

        main_file = open(_MAIN_FILE_PATH, 'rb')

        valores_por_função = Hash ()

        for key in self.functions_pointers.keys():
             pointers = self.functions_pointers[key]

             for pointer in pointers:
                main_file.seek(pointer)     #offset no arquivo principal 
                emenda = pickle.load(main_file) #carrega do arquivo principal

                if valores_por_função[emenda[self.indices['function']]] == None:
                    valores_por_função[emenda[self.indices['function']]] = [emenda[self.indices['value']], 1]
                else:
                    valores_por_função[emenda[self.indices['function']]][0] += emenda[self.indices['value']]
                    valores_por_função[emenda[self.indices['function']]][1] += 1

        cols = ['Função', 'Valor', 'Quantidade']
        rows = []

        for key in valores_por_função.keys():
            rows.append([key,f"{round(valores_por_função[key][0],3):,}", f"{valores_por_função[key][1]}"]) #função, valor,quantidade
        
        for row in tm.make_table(cols=cols, rows=rows).split('\n'):
            print(row)

######################################################################################################################################

    def show_total_by_locality(self):

        main_file = open(_MAIN_FILE_PATH, 'rb')

        valores_por_estado = Hash()

        for key in self.states_record.keys():
            pointers = self.states_record[key]

            for pointer in pointers:
                main_file.seek(pointer)     #offset no arquivo principal 
                emenda = pickle.load(main_file) #carrega do arquivo principal
                
                if valores_por_estado[emenda[self.indices['state']]] == None:
                    valores_por_estado[emenda[self.indices['state']]] = [emenda[self.indices['value']], 1]
                else:
                    valores_por_estado[emenda[self.indices['state']]][0] += emenda[self.indices['value']]
                    valores_por_estado[emenda[self.indices['state']]][1] += 1
        
        cols = ['Local', 'Valor', 'Quantidade']
        rows = []

        for key in valores_por_estado.keys():
            rows.append([key,f"{round(valores_por_estado[key][0],3):,}", f"{valores_por_estado[key][1]}"]) #local,valor,quantidade
        
        for row in tm.make_table(cols=cols, rows=rows).split('\n'):
            print(row)

   
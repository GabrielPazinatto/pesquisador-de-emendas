from Hash import Hash
from Load import Loader
from quicksort import quicksort_iterative

import pickle
from tabulate import tabulate


_MAIN_FILE_PATH = "Amendments.bin"


class Searcher(Loader):
    
    def __init__(self) -> None:
        super().__init__()

################################################################################################
    #Busca por as emendas por função utilizando o arquivo invertido
    def search_by_function(self, ascending: bool):

        #Abertura do arquivo principal
        main_file = open(_MAIN_FILE_PATH, 'rb')

        print("Entre com o nome da função: ")
        function_name = input() 

        #Valida a função
        if function_name not in self.functions_pointers.keys():
            print("Função inválida.")
            return
        
        #Salva a lista de ponteiros (offset) para essa emendas 
        pointers = self.functions_pointers[function_name]

        amendments = []

        #Carrega as emendas do arquivo principal 
        for pointer in pointers:
            main_file.seek(pointer)     #offset no arquivo principal 
            amendments.append(pickle.load(main_file)) #carrega do arquivo principal

        main_file.close()

        amendments = quicksort_iterative(amendments, ascending)

        quantity = 0 #Total de emendas dessa função
        total_value = 0 #Total gasto nessa área (Saúde, Educação..)

        cols = ['Ano', 'Autor', 'Valor', 'Área', 'Estado']
        rows = []
        #Salva as informações da emenda por linha
        for a in amendments:
            quantity += 1
            total_value += a[self.indices['value']]
            rows.append([str(a[self.indices['year']]),a[self.indices['author']], f"{round(a[self.indices['value']], 3)}", 
                         a[self.indices['function']], a[self.indices['state']]])

        for row in tabulate(rows, cols, disable_numparse=True).split('\n'):
            print(row)
        
        totals_cols = ["Quantidade", "Valor Total", "Área"]
        totals_rows = [[f"{quantity:,}" ,f"{round(total_value, 3):,}", function_name]]
        
        print('\n',tabulate(totals_rows, totals_cols, disable_numparse=True),'\n')

##############################################################################################################################
    #Busca as emendas pelo autor
    def search_by_author(self, ascending: bool):
        
        #Abertura do arquivo principal
        main_file = open(_MAIN_FILE_PATH, 'rb')
        
        print("Entre com o nome do parlamentar: ")
        author_name = input()
        
        #Procura na TRIE o offset pelos nomes dos parlamentares 
        amendments_addr = self.authors_record.search_by_prefix(author_name)
        
        #Valida o nome dado na entrada
        if amendments_addr == None:
            print("Nome não consta.\n")
            return

        amendments = []

        #Busca os offsets no arquivo principal
        for address in amendments_addr:
            main_file.seek(address)
            amendments.append(pickle.load(main_file))

        main_file.close()

        amendments = quicksort_iterative(amendments, ascending)

        #Parametros das emendas
        cols = ['Ano', 'Autor', 'Valor', 'Área', 'Estado']
        rows = []

        total_value = 0 #total de gasto desse parlamentar
        quantity = 0    #quantidade de emendas desse parlamentar 
        
        #Salva as informações de cada emenda por linha
        for a in amendments:
            quantity += 1
            total_value += a[self.indices['value']]
            # print(a[self.indices['value']]) ta certo 
            rows.append([str(a[self.indices['year']]),a[self.indices['author']], 
                         f"{round(a[self.indices['value']], 3)}", a[self.indices['function']], a[self.indices['state']]])
        
        for row in tabulate(rows, cols, disable_numparse=True).split('\n'):
            print(row)
        
        #Mostra a quantidade total de emendas e o valor total das emendas desse parlamentar 
        totals_cols = ["Quantidade", "Valor Total"]
        totals_rows = [[f"{quantity:,}" ,f"{round(total_value, 3):,}"]] 
        
        print('\n',tabulate(totals_rows, totals_cols, disable_numparse=True),'\n')

####################################################################################################################################
    #Busca as emendas por localidade (Estado, região do Brasil, ou Exterior)
    def search_by_local(self, ascending: bool):
        #Abertura do arquivo principal
        main_file = open(_MAIN_FILE_PATH, 'rb')

        print("Entre com o nome da localidade: ")
        local_name = input()

        #Confere se a localidade de entrada é válida 
        if local_name not in self.states_record.keys():
            print("Localidade inválida")
            return
        
        #Salva a lista de offsets para as emendas dessa localidade
        pointers = self.states_record[local_name]
        
        #Lista para armazenas as emendas
        amendments = []

        #Busca pelos offsets
        for address in pointers:
            main_file.seek(address)
            amendments.append(pickle.load(main_file))

        main_file.close()
        
        amendments = quicksort_iterative(amendments, ascending)

        #Parametros das emendas
        cols = ['Ano', 'Autor', 'Valor', 'Área', 'Estado']
        rows = []

        total_value = 0  #total gasto nessa localidade
        quantity = 0     #total de emendas nessa localidade

        #Salva as informações das emendas por linha
        for a in amendments:
            quantity += 1
            total_value += a[self.indices['value']]
            rows.append([str(a[self.indices['year']]),a[self.indices['author']], 
                        f"{round(a[self.indices['value']], 3)}", a[self.indices['function']], a[self.indices['state']]])
            
        #Mostra as emendas
        for row in tabulate(rows, cols, disable_numparse=True).split('\n'):
            print(row)
        
        #Mostra o a quantidade total de emendas e o valor total delas 
        totals_cols = ["Quantidade", "Valor Total"]
        totals_rows = [[f"{quantity:,}" ,f"{round(total_value, 3):,}"]]
        
        print('\n',tabulate(totals_cols, totals_rows, disable_numparse=True),'\n')

###############################################################
#   FUNÇÕES QUE PROCESSAM TODAS AS INFORMAÇÕES DO ARQUIVO 
###############################################################

    #Mostra a quantidade total de emendas por ano e o valor total desembolsado com emendas naquele ano
    def show_total_by_year(self):

        #Abertura do arquivo principal 
        main_file = open(_MAIN_FILE_PATH, 'rb')
        
        #Hash para armazezenar os valores e quantidades pela key
        value_by_year = Hash()
        
        #Loop para processar o arquivo 
        while True:
            try:
                emenda = pickle.load(main_file) #Carrega a emenda

                if value_by_year[str(emenda[self.indices['year']])] == None:    #Se ela ainda não está na Hash
                    value_by_year[str(emenda[self.indices['year']])] = [emenda[self.indices['value']], 1] #Adiciona o primeiro valor

                else:
                    value_by_year[str(emenda[self.indices['year']])][0] += emenda[self.indices['value']] #Soma o valor de cada emenda ao total da key
                    value_by_year[str(emenda[self.indices['year']])][1] += 1 #Conta a quantidade 

            except EOFError:
                break  

        main_file.close()
        
        #Define as colunas a serem exibidas 
        cols = ['Ano', 'Valor', 'Quantidade']
        rows = []
        
        #Para cada key (ano), salva o ano, o valor total e a quantidade 
        for key in value_by_year.keys():
            rows.append([f"{key}", f"{round(value_by_year[key][0], 3):,}", f"{value_by_year[key][1]}"]) #ano, valor, quantidade
        
        #Apresenta os dados
        for row in tabulate(rows, cols, disable_numparse=True).split('\n'):
            print(row)
        
##################################################################################################################################

    #Mostra o total gasto e a quantidade total de emendas por função/área 
    def show_total_by_function(self):

        #Abertura do arquivo principal
        main_file = open(_MAIN_FILE_PATH, 'rb')

        value_by_function = Hash ()

        #Utiliza os offsets do arquivo invertido 
        for key in self.functions_pointers.keys():
             #Salva os offstes de cada key (função)
             pointers = self.functions_pointers[key]
             print(key)

             for pointer in pointers:
                main_file.seek(pointer)     #offset no arquivo principal 
                emenda = pickle.load(main_file) #carrega do arquivo principal

                if value_by_function[emenda[self.indices['function']]] == None: #Se ainda não está na Hash
                    value_by_function[emenda[self.indices['function']]] = [emenda[self.indices['value']], 1] #Adiciona o primeiro valor
                else:
                    value_by_function[emenda[self.indices['function']]][0] += emenda[self.indices['value']] #Soma ao valor total 
                    value_by_function[emenda[self.indices['function']]][1] += 1 #Soma as quantidades 

        main_file.close()

        #Define as colunas a serem exibidas
        cols = ['Função', 'Valor', 'Quantidade']
        rows = []

        #Para cada key (função), salva a key, valor total desembolsado e a quantidade total
        for key in value_by_function.keys():
            rows.append([key,f"{round(value_by_function[key][0],3):,}", f"{value_by_function[key][1]}"]) #função, valor,quantidade

        #Mostra as informações
        for row in tabulate(rows, cols, disable_numparse=True).split('\n'):
            print(row)

######################################################################################################################################
    #Mostra o total gasto e a quantidade total de emendas por localidade (Estado, região do Brasil ou Exterior)
    def show_total_by_locality(self):

        #Abertura do arquivo principal
        main_file = open(_MAIN_FILE_PATH, 'rb')

        value_by_local = Hash()

        #Utiliza os offsets do arquivo invertido 
        for key in self.states_record.keys():
            pointers = self.states_record[key]

            for pointer in pointers:
                main_file.seek(pointer)     #offset no arquivo principal 
                emenda = pickle.load(main_file) #carrega do arquivo principal
                
                if value_by_local[emenda[self.indices['state']]] == None: #Se ainda não está na Hash 
                    value_by_local[emenda[self.indices['state']]] = [emenda[self.indices['value']], 1] #Adiciona o primeiro valor e a quantidade 
                else:
                    value_by_local[emenda[self.indices['state']]][0] += emenda[self.indices['value']] #Soma o valor total
                    value_by_local[emenda[self.indices['state']]][1] += 1 #Soma as quantidades
            
        main_file.close()

        #Define as colunas a serem apresentadas
        cols = ['Local', 'Valor', 'Quantidade']
        rows = []

        #Para cada key(localida), salva a key, o valor total e a quantidade total em uma linha
        for key in value_by_local.keys():
            rows.append([key,f"{round(value_by_local[key][0],3):,}", f"{value_by_local[key][1]}"]) #local,valor,quantidade

        #Apresenta os dados
        for row in tabulate(rows, cols, disable_numparse=True).split('\n'):
            print(row)



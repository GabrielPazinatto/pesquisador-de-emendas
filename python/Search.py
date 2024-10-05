from .Hash import Hash
from .Load import Loader

import pickle
from operator import itemgetter

_MAIN_FILE_PATH = "bin/Amendments.bin"

class Searcher(Loader):
    
    def __init__(self) -> None:
        super().__init__()

################################################################################################
    #Busca por as emendas por função utilizando o arquivo invertido
    def search_by_function(self, function_name:str, ascending: bool, page_size:int = 100, page:int = 0, key:str = 'value'):

        #Abertura do arquivo principal
        main_file = open(_MAIN_FILE_PATH, 'rb')
                
        #Valida a função
        if function_name not in self.functions_pointers.keys():
            return {'amendments': None, 
                'quantity' : 0, 
                'total_value': 0}	
        
        #Salva a lista de ponteiros (offset) para essa emendas 
        pointers = self.functions_pointers[function_name]

        amendments = []

        #Carrega as emendas do arquivo principal
        for pointer in pointers:
            main_file.seek(pointer)     #offset no arquivo principal 
            amendments.append(pickle.load(main_file)) #carrega do arquivo principal

        main_file.close()

        quantity = 0 #Total de emendas dessa função
        total_value = 0 #Total gasto nessa área (Saúde, Educação..)
        
        #Salva as informações da emenda por linha
        for a in amendments:
            quantity += 1
            total_value += a['value']

        amendments.sort(key=itemgetter(key), reverse = not ascending)

        return {'amendments': amendments[page*page_size:(page + 1)*page_size], 
                'quantity' : quantity, 
                'total_value': total_value}

##############################################################################################################################
    #Busca as emendas pelo autor
    def search_by_author(self, author_name:str = None, ascending:bool = True, page_size:int = 100, page:int = 0, key:str = 'value'):
        
        #Abertura do arquivo principal
        main_file = open(_MAIN_FILE_PATH, 'rb')
        
        if author_name == None:
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

        amendments.sort(key=itemgetter(key), reverse = not ascending)
        
        #Salva as informações da emenda por linha
        quantity = 0
        total_value = 0
        for a in amendments:
            quantity += 1
            total_value += a['value']

        return {'amendments': amendments[page*page_size:(page + 1)*page_size], 
                'quantity' : quantity, 
                'total_value': total_value}

####################################################################################################################################
    #Busca as emendas por localidade (Estado, região do Brasil, ou Exterior)
    def search_by_local(self, local_name:str = None, ascending:bool = True, page_size:int = 100, page:int = 0, key:str = 'value'):
        #Abertura do arquivo principal
        main_file = open(_MAIN_FILE_PATH, 'rb')

        #Confere se a localidade de entrada é válida 
        if local_name not in self.locals_record.keys():
            print("Localidade inválida")
            return
        
        #Salva a lista de offsets para as emendas dessa localidade
        pointers = self.locals_record[local_name]
        
        #Lista para armazenas as emendas
        amendments = []

        #Busca pelos offsets
        for address in pointers:
            main_file.seek(address)
            amendments.append(pickle.load(main_file))

        main_file.close()
        
        amendments.sort(key=itemgetter(key), reverse = not ascending)
        
        #Salva as informações da emenda por linha
        total_value = 0  #total gasto nessa localidade
        quantity = 0     #total de emendas nessa localidade
        for a in amendments:
            quantity += 1
            total_value += a['value']

        return {'amendments': amendments[page*page_size:(page + 1)*page_size], 
                'quantity' : quantity, 
                'total_value': total_value}


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

        return [value_by_year[key] for key in value_by_year.keys()]
        
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

             for pointer in pointers:
                main_file.seek(pointer)     #offset no arquivo principal 
                emenda = pickle.load(main_file) #carrega do arquivo principal

                if value_by_function[emenda[self.indices['function']]] == None: #Se ainda não está na Hash
                    value_by_function[emenda[self.indices['function']]] = [emenda[self.indices['value']], 1] #Adiciona o primeiro valor
                else:
                    value_by_function[emenda[self.indices['function']]][0] += emenda[self.indices['value']] #Soma ao valor total 
                    value_by_function[emenda[self.indices['function']]][1] += 1 #Soma as quantidades 

        main_file.close()

        return [value_by_function[key] for key in value_by_function.keys()]

######################################################################################################################################
    #Mostra o total gasto e a quantidade total de emendas por localidade (Estado, região do Brasil ou Exterior)
    def show_total_by_locality(self):

        #Abertura do arquivo principal
        main_file = open(_MAIN_FILE_PATH, 'rb')

        value_by_local = Hash()

        #Utiliza os offsets do arquivo invertido 
        for key in self.locals_record.keys():
            pointers = self.locals_record[key]

            for pointer in pointers:
                main_file.seek(pointer)     #offset no arquivo principal 
                emenda = pickle.load(main_file) #carrega do arquivo principal
                
                if value_by_local[emenda[self.indices['local']]] == None: #Se ainda não está na Hash 
                    value_by_local[emenda[self.indices['local']]] = [emenda[self.indices['value']], 1] #Adiciona o primeiro valor e a quantidade 
                else:
                    value_by_local[emenda[self.indices['local']]][0] += emenda[self.indices['value']] #Soma o valor total
                    value_by_local[emenda[self.indices['local']]][1] += 1 #Soma as quantidades
            
        main_file.close()

        return [value_by_local[key] for key in value_by_local.keys()]

from data_handler import generate_bin_files
from Hash import Hash
import pickle
from Trie import Trie
import time
import os
import table_maker as tm

#################################
#    MAPEAMENTO DE INDICES
#################################
indices = Hash(
    entries={
        'uid' : 0,
        'value' : 1,
        'state' : 2,
        'function' : 3,
        'author' : 4,
        'year' : 5,
    })
################################
#  MAPEAMENTO DE PONTEIROS PARA 
#      EMENDAS POR FUNÇÃO
################################
functions_pointers = Hash(
    entries={
    'Saúde' : None,
    'Educação' : None,
    'Urbanismo' : None,
    'Agricultura' : None,
    'Assistência social' : None,
    'Outros' : None
})
#################################
#       VARIÁVEIS GLOBAIS
#################################
pointers_file = None
main_file = None
authors_file = None
authors:Trie = None
################################


def search_by_author():
    
    print("Entre com o nome do parlamentar: ")
    author_name = input()
    
    amendments_addr = authors.search(author_name)
    
    if amendments_addr == None:
        print("Nome não consta.\n")
        return

    amendments = []
    for address in amendments_addr:
        main_file.seek(address)
        amendments.append(pickle.load(main_file))
        
    cols = ['Ano', 'Valor', 'Área', 'Estado']
    rows = []
    
    for a in amendments:
        rows.append([str(a[indices['year']]), str(a[indices['value']]), a[indices['function']], a[indices['state']]])
    
    print(tm.make_table(cols, rows))
    
    
def load_data():
    # Faz a função atualizar as variáveis declaradas globalmente
    global pointers_file
    global main_file
    global authors_file
    global functions_pointers
    global authors
    
    # Abre os arquivos binários    
    pointers_file = open("Pointers.bin", 'rb')
    main_file = open("Amendments.bin", 'rb')
    authors_file = open("Authors.bin", 'rb')
    
    # Atualiza o mapeamento de ponteiros para emenda por função
    functions_pointers['Saúde'] = pickle.load(pointers_file)
    functions_pointers['Educação'] = pickle.load(pointers_file)
    functions_pointers['Urbanismo'] = pickle.load(pointers_file)
    functions_pointers['Agricultura'] = pickle.load(pointers_file)
    functions_pointers['Assistência social'] = pickle.load(pointers_file)
    functions_pointers['Outros'] = pickle.load(pointers_file)
    
    # Carrega em memória os ponteiros mapeados por autor de emenda
    authors = pickle.load(authors_file)

#################################################
#           GERA OS ARQUIVOS BINÁRIOS
def update_data_set():
    start = time.process_time()
    print("Atualizando base de dados...") 
    generate_bin_files("Emendas.csv")
    print("Base de dados atualizada em ", 
          time.process_time() - start, "s!")
    
#################################################
#                   MAIN
if __name__ == '__main__':
 
    print("Inicializando...")
    start = time.process_time()
    load_data()
    print("Programa inicializado em ",time.process_time() - start, 's!')
 
    choice = ''   
    
    while choice != '!':
        print("(0) Atualizar base de dados.")
        print("(1) Buscar emendas por nome do autor.")
        print("(!) Encerrar.")
        
        try:
            choice = int(input())
        except: choice = ''
    
        match(choice):
            case 0:
                update_data_set()
            case 1:
                search_by_author()
            case '!':
                exit()
            case _:
                print("Escolha inválida.")
                
            
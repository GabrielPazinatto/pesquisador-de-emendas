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
    
    amendments_addr = authors.search_by_prefix(author_name)
    
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
        total_value += a[indices['value']]
        rows.append([str(a[indices['year']]),a[indices['author']], f"{round(a[indices['value']], 3)}", a[indices['function']], a[indices['state']]])
    
    for row in tm.make_table(cols,rows).split('\n'):
        print(row)
        
    totals_cols = ["Quantidade", "Valor Total"]
    totals_rows = [[f"{quantity:,}" ,f"{round(total_value, 3):,}"]]
    
    print(tm.make_table(totals_cols, totals_rows, scaling=2))
    
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
    load_data()
    print("Base de dados atualizada em ", 
          time.process_time() - start, "s!")
    
#################################################
#                   MAIN
if __name__ == '__main__':
 
    print("Inicializando...")
    start = time.process_time()
    
    try:
        load_data()
    except:
        print("Dados não gerados!")
    
    print("Programa inicializado em ",time.process_time() - start, 's!')
 
    choice = ''   
    
    while True:
        print("(1) Atualizar base de dados.")
        print("(2) Buscar emendas por nome do autor.")
        print("(0) Encerrar.")
        
        choice = input()
    
        match(choice):
            case '1':
                update_data_set()
            case '2':
                search_by_author()
            case '0':
                exit()
            case _:
                print("Escolha inválida.")
                
            
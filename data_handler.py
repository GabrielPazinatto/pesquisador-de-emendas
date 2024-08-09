import pandas as pd
import pickle
from Hash import Hash
from Trie import Trie

##########################################################################
#                           FUNCIONAMENTO DO PROGRAMA
#
# Dados coletados de "Emendas.csv"
# 
# Dados normalizados e armazenados em listas da seguinte maneira:
# [uid, value, state, function, author, year]
# 
# Armazena-se cada lista sequencialmente no arquivo "Amendments.bin" (cada carregamento
# retorna uma emenda).
# 
# Gera-se um arquivo invertido "Pointers.bin", o qual, para cada carregamento realizado,
# retorna uma lista de ponteiros para emendas mapeadas por função, na mesma 
# ordem encontrada na variável functions_record.
# 
# Quando cada emenda é processada, é armazenado o nome de seu autor em uma
# árvore Trie. Ele é utilizado para indexar uma lista de ponteiros para todas as 
# emendas atreladas a esse nome. Então, gera-se um terceiro arquivo "Authors.bin",
# onde é armazanada a árvore.
# 
##########################################################################

# Dicionário de mapeamento de funções para emendas
functions_record = Hash(
    entries={
    'Saúde' : [],
    'Educação' : [],
    'Urbanismo' : [],
    'Agricultura' : [],
    'Assistência social' : [],
    'Outros' : []
})

# Árvore de indexação de Autores para emendas
authors_record = Trie()

##########################################################################

# Atualiza a árvore de índices de autores para emendas
def update_authors_record(item, main_file):
    authors_record.update_key(item['author'], main_file.tell())

# Atualiza o registro de emendas por função
def update_functions_record(item, main_file):
    # Se a função não for uma das escolhidas, é armazenada como "Outros"
    if item['function'] not in functions_record.keys():
        functions_record['Outros'].append(main_file.tell())
    else:
        functions_record[item['function']].append(main_file.tell())

##########################################################################

# Armazena a árvore Trie em um arquivo binário
def generate_authors_file(file, pointers:Trie = authors_record):
    pickle.dump(file=file, obj=pointers)

# Armazena as listas de ponteiros para emendas por função
def generate_pointers_file(file, pointers = functions_record):
    for key in ['Saúde', 'Educação', 'Urbanismo', 'Agricultura', 'Assistência social', 'Outros']:
        item = pointers[key]
        pickle.dump(file = file, obj=item)
            
# Gera o arquivo principal e armazena informações sobre as emendas
# para geração dos demais arquivos.
def generate_main_file(chunk, rows_read:int, main_file):
    chunk = chunk.to_dict(orient = 'records')
    
    # Gera um id unico para cada emenda
    uids = [i for i in range(rows_read, rows_read + len(chunk))]

    for i in range(len(chunk)):
        row = chunk[i]
        
        # Entrada do armazenamento principal
        item = process_entry(row, uids[i])
        
        # Gera listas de ponteiro para itens de cada função
        update_functions_record(item=item, main_file= main_file)
        # Atualiza a árvore Trie com os nomes presentes no csv e suas respectivas emendas
        update_authors_record(item = item, main_file = main_file)
        
        # Transforma os itens do dicionário em uma lista, tornando o armazenamento mais eficiente
        item = [item['uid'], item['value'], item['state'], item['function'], item['author'], item['year']]
         
        # Insere entrada (emenda) no arquivo de armazenamento principal
        pickle.dump(file= main_file, obj= item)


def generate_bin_files(input_file_path: str, chunk_size:int = 100000, offsets:list = []):
    
    # Abre os arquivos a serem escritos e passa por referência para as funções
    # Evita que sejam abertos múltiplas vezes
    main_file = open("Amendments.bin", "wb+")
    pointers_file = open("Pointers.bin", "wb+")
    authors_file = open("Authors.bin", "wb+")
    
    # Lê o arquivo de 100.000 em 100.000 linhas
    rows_read = 0
    for chunk in pd.read_csv(
        input_file_path, encoding='ISO-8859-15',
        on_bad_lines='warn', header=0, sep=';',
        low_memory=False, chunksize=chunk_size):
        
        # Arquivo que armazena todas as entradas
        generate_main_file(chunk, rows_read, main_file)
    
    # Arquivos invertidos
    generate_pointers_file(file = pointers_file, pointers = functions_record)
    generate_authors_file(file = authors_file, pointers = authors_record)
        
    authors_file.close()
    main_file.close()
    pointers_file.close()
    
# Processa uma entrada do arquivo csv
def process_entry(row:pd.DataFrame, uid:int)->list:

    item = Hash(
        entries={
        'uid' : -1,
        'value' : 0,
        'state' : '',
        'function' : '',
        'author' : '',
        'year' : -1        
    }, size = 6)

    # Transforma a entrada em um dicionário

    value = 0
    value += float(row["Valor Empenhado"].replace(',', '.'))
    value += float(row["Valor Liquidado"].replace(',', '.'))
    value += float(row["Valor Pago"].replace(',', '.'))
    value += float(row["Valor Restos A Pagar Inscritos"].replace(',', '.'))
    value += float(row["Valor Restos A Pagar Cancelados"].replace(',', '.'))
    value += float(row["Valor Restos A Pagar Pagos"].replace(',', '.'))

    item['uid'] = uid
    item['value'] = value
    item['state'] = (_get_state_name(row['Localidade do gasto']))
    item['function'] = (row["Nome Função"])
    item['author'] = (row["Nome do Autor da Emenda"])
    item['year'] = (int(row["Ano da Emenda"]))      
    
    return item


# Dado um campo "localidade" de uma emenda, retorna o estado mencionado na string
# NORMALIZAR!!!!!!!!!
def _get_state_name(s:str):
    if 'UF' in s:
        for i in range(len(s)):
            if s[i] == '(':
                return s[:i-1]
    
    for i in range(len(s)):
        if s[i] == '-':
            return s[i+2:i+4]
        
    return "União"



import pandas as pd
import pickle
from Hash import Hash
from Trie import Trie

functions = Hash(
    entries={
    'Saúde' : 0,
    'Educação' : 1,
    'Urbanismo' : 2,
    'Agricultura' : 3,
    'Assistência social' : 4,
    'Outros' : 5
})

functions_record = Hash(
    entries={
    'Saúde' : [],
    'Educação' : [],
    'Urbanismo' : [],
    'Agricultura' : [],
    'Assistência social' : [],
    'Outros' : []
})

authors_record = Trie()

def generate_authors_file(file, pointers:Trie = authors_record):
    pickle.dump(file=file, obj=pointers)

def update_authors_record(item, main_file):
    authors_record.update_key(item['author'], main_file.tell())

def update_functions_record(item, main_file):
    if item['function'] not in functions.keys():
        functions_record['Outros'].append(main_file.tell())
    else:
        functions_record[item['function']].append(main_file.tell())
            
def generate_main_file(chunk, rows_read:int, main_file):
    chunk = chunk.to_dict(orient = 'records')
    uids = [i for i in range(rows_read, rows_read + len(chunk))]

    for i in range(len(chunk)):
        row = chunk[i]
        
        # Entrada do armazenamento principal
        item = process_entry(row, uids[i])
        
        # Gera listas de ponteiro para itens de cada função
        update_functions_record(item=item, main_file= main_file)
        update_authors_record(item = item, main_file = main_file)
        
        item = [item['uid'], item['value'], item['state'], item['function'], item['author'], item['year']]
         
        # Insere entrada no arquivo de armazenamento principal
        pickle.dump(file= main_file, obj= item)
                    
def generate_pointers_file(file, pointers = functions_record):
    for key in ['Saúde', 'Educação', 'Urbanismo', 'Agricultura', 'Assistência social', 'Outros']:
        item = pointers[key]
        pickle.dump(file = file, obj=item)

def generate_bin_files(input_file_path: str, chunk_size:int = 100000, offsets:list = []):
    main_file = open("Amendments.bin", "wb+")
    pointers_file = open("Pointers.bin", "wb+")
    authors_file = open("Authors.bin", "wb+")
    
    rows_read = 0
    for chunk in pd.read_csv(
        input_file_path, encoding='ISO-8859-15',
        on_bad_lines='warn', header=0, sep=';',
        low_memory=False, chunksize=chunk_size):
        
        generate_main_file(chunk, rows_read, main_file)
    
    generate_pointers_file(file = pointers_file, pointers = functions_record)
    generate_authors_file(file = authors_file, pointers = authors_record)
        
    main_file.close()
    pointers_file.close()
    
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

def _get_state_name(s:str):
    if 'UF' in s:
        for i in range(len(s)):
            if s[i] == '(':
                return s[:i-1]
    
    for i in range(len(s)):
        if s[i] == '-':
            return s[i+2:i+4]
        
    return "União"



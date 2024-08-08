import pandas as pd
import pickle
from enum import Enum

class Indexes(Enum):
    UID = 0
    VALUE = 1
    STATE = 2
    FUNCTION = 3
    AUTHOR = 4
    YEAR = 5
    
class Functions(Enum):
    SAUDE = 0
    EDUCACAO = 1
    URBANISMO = 2
    AGRICULTURA = 3
    ASSISTENCIA_SOCIAL = 4
    OTHERS = 5

functions_record = [[],[],[],[],[],[]]

def update_functions_record(item, main_file):
    match item[Indexes.FUNCTION.value]:    
        case 'Saúde':
            functions_record[Functions.SAUDE.value].append(main_file.tell())
        case 'Educação':
            functions_record[Functions.EDUCACAO.value].append(main_file.tell())
        case 'Urbanismo':
            functions_record[Functions.URBANISMO.value].append(main_file.tell())
        case 'Agricultura':
            functions_record[Functions.AGRICULTURA.value].append(main_file.tell())
        case 'Assistência social':
            functions_record[Functions.ASSISTENCIA_SOCIAL.value].append(main_file.tell())
        case _:
            functions_record[Functions.OTHERS.value].append(main_file.tell())
            
            
def generate_main_file(chunk, rows_read:int, main_file, pointers_file):
    chunk = chunk.to_dict(orient = 'records')
    uids = [i for i in range(rows_read, rows_read + len(chunk))]

    for i in range(len(chunk)):
        row = chunk[i]
        
        # Entrada do armazenamento principal
        item = process_entry(row, uids[i])
        
        # Gera listas de ponteiro para itens de cada função
        update_functions_record(item=item, main_file= main_file)
         
        # Insere entrada no arquivo de armazenamento principal
        pickle.dump(file= main_file, obj= item)
        

                    
def generate_pointers_file(file, pointers = functions_record):
    for i in range(6):
        item = functions_record[i]
        #print(len(item))  
        pickle.dump(file = file, obj=item)
                    
    
def generate_bin_files(input_file_path: str, chunk_size:int = 100000, offsets:list = []):
    main_file = open("Amendments.bin", "wb+")
    pointers_file = open("Pointers.bin", "wb+")
    
    rows_read = 0
    for chunk in pd.read_csv(
        input_file_path, encoding='ISO-8859-15',
        on_bad_lines='warn', header=0, sep=';',
        low_memory=False, chunksize=chunk_size):
        
        generate_main_file(chunk, rows_read, main_file, pointers_file)
    
    generate_pointers_file(file = pointers_file, pointers = functions_record)
        
    main_file.close()
    pointers_file.close()
    
def process_entry(row:pd.DataFrame, uid:int)->list:
    item = [None]*6

    value = 0
    value += float(row["Valor Empenhado"].replace(',', '.'))
    value += float(row["Valor Liquidado"].replace(',', '.'))
    value += float(row["Valor Pago"].replace(',', '.'))
    value += float(row["Valor Restos A Pagar Inscritos"].replace(',', '.'))
    value += float(row["Valor Restos A Pagar Cancelados"].replace(',', '.'))
    value += float(row["Valor Restos A Pagar Pagos"].replace(',', '.'))

    item[Indexes.UID.value] = uid
    item[Indexes.VALUE.value] = value
    item[Indexes.STATE.value] = (_get_state_name(row['Localidade do gasto']))
    item[Indexes.FUNCTION.value] = (row["Nome Função"])
    item[Indexes.AUTHOR.value] = (row["Nome do Autor da Emenda"])
    item[Indexes.YEAR.value] = (int(row["Ano da Emenda"]))      
    
    return item
    

def _get_state_name(s:str):
    if 'UF' in s:
        return 'UF'
    
    for i in range(len(s)):
        if s[i] == '-':
            return s[i+2:i+4]
        
    return "União"




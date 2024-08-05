import pandas as pd
import random

def get_input_data(input_file_path: str, chunk_size:int = 100000):
    output = []
    
    rows_read = 0
    
    for chunk in pd.read_csv(
        input_file_path, encoding='ISO-8859-15',
        on_bad_lines='warn', header=0, sep=';',
        low_memory=False, chunksize=chunk_size):
        
        chunk = chunk.to_dict(orient = 'records')
        
        uids = random.sample(range(rows_read, rows_read + len(chunk)), len(chunk))
        rows_read += len(chunk)
        
        for i in range(len(chunk)):
            row = chunk[i]
            
            item = [None] * 6
        
            value = 0
            value += float(row["Valor Empenhado"].replace(',', '.'))
            value += float(row["Valor Liquidado"].replace(',', '.'))
            value += float(row["Valor Pago"].replace(',', '.'))
            value += float(row["Valor Restos A Pagar Inscritos"].replace(',', '.'))
            value += float(row["Valor Restos A Pagar Cancelados"].replace(',', '.'))
            value += float(row["Valor Restos A Pagar Pagos"].replace(',', '.'))

            item[0] = uids[i]
            item[1] = value
            item[2] = (_get_state_name(row['Localidade do gasto']))
            item[3] = (row["Nome Função"])
            item[4] = (row["Nome do Autor da Emenda"])
            item[5] = (int(row["Ano da Emenda"]))        
            
            output.append(item)
            
            i += 1
    return output

def _get_state_name(s:str):
    if 'UF' in s:
        return 'UF'
    
    for i in range(len(s)):
        if s[i] == '-':
            return s[i+2:i+4]
        
    return "União"


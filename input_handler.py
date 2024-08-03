import pandas as pd
import random

def import_data(input_file_path: str) -> pd.DataFrame:
    data = pd.read_csv(input_file_path, encoding='ISO-8859-15',
                    on_bad_lines='warn', header=0, sep=';',
                    low_memory=False)
    return data

def _get_state_name(s:str):
    if 'UF' in s:
        return 'UF'
    
    for i in range(len(s)):
        if s[i] == '-':
            return s[i+2:i+4]
        
    return "União"

def generate_data_set(data:pd.DataFrame) -> list[float]:
    data = data.to_dict(orient='records')
    output = [[]]*6
    
    uids = []
    values = []
    states = []
    years = []
    authors = []
    functions = []
    uids = random.sample(range(0, len(data)), len(data))
    
    for row in data:
        value = 0
        value += float(row["Valor Empenhado"].replace(',', '.'))
        value += float(row["Valor Liquidado"].replace(',', '.'))
        value += float(row["Valor Pago"].replace(',', '.'))
        value += float(row["Valor Restos A Pagar Inscritos"].replace(',', '.'))
        value += float(row["Valor Restos A Pagar Cancelados"].replace(',', '.'))
        value += float(row["Valor Restos A Pagar Pagos"].replace(',', '.'))
        values.append(value)
        
        functions.append(row["Nome Função"])
        years.append(int(row["Ano da Emenda"]))        
        authors.append(row["Nome do Autor da Emenda"])
        states.append(_get_state_name(row['Localidade do gasto']))
    
    output[0] = uids
    output[1] = values
    output[2] = states
    output[2] = functions
    output[3] = authors
    output[4] = years
            
    return output,len(data)
    
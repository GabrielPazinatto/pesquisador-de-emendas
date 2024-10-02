from python.Hash import Hash
from python.Trie import Trie

import pickle
import time
import unicodedata
import pandas as pd

class Updater:
    def __init__(self) -> None:      
        #################################
        #    MAPEAMENTO DE INDICES
        #################################
        
        self.functions_record = Hash(
            entries={
            'Saúde' : [],
            'Educação' : [],
            'Urbanismo' : [],
            'Agricultura' : [],
            'Assistência social' : [],
            'Outros' : []
        })
        
        ################################
        #  MAPEAMENTO DE PONTEIROS PARA 
        #      EMENDAS POR FUNÇÃO
        ################################
        self.functions_pointers = Hash(
            entries={
            'Saúde' : None,
            'Educação' : None,
            'Urbanismo' : None,
            'Agricultura' : None,
            'Assistência social' : None,
            'Outros' : None
        })
        
        ################################
        #  MAPEAMENTO DE PONTEIROS PARA 
        #      EMENDAS POR ESTADO
        ################################
        self.locals_record = Hash(
            entries={
            'AC': [],  # Acre
            'AL': [],  # Alagoas
            'AP': [],  # Amapá
            'AM': [],  # Amazonas
            'BA': [],  # Bahia
            'CE': [],  # Ceará
            'DF': [],  # Distrito Federal
            'ES': [],  # Espírito Santo
            'GO': [],  # Goiás
            'MA': [],  # Maranhão
            'MT': [],  # Mato Grosso
            'MS': [],  # Mato Grosso do Sul
            'MG': [],  # Minas Gerais
            'PA': [],  # Pará
            'PB': [],  # Paraíba
            'PR': [],  # Paraná
            'PE': [],  # Pernambuco
            'PI': [],  # Piauí
            'RJ': [],  # Rio de Janeiro
            'RN': [],  # Rio Grande do Norte
            'RS': [],  # Rio Grande do Sul
            'RO': [],  # Rondônia
            'RR': [],  # Roraima
            'SC': [],  # Santa Catarina
            'SP': [],  # São Paulo
            'SE': [],  # Sergipe
            'TO': [],   # Tocantins
            'CENTRO-OESTE' : [],
            'SUDESTE' : [],
            'SUL' : [],
            'NORTE' : [],
            'NORDESTE': [],
            'EXTERIOR':[]
    })

        ################################
        #  MAPEAMENTO DE PONTEIROS PARA 
        #      EMENDAS POR ESTADO
        ################################
        self.authors_record = Trie()

        ################################
        #  MAPEAMENTO DE PONTEIROS PARA 
        #      EMENDAS POR REGIAO
        ################################
        self.region_record = Hash(
            entries = {
            'CENTRO-OESTE' : [],
            'SUDESTE' : [],
            'SUL' : [],
            'NORTE' : [],
            'NORDESTE': []
        })
        
        ################################
        #   MAPEAMENTO DE ESTADOS  
        #       PARA ACRONIMOS
        ################################
        self.local_acronym = Hash(
            entries ={
                "ACRE": "AC",
                "ALAGOAS": "AL",
                "AMAPA": "AP",
                "AMAZONAS": "AM",
                "BAHIA": "BA",
                "CEARA": "CE",
                "DISTRITO FEDERAL": "DF",
                "ESPIRITO SANTO": "ES",
                "GOIAS": "GO",
                "MARANHAO": "MA",
                "MATO GROSSO": "MT",
                "MATO GROSSO DO SUL": "MS",
                "MINAS GERAIS": "MG",
                "PARA": "PA",
                "PARAIBA": "PB",
                "PARANA": "PR",
                "PERNAMBUCO": "PE",
                "PIAUI": "PI",
                "RIO DE JANEIRO": "RJ",
                "RIO GRANDE DO NORTE": "RN",
                "RIO GRANDE DO SUL": "RS",
                "RONDONIA": "RO",
                "RORAIMA": "RR",
                "SANTA CATARINA": "SC",
                "SAO PAULO": "SP",
                "SERGIPE": "SE",
                "TOCANTINS": "TO"
            })

##########################################################################

    def update_data_set(self):
        start = time.process_time()
        print("Atualizando base de dados...") 
        self._generate_bin_files("python/Emendas.csv")
        print("Base de dados atualizada em ", 
            time.process_time() - start, "s!")
        
##########################################################################
    
    def _generate_bin_files(self, input_file_path: str, chunk_size:int = 100000, offsets:list = []):
        
        # Abre os arquivos a serem escritos e passa por referência para as funções
        # Evita que sejam abertos múltiplas vezes
        main_file = open("bin/Amendments.bin", "wb+")
        pointers_file = open("bin/Pointers.bin", "wb+")
        authors_file = open("bin/Authors.bin", "wb+")
        local_file = open("bin/local.bin", "wb+")
        
        self.__init__()
        
        # Lê o arquivo de 100.000 em 100.000 linhas
        rows_read = 0
        for chunk in pd.read_csv(
            input_file_path, encoding='ISO-8859-15',
            on_bad_lines='warn', header=0, sep=';',
            low_memory=False, chunksize=chunk_size):
            
            # Arquivo que armazena todas as entradas
            self._generate_main_file(chunk, rows_read, main_file)
        
        # Arquivos invertidos
        self._generate_pointers_file(file = pointers_file)
        self._generate_authors_file(file = authors_file)
        self._generate_locals_file(file = local_file)

        authors_file.close()
        main_file.close()
        pointers_file.close()
        local_file.close()

##########################################################################

    # Gera o arquivo principal e armazena informações sobre as emendas
    # para geração dos demais arquivos.
    def _generate_main_file(self, chunk, rows_read:int, main_file):
        chunk = chunk.to_dict(orient = 'records')
        
        # Gera um id unico para cada emenda
        uids = [i for i in range(rows_read, rows_read + len(chunk))]

        for i in range(len(chunk)):
            row = chunk[i]
            
            # Entrada do armazenamento principal
            item = self._process_entry(row, uids[i])

            #Gera listas de ponteiro para itens de cada Estado
            self._update_locals_record(item = item, main_file = main_file)
            # Gera listas de ponteiro para itens de cada função
            self._update_functions_record(item=item, main_file= main_file)
            # Atualiza a árvore Trie com os nomes presentes no csv e suas respectivas emendas
            self._update_authors_record(item = item, main_file = main_file)
            
            # Transforma os itens do dicionário em uma lista, tornando o armazenamento mais eficiente
            item = {
                'uid': item['uid'], 
                'value': item['value'], 
                'local': item['local'], 
                'function': item['function'], 
                'author': item['author'], 
                'year': item['year']
            }
            
            # Insere entrada (emenda) no arquivo de armazenamento principal
            pickle.dump(file= main_file, obj= item)

##########################################################################

    # Atualiza a árvore de índices de autores para emendas
    def _update_authors_record(self, item, main_file):
        self.authors_record.update_key(item['author'], main_file.tell())

    # Atualiza o registro de emendas por função
    def _update_functions_record(self, item, main_file):
        # Se a função não for uma das escolhidas, é armazenada como "Outros"
        if item['function'] not in self.functions_record.keys():
            self.functions_record['Outros'].append(main_file.tell())
        else:
            self.functions_record[item['function']].append(main_file.tell())

    #Atualiza o resgistro de emendas por Localidade
    def _update_locals_record(self, item , main_file):
        #Se o Estado não estiver no dicionário, informa erro
        if item['local'] in self.locals_record.keys():
            self.locals_record[item['local']].append(main_file.tell()) #coloca o ponteiro para o arquivo principal no Estado ou Região correspondente
            

    ##########################################################################

    # Armazena a árvore Trie em um arquivo binário
    def _generate_authors_file(self, file):
        pointers = self.authors_record
        pickle.dump(file=file, obj=pointers)

    # Armazena as listas de ponteiros para emendas por função
    def _generate_pointers_file(self, file):
        for key in ['Saúde', 'Educação', 'Urbanismo', 'Agricultura', 'Assistência social', 'Outros']:
            item = self.functions_record[key]
            pickle.dump(file = file, obj=item)

    #Armazena as listas dos ponteiros das emendas por localidade
    def _generate_locals_file(self, file):
        pickle.dump(file = file, obj = self.locals_record)
            
##########################################################################
    # Processa uma entrada do arquivo csv
    def _process_entry(self, row:pd.DataFrame, uid:int)->list:

        item = Hash(
            entries={
            'uid' : -1,
            'value' : 0,
            'local' : '',
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
        value += float(row["Valor Restos A Pagar Pagos"].replace(',', '.'))

        item['uid'] = uid
        item['value'] = value
        
        item['local'] = (self._get_local_name(row['Localidade do gasto']))
        item['function'] = (row["Nome Função"])
        item['author'] = (row["Nome do Autor da Emenda"])
        item['year'] = (int(row["Ano da Emenda"]))      
        
        return item

##########################################################################
    # Dado um campo "localidade" de uma emenda, retorna o estado (sigla) mencionado na string
    def _get_local_name(self, s:str) -> str:

        #Padroniza as informações
        s = s.upper().strip()
        s = unicodedata.normalize('NFD', s)
        s = ''.join([c for c in s if not unicodedata.combining(c)])

        #Primeiro checa se não é uma região
        if s in self.region_record.keys():
            return s                #Se for, retorna a própria Região
        
        #Caso em "Cidade - Estado"
        if '-' in s:
            if s not in self.region_record.keys():
                parts = s.split('-')   
                return parts[-1].strip()
        
        #Caso "Rio Grande do Sul (UF)"
        if '(UF)' in s:
            local_name = s.replace('(UF)', '').strip()
            return self.local_acronym.get(local_name, "Formato inválido")
        
        #Casos especiais 
        if s == "NACIONAL" or s == "MULTIPLO":
            return "DF"
        
        if s == "EXTERIOR":
            return "EXTERIOR"
        

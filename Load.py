import pickle
from Update import Updater

class Loader(Updater):
    
    def __init__(self) -> None:
        super().__init__()
    
##########################################################################
    # Carrega os dados dos arquivos invertidos em memória
    def load_data(self):    
        # Abre os arquivos binários    
        pointers_file = open("Pointers.bin", 'rb')
        main_file = open("Amendments.bin", 'rb')
        authors_file = open("Authors.bin", 'rb')
        local_file = open("local.bin", 'rb')
        
        # Atualiza o mapeamento de ponteiros para emenda por função
        self.functions_pointers['Saúde'] = pickle.load(pointers_file)
        self.functions_pointers['Educação'] = pickle.load(pointers_file)
        self.functions_pointers['Urbanismo'] = pickle.load(pointers_file)
        self.functions_pointers['Agricultura'] = pickle.load(pointers_file)
        self.functions_pointers['Assistência social'] = pickle.load(pointers_file)
        self.functions_pointers['Outros'] = pickle.load(pointers_file)
        
        # Carrega em memória os ponteiros mapeados por autor de emenda
        self.authors_record = pickle.load(authors_file)
        
        pointers_file.close()
        main_file.close()
        local_file.close()
        authors_file.close()
        
##########################################################################


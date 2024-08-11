class Hash:
    def __init__(self, size:int = 31, entries = None) -> None:

        # Se entries for determinado, inicializa o tamanho
        # da tabela para corresponder ás entradas informadas
        if entries and len(entries.items()) - 1 != size:
            self.size = len(entries.items()) - 1
        else:
            self.size = size
        
        # Inicializa a tabela
        self.table = [[] for _ in range(self.size)]
        
        # Inicializa as entradas
        if entries != None:
            for key, value in entries.items():
                self[key] = value
                
    # Função de cálculo de endereço
    # Somatório do valor ascii dos digitos da chave % dimensão da tabela hash
    def hash(self, key:any) -> int:
        return sum(ord(c) for c in key) % self.size
        
    # Override do operador [] para buscar uma entrada
    def __getitem__(self, key:any) -> any:
        idx = self.hash(key=key)        # Calcula o endereço
        for entry in self.table[idx]:   # Busca linear na lista correspondente
            if entry[0] == key:         # Se não encontrar, retorna None
                return entry[1]
        return None
    
    # Override do operador [] para setar uma entrada
    def __setitem__(self, key:any, value:any):
        idx = self.hash(key=key)        # Calcula o enderenço
        for entry in self.table[idx]:   # Busca linear na lista correspondente
            if entry[0] == key:         # Se achar a chave, atualiza o valor
                entry[1] = value        # Se não, cria nova entrada
        self.table[idx].append([key, value])
        
    def keys(self) -> list[any]:        # Retorna todas as chaves 
        keys = []
        for row in self.table:
            for entry in row:
                keys.append(entry[0])
        return keys
    
    def items(self) ->list[any]:        # Retorna todos os valores
        items= []
        for row in self.table:
            for entry in row:
                items.append(entry[1])
        return items

    def get(self, key:any, default:any) ->list[any]:
        try:
            return self.__getitem__(key)
        except:
            return default
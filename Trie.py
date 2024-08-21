import unicodedata


##########################################################################
class _TrieNode:
    def __init__(self) -> None:
        self.children = [None for _ in range(26)]
        self.is_final = False
        self.value = None
##########################################################################
class Trie:
    def __init__(self) -> None:
        self.root: _TrieNode = _TrieNode()
##########################################################################
    # Insere uma tupla (key : value) na árvore
    def insert(self, key:str, value:any):
        # Gambiarra para remover todos os caracteres especiais e letras maiúsculas dos nomes
        key = unicodedata.normalize('NFKD', key).encode('ascii',errors='ignore').decode('ascii').lower()
        node = self.root
        
        for c in key:
            if c in [' ', '.', '-', ',', '\'']: continue
            # Acessa as sub-arvores correspondentes a cada caractere
            index = ord(c) - ord('a')
            if node.children[index] is None:         # Se não houver o nodo correspondente ao caractere, cria-o
                node.children[index] = _TrieNode()  
            node = node.children[index]
            
        node.is_final = True                         # Marca o Nodo como final e armazena as informações nele
        node.value = value
        
##########################################################################

    # Dada uma chave, retorna seu valor correspondente
    def search(self, key:str):
        # Gambiarra para remover todos os caracteres especiais e letras maiúsculas dos nomes
        key = unicodedata.normalize('NFKD', key).encode('ascii',errors='ignore').decode('ascii').lower()
        node = self.root
        for c in key:
            if c in [' ', '.', '-', ',', '\'']: continue
            # Acessa as sub-arvores correspondentes a cada caractere
            index = ord(c) - ord('a')
            if node.children[index] is None:   # Se o nodo correspondente ao caractere não existir,
                return None                    # a informação não está na árvore, retorna None
            else: node = node.children[index]  
            
        return node.value    
        
##########################################################################

    def update_key(self, key:str, new_value:any):
        # Gambiarra para remover todos os caracteres especiais e letras maiúsculas dos nomes
        key = unicodedata.normalize('NFKD', key).encode('ascii',errors='ignore').decode('ascii').lower()
        node = self.root
        
        for c in key:
            if c in [' ', '.', '-', ',', '\'']: continue
            index = ord(c) - ord('a')
            # Acessa as sub-arvores correspondentes a cada caractere
            if node.children[index] is None:
                node.children[index] = _TrieNode()
            node = node.children[index]
            
        node.is_final = True              
        try:
            node.value.append(new_value)    # Se o valor for uma lista, adiciona à lista
        except:                             # Se não, transforma em lista
            old_value = node.value
            node.value = [new_value]        
            if old_value != None:
                node.value.append(old_value)
                
##########################################################################
            
    def search_by_prefix(self, key:str):
        # Gambiarra para remover todos os caracteres especiais e letras maiúsculas dos nomes
        key = unicodedata.normalize('NFKD', key).encode('ascii',errors='ignore').decode('ascii').lower()
        node = self.root
            
        for c in key:
            if c in [' ', '.', '-', ',', '\'']: continue
            # Acessa as sub-arvores correspondentes a cada caractere
            index = ord(c) - ord('a')
            if node.children[index] is None:   # Consome cada caractere do prefixo
                return None                    # informado
            else: node = node.children[index]  
        
        output = []
        if node.value != None:
            output.extend(node.value)   
        
        if not node.is_final:
            for val in self._search_by_prefix_aux(node):    # Retorna todos os valores cujas chaves
                output.extend(val)                          # começam com o prefixo (visita todos os
                                                            # nodos em níveis mais baixos do atual)
        return output
        
    # Retorna todos os valores dos nodos abaixo do nodo informado
    def _search_by_prefix_aux(self,node):
        if node == None: return []
        
        output = []
        if node.is_final:
            output.append(node.value)
        for child in node.children:
            output.extend(self._search_by_prefix_aux(child))
            
        return output
##########################################################################
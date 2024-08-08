import unicodedata

class _TrieNode:
    def __init__(self) -> None:
        self.children = [None for _ in range(26)]
        self.is_final = False
        self.value = []
        
class Trie:
    def __init__(self) -> None:
        self.root: _TrieNode = _TrieNode()
        
    def insert(self, key:str, value:any):
        key = unicodedata.normalize('NFKD', key).encode('ascii',errors='ignore').decode('ascii').lower()
        node = self.root
        
        for c in key:
            if c in [' ', '.', '-', ',', '\'']: continue
            index = ord(c) - ord('a')
            if node.children[index] is None:
                node.children[index] = _TrieNode()
            node = node.children[index]
            
        node.is_final = True
        node.value = value
        
    def search(self, key:str):
        key = unicodedata.normalize('NFKD', key).encode('ascii',errors='ignore').decode('ascii').lower()
        node = self.root
        for c in key:
            if c in [' ', '.', '-', ',', '\'']: continue
            index = ord(c) - ord('a')
            if node.children[index] is None:
                return None
            else: node = node.children[index]
            
        return node.value    
        
    def update_key(self, key:str, new_value:any):
        key = unicodedata.normalize('NFKD', key).encode('ascii',errors='ignore').decode('ascii').lower()
        node = self.root
        
        for c in key:
            if c in [' ', '.', '-', ',', '\'']: continue
            index = ord(c) - ord('a')
            if node.children[index] is None:
                node.children[index] = _TrieNode()
            node = node.children[index]
            
        node.is_final = True
        try:
            node.value.append(new_value)
        except:
            node.value = [new_value]
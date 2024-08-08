class Hash:
    def __init__(self, size:int = 31, entries = None) -> None:

        if entries and len(entries.items()) - 1 != size:
            self.size = len(entries.items()) - 1
        else:
            self.size = size
        
        self.table = [[] for _ in range(self.size)]
        
        if entries != None:
            for key, value in entries.items():
                self[key] = value
                
    def hash(self, key:any) -> int:
        return sum(ord(c) for c in key) % self.size
        
    def __getitem__(self, key:any) -> any:
        idx = self.hash(key=key)
        for entry in self.table[idx]:
            if entry[0] == key:
                return entry[1]
        return None
    
    def __setitem__(self, key:any, value:any):
        idx = self.hash(key=key)
        for entry in self.table[idx]:
            if entry[0] == key:
                entry[1] = value
        self.table[idx].append([key, value])
        
    def keys(self) -> list[any]:
        keys = []
        for row in self.table:
            for entry in row:
                keys.append(entry[0])
        return keys
    
    def items(self) ->list[any]:
        items= []
        for row in self.table:
            for entry in row:
                items.append(entry[1])
        return items
    
    def __repr__(self):
        items = {item[0]: item[1] for sublist in self.table for item in sublist}
        return str(items)
# trabalho-cpd

## Passos

1. Faz a leitura do CSV que contém as emendas parlamentares

2. Separa cada emenda array de tamanho 7, utilizando uma Hash table para os índices, são eles:
    1. Identificador único (gerado ao ler o csv)
    2. Valor (soma dos valores, exceto os valores que foram cancelados)
    3. Localidade (Estado, Região ou Exterior)
    4. Função (Saúde, educação, etc)
    5. Autor (nome do legislador)
    6. Ano

3. Foram implementados dicionários (Hash table) para:
    1. Funções das emendas
    2. Localidades
    3. Nome das localidades e siglas

4. Implementação da árvore TRIE indexada pelos nomes dos parlamentares, com as funções:
    1. Inserção
    2. Busca

5. Durante a leitura e processamento dos dados do arquivo binário:
    1. Gera arquivo invertido que contém os offsets das emendas por função
    2. Gera arquivo invertido que contém os offsets das emendas por localidade
    3. Atualiza a TRIE indexada pelos nomes dos parlamentares e suas emendas
 
6. Implementada funções de busca que utilizam tanto os offstes dos arquivos invertidos quanto a TRIE para:
    1. Buscar as emendas por função
    2. Buscar as emendas por parlamentar
    3. Buscar as emendas por localidade 
    4. Mostra o valor total desembolsado e a quantidade total de emendas por ano 
    5. Mostra o valor total desembolsado e a quantidade total de emendas por função 
    6. Mostra o valor total desembolsado e a quantidade total de emendas por localidade


    
    

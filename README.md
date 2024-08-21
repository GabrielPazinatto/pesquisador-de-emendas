# trabalho-cpd

## Passos
1. Faz a leitura do CSV que contém as emendas parlamentares

1. Ler arquivo

2. Separar dados em um array de tamanho 7, com cada índice sendo:
    1. Identificador único (gerado ao ler o csv)
    2. Valor (soma dos valores, exceto os valores que foram cancelados)
    3. Localidade (Estado, Região ou Exterior)
    4. Função (Saúde, educação, etc)
    5. Autor (nome do legislador)
    6. Ano
  
3. Armazenar o array em uma Árvore B+ ???, utilizando o código (índice 0 do array) como chave, e salvar como arquivo binário.
    1. Armazenar lista de offsets das emendas por estado em arquivo invertido
    2. Armazenar lista de offsets das emendas por função em arquivo invertido

4. Ler e processar os dados do arquivo binário:
    1. Gerar lista ordenada dos estados que mais recebem emendas
    2. Gerar lista ordenada dos parlamentares que mais empenham emendas
    3. Gerar histograma(teminalplot?) do valor gasto por ano
    4. Gerar lista ordenada das cidades que mais recebem emendas
    5. Gerar lista ordenada das funções que mais recebem emendas

    6. Listar quantidade de emendas por função e maior valor
    7. Listar emendas individualmente por função e maior valor
    8. Listar emendas por maior valor (top 20)

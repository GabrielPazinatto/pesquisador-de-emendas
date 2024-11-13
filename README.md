# Pesquisador de Emendas

O projeto pode ser acessado por [este link](https://gabrielpazinatto.github.io/pesquisador-de-emendas/).

**IMPORTANTE:** A API está hospedada em um servidor gratuito do Render. Por isso, a primeira solicitação pode demorar para ser processada.

### O Que São Emendas Parlamentares?
Emendas Parlamentares são uma parcela do orçamento público reservada para que parlamentares da esfera federal (senadores e deputados federais) resolvam problemas em suas regiões de origem, enviando essa verba para determinadas causas ou instituições públicas ou de caridade.

## O Pesquisador

Esse é um projeto acadêmico para a disciplina de Classificação e Pesquisa de Dados. Originalmente, ele foi desenvolvido para ser usado através do terminal, mas, posteriormente, foi adaptado para uso com interface Web, utilizando FastAPI para o Back-end. Os dados são coletados em um .csv disponível no [Portal da Transparência](https://portaldatransparencia.gov.br/emendas) e armazenados utilizando um sistema de arquivos próprio. Ao atualizar a base de dados, todas as entradas do .csv são lidas e armazenadas em um arquivo binário serial. Simultaneamente, os ponteiros para as posições das emendas no arquivo são salvas nas estruturas de busca.

### Buscas:

<center>

|       |    **Chave**   | **Estrutura** |  **Busca**  |
|:-----:|:--------------:|:-------------:|:-----------:|
| **1** |  Nome do Autor |   Trie Tree   | Por Prefixo |
| **2** |   Localidade   |   Hash Table  |  Por Valor  |
| **3** | Ano de Autoria |   Hash Table  |  Por Valor  |

</center>

Todas as pesquisas podem ser feitas ordenando as chaves de maneira crescente ou decrescente. Há algumas funcionalidades desenvolvidas que ainda não foram implementadas no front-end.
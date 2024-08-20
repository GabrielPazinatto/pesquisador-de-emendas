import unicodedata

###################################################################################################################################

def partition(array, low, high):
        i = low - 1 #marca a posição onde o próximo elemento menor deve ser colocado, iniciando do mais a esquerda

        pivot = array[high]  # Define o último elemento do array como pivô [[], [], [], []  <---]
        
        for j in range(low, high):
            #Se o elemento for menor que o pivo e está em ordem crescente (menores a esquerda) 
            if (array[j][1] <= pivot[1]):
                i += 1 
                array[i], array[j] = array[j], array[i]  # Troca para o próximo índice depois do menor anteriormente adicionado

        array[i + 1], array[high] = array[high], array[i + 1]  #Coloca o pivo na posição correta

        return i + 1 #retorna a posição do pivo 

######################################################################################################################################

def quicksort_iterative(amendments, ascending=True):
        
        low = 0
        high = len(amendments) - 1
        size = high - low + 1
        stack = [0] * size

        # Inicializa o topo da pilha
        top = -1            #Pilha vazia
        top += 1            #Começa o índice em 0
        stack[top] = low    #Início do array 
        top += 1
        stack[top] = high   #Fim do Array

        # Enquanto a pilha não está vazia
        while top >= 0:

            #Desempilha
            high = stack[top]   #fim do array
            top -= 1
            low = stack[top]    #início do array
            top -= 1

            # Chama a função para particionar e retornar a posição do pivo (menores a esquerda e maiores a direita)
            p = partition(amendments, low, high)

            # Se houver elementos à esquerda do pivô, coloca-os na pilha
            if p - 1 > low:
                top += 1
                stack[top] = low    #coloca na pilha o índice 0 <- i do array que ainda precisa ser ordenado 
                top += 1
                stack[top] = p - 1

            # Se houver elementos à direita do pivô, coloca-os na pilha
            if p + 1 < high:
                top += 1
                stack[top] = p + 1
                top += 1
                stack[top] = high   #coloca na pilha o índice i -> high que ainda precisa ser ordenado

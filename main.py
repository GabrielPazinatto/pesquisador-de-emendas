from Search import Searcher
import time
import Update 

if __name__ == '__main__':
    
    print("Inicializando...")
    start = time.process_time()

    data_manager = Searcher()
    try:data_manager.load_data()
    except: print("Dados não gerados!")
    
    print("Programa inicializado em ",time.process_time() - start, 's!')
 
    choice = ''   
    
    while True:
        print("(1) Atualizar base de dados.")
        print("(2) Buscar emendas por nome do autor.")
        print("(3) Buscar emendas por função.")
        print("(4) Buscar emendas por localidade. ")
        print("(5) Mostrar emendas por ano. ")
        print("(6) Mostrar emendas por função. ")
        print("(7) Mostrar emendas por localidade. ")
        print("(0) Encerrar.")
        
        choice = input()

        
        print("Escolha a ordem dos valores: ")
        print("(1) CRESCENTE. ")
        print("(2) DESCRESCENTE. ")
        order = input()

        match(choice):
            case '1':
                order = True
            case '2':
                order = False

        match(choice):
            case '1':
                data_manager.update_data_set()
            case '2':
                data_manager.search_by_author(order)
            case '3':
                data_manager.search_by_function(order)
            case '4':
                data_manager.search_by_local(order)
            case '5':
                data_manager.show_total_by_year()
            case '6':
                data_manager.show_total_by_function()
            case '7':
                data_manager.show_total_by_locality()
            case '0':
                exit()
            case _:
                print("Escolha inválida.")
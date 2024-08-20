from Search import Searcher
import time
import Update 
import os

if __name__ == '__main__':
    
    print("\nInicializando...")
    start = time.process_time()

    data_manager = Searcher()
    try:data_manager.load_data()
    except: print("Dados não gerados!")
    
    order = False
    
    print("Programa inicializado em ",time.process_time() - start, 's!')
 
    choice = ''   
    
    while True:
        print("(1) Atualizar base de dados.")
        print("\nBUSCAS POR CHAVE------------------------")
        print("(2) Buscar emendas por nome do autor.")
        print("(3) Buscar emendas por função.")
        print("(4) Buscar emendas por localidade. ")
        print("------------------------------------------")
        print("\nDADOS PROCESSADOS-----------------------")
        print("(5) Mostrar emendas por ano. ")
        print("(6) Mostrar emendas por função. ")
        print("(7) Mostrar emendas por localidade. ")
        print("------------------------------------------")
        print("\n(8) Mudar ordenação dos dados. " + ("(CRESCENTE)" if order else "(DECRESCENTE)"))
        print("(0) Encerrar.\n")
        
        choice = input("Opção: ")

        os.system('cls' if os.name == 'nt' else 'clear')

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
            case '8':
                order = not order
            case '0':
                exit()
            case _:
                print("Escolha inválida.")
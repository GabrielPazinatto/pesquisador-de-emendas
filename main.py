from input_handler import import_data, generate_data_set

if __name__ == '__main__':
    
    input_data = import_data("Emendas.csv")
    a,data_set_size = generate_data_set(input_data)
    

        

from data_handler import get_input_data
import time

if __name__ == '__main__':
    
    start = time.process_time()
    
    data_set = get_input_data("Emendas.csv")
        
    print(time.process_time() - start)
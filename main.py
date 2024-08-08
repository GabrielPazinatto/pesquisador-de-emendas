from data_handler import generate_bin_files,Indexes,Functions
import time
import pickle

if __name__ == '__main__':
    
    offsets = []
    
    generate_bin_files("Emendas.csv", offsets=offsets)
   
    pointers_file = open("Pointers.bin", 'rb')
    main_file = open("Amendments.bin", 'rb')


import random

import csv

from combined import Read_Data, Request_Address


#MEMORY_RAM

File_Name = "memory.csv"


def load_ram_csv():
    ram = {}
    with open(File_Name, mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            addr = int(row["Address"], 2)
            val = int(row["Data"], 16)
            ram[addr] = val
    return ram


def save_ram_csv(ram):
    with open(File_Name, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Address", "Data"])  # Header
        for addr, val in ram.items():
            writer.writerow([f"0b{addr:06b}", f"0x{val:08X}"])

Ram = load_ram_csv()



#core
Control = random.randint(0,1) # 1 bit control signal
Address = random.randint(0,0b111111) # 6 bits address

if(Control):
    Write_Data = random.randint(0,0xFFFFFFFF) # on write instruction when data is written to memory from the core


#each block must have an address as well.

#Cache
Read_Data = 0
Cache = {}
def Write_Cache(address, Write_Data):

    Cache[address]= Write_Data

def Read_Cache(address):
    Read_Data = Cache[address]

def Cache_Write_Miss(address,Write_Data):
    Ram[address] = Write_Data

def Cache_Read_Miss(address):
    Read_Data = Ram[address]
    Cache[address] = Read_Data
    


for i in Cache.items():
    if i. == Address:
        print("this is a cache hit")
        if(Control):
            Write_Cache(Address, Write_Data)
        else :
            Read_Cache(Address)
    else :
        if(Control):
            Cache_Write_Miss(Address,Write_Data)
        else:
            Cache_Read_Miss(Address)
    




    







#Request_Recieved = 0x0000000000 #39 bits this includes 32 bits of data
#and six bits of address and one bit of control


# on load instruction when data is read from memory and given to the core


#[[control bit][6 bits of address][32 bits of data]]

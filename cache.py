import random
import os
import csv




#MEMORY_RAM

File_Name = "memory.csv"
CACHE_FILE = "cache.csv"


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


def load_cache_csv():
    cache = {}
    if not os.path.exists(CACHE_FILE):
        return cache
    with open(CACHE_FILE, mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            addr = int(row["Address"], 2)
            val = int(row["Data"], 16)
            cache[addr] = val
    return cache

def save_cache_csv(cache):
    with open(CACHE_FILE, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Address", "Data"])
        for addr, val in cache.items():
            writer.writerow([f"0b{addr:06b}", f"0x{val:08X}"])

class Cache_Block: 
    def __init__ (self):
        self.address = None
        self.order = 0
        self.state = "I"
        self.data = 0 

    def show(self):
        print(f"Address : {self.address:06b}")
        print(f"Data    : {self.data:08X}")
        print(f"State   : {self.state}")
        print(f"Order   : {self.order}")

Cache = {
    0: Cache_Block(),
    1: Cache_Block(),
    2: Cache_Block(),
    3: Cache_Block()}


#core
Control = random.randint(0,1) # 1 bit control signal
Address = random.randint(0,0b111111) # 6 bits address

print(f"ADDRESS : bin({Address:06b}) , Control = {Control} ")

if(Control):
    Write_Data = random.randint(0,0xFFFFFFFF) # on write instruction when data is written to memory from the core
    print(f"the data to be written is hex{Write_Data:08x}")

#each block must have an address as well.

#Cache

Cache = load_cache_csv()
Read_Data = 0


def Write_Cache(Address, Write_Data):

    Cache[Address]= Write_Data
    print("this is a write cache hit")

def Read_Cache(Address):
    Read_Data = Cache[Address]
    print("this is a read cache hit")

def Cache_Write_Miss(Address,Write_Data):
    print(f"this is a write cache miss")
    Cache[Address] = Ram[Address]
    print("we have Ram's data in cache right now, now we will write the data to Cache")
    Cache[Address] = Write_Data
    print(f"we are writing the data to RAM as well")
   
    Ram[Address] = Write_Data

def Cache_Read_Miss(Address):
    Read_Data = Ram[Address]
    print(f"this is a read cache miss")
    Cache[Address] = Read_Data
    


#Execution is starting from here

    
if len(Cache) == 0 :
    if(Control):
        Cache_Write_Miss(Address,Write_Data)
    else :
        Cache_Read_Miss(Address)
else:
    if Address in Cache:
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

save_ram_csv(Ram)



save_cache_csv(Cache)



    




    







#Request_Recieved = 0x0000000000 #39 bits this includes 32 bits of data
#and six bits of address and one bit of control


# on load instruction when data is read from memory and given to the core


#[[control bit][6 bits of address][32 bits of data]]

import csv
import os
import random

import time 

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



class Cache_Block:

    def __init__(self):
        self.address = None
        self.order = 0
        self.state = "I"
        self.data = 0
 
    def show(self):
        
        print(f"Address : {self.address}")
        print(f"Data    : {self.data}")
        print(f"State   : {self.state}")
        print(f"Order   : {self.order}")



cache_dict = {i: Cache_Block() for i in range(4)}
  


def load_cache_csv():
  

    if not os.path.exists(CACHE_FILE):
        return cache_dict

    with open(CACHE_FILE, mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            slot = int(row["Slot"])
            block = cache_dict[slot]

           
            if row["Address"] != "None" and row["Address"] != "":
                block.address = int(row["Address"], 2)
            else:
                block.address = None

          
            if row["Data"] != "None" and row["Data"] != "":
                block.data = int(row["Data"], 16)
            else:
                block.data = 0

            
            block.state = row["State"]
            block.order = int(row["Order"])

    return cache_dict


def save_cache_csv(cache_dict):
    with open(CACHE_FILE, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Slot", "Address", "Data", "State", "Order"])

        for slot, block in cache_dict.items():
          
            addr_str = (
                f"0b{block.address:06b}"
                if isinstance(block.address, int)
                else "None"
            )

           
            data_str = (
                f"0x{block.data:08X}"
                if isinstance(block.data, int)
                else "None"
            )

            writer.writerow(
                [slot, addr_str, data_str, block.state, block.order]
            )


Cache = load_cache_csv()
Read_Data = 0
powder = 0 



def find_cache_slot(addr):
    for slot, block in Cache.items():
        if block.address == addr and block.state != "I":
            return slot
    return None


def get_slot_for_miss():
    for slot, block in Cache.items():
        if block.state == "I" or block.address is None:
            return slot
    return 0  


def Write_Cache(slot, Write_Data):
    Cache[slot].data = Write_Data
    Cache[slot].state = "M"
    print("this is a write cache hit")
    Cache[slot].order = powder


def Read_Cache(slot):
    global Read_Data
    Read_Data = Cache[slot].data
    print("this is a read cache hit")
    Cache[slot].order = powder


def Cache_Write_Miss(Address, Write_Data):
    print(f"this is a write cache miss")
    slot = get_slot_for_miss()
    Cache[slot].address = Address
    Cache[slot].data = Ram[Address]
    Cache[slot].state = "M"
    print(
        "we have Ram's data in cache right now, now we will write the data to Cache"
    )
    Cache[slot].data = Write_Data
    print(f"we are writing the data to RAM as well")
    Cache[slot].order = powder
    #Ram[Address] = Write_Data (we are not evicting now)


def Cache_Read_Miss(Address):
    global Read_Data
    slot = get_slot_for_miss()
    Read_Data = Ram[Address]
    print(f"this is a read cache miss")
    Cache[slot].address = Address
    Cache[slot].data = Read_Data
    Cache[slot].state = "E"
    Cache[slot].order = powder

for i in range(10):
    
    Control = random.randint(0, 1)  # 1 bit control signal
    Address = random.randint(0, 0b111111)  # 6 bits address

    print(f"ADDRESS : bin({Address:06b}) , Control = {Control} ")

    if Control:
        Write_Data = random.randint(0, 0xFFFFFFFF)  # 32 bits data
        
        
        print(f"the data to be written is hex{Write_Data:08x}")


   
#EXECUTION
    hit_slot = find_cache_slot(Address)

    if hit_slot is not None:
        print("this is a cache hit")
        if Control:
            Write_Cache(hit_slot, Write_Data)
        else:
            Read_Cache(hit_slot)
    else:
        if Control:
            Cache_Write_Miss(Address, Write_Data)
        else:
            Cache_Read_Miss(Address)
    print(i, "th iteration")

    for k,v in Cache.items():
        print(f"Slot {k}: Address={v.address}, Data={v.data}, State={v.state}, Order={v.order}")


    time.sleep(8)
    print("Now we will save the cache into cache.csv file")
    time.sleep(1)
    if(powder == 3):
         powder = 0 
    else :
        powder = powder + 1
    save_cache_csv(Cache)
    

   

save_ram_csv(Ram)
save_cache_csv(Cache)

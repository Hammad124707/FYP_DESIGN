import csv
import os
import random
import time
File_Name = "memory.csv"
CACHE_FILE = "cache.csv" 
eviction_log = []
powder = -1

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
        writer.writerow(["Address", "Data"])

        for addr, val in ram.items():
            addr_str = f"0b{addr:06b}"
            val_str = f"0x{val:08X}"

            writer.writerow([addr_str, val_str])


Ram = load_ram_csv()



def load_cache_csv(cache):
    global powder

    if not os.path.exists(CACHE_FILE):
        return cache.cache_dict

    with open(CACHE_FILE, mode="r") as file:
        reader = csv.DictReader(file)

        for row in reader:

            if not row.get("Slot") or not row["Slot"].isdigit():
                break

            slot = int(row["Slot"])
            block = cache.cache_dict[slot]

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
            if (block.order > powder) :
                powder = block.order


    powder = powder + 1 


    return cache.cache_dict


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

            writer.writerow([
                slot,
                addr_str,
                data_str,
                block.state,
                block.order
            ])

        for _ in range(3):
            writer.writerow([])

        writer.writerow(["--- Eviction Summary (Stack View) ---"])
        writer.writerow(["Event", "Address", "Data"])

        for event_row in reversed(eviction_log):
            writer.writerow(event_row)



def log_cache_event(address, data, state):

    event = None

    if state == "M":
        event = "Write Back"

    elif state == "E":
        event = "Silent Eviction"

    if event:
        eviction_log.append([
            event,
            f"0b{address:06b}",
            f"0x{data:08X}"
        ])




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


#writeback method is missing
class Core :
    def __init__(self, core_id):
        self.core_id = core_id
        self.request = None
        self.write_data = None
        self.return_read_data = None
        self.return_write_validation = None 
        self.permission = 1
        
    def generate_request(self):
        if(self.permission):
            self.request = random.randint(0, 0b11111111)
            #2 bits of what to do 
            #6 bits of the address
            return self.request

    def generate_write_data(self):
        if(self.permission):
            self.write_data = random.randint(0, 0xffffffff)
            return self.write_data
 
    def process_request(self):
        time.sleep(3)
        self.permission = 0 
        print("The core Has a new Request \n we are now about to process a new request")
        print("  ")
        print(" ")
        request_address = self.request & (0b00111111)
        print(f"this is the requested address bin({request_address:06b})")
        request_control = self.request >> 6
        print(f"{request_control:02b} these are the control bits")

        if  not(request_control):
            print(f"this is the Write Request and the data to be written is \n hex {self.write_data:08x}")
        else:
            print(" this is another request") 
        self.permission = 1 
        print(" the request will now go out of core to the Cache")
        print(" ")

    def cache_to_core(self):
        if self.return_read_data :
            print(f"Core has recieved the data and the data is {self.return_read_data}")
        elif(self.return_write_validation):
            print("we have successfully written the data to the Ram")



class Cache:

    def __init__(self, cache_id):
        self.cache_id = cache_id
       

        self.flag = 0b0 # 1 bit
        self.state = 0b0 # 8 bits

        self.cache_dict = {
            i: Cache_Block() for i in range(4)
        } # 4 cache lines

    def recieve_request(self,request,write_data):
        time.sleep(3)
        print(" the cache has recieved the request")
        self.request = request 
        self.write_data = write_data

    def find_cache_slot(self, addr):
        for slot, block in self.cache_dict.items():
            if block.address == addr and block.state != "I":
                return slot
        return None

    def get_slot_for_miss(self):
        for slot, block in self.cache_dict.items():
            if block.state == "I" or block.address is None:
                return slot

        return self.min()

    def Write_Cache(self, slot, Write_Data):
        self.cache_dict[slot].data = Write_Data
        self.cache_dict[slot].state = "M"
        print("This is a write cache hit")

    def Read_Cache(self, slot):
        Read_Data = self.cache_dict[slot].data
        print("This is a read cache hit")
        return Read_Data

    def min(self):
        min = 100000
        for slot in self.cache_dict.keys():
            if self.cache_dict[slot].order<min:
                min = self.cache_dict[slot].order
                slt = slot

        
        Eviction_Data = self.cache_dict[slt].data
        Eviction_Address = self.cache_dict[slt].address
        return slt

    def write_back(self,data,address,event):
        print(f"we are writing back the data to RAM")
        Ram[address] = data
        "eviction done"
        log_cache_event(address,data,event)
#check the difference between yours and gpt
    def Cache_Write_Miss(self, Address, Write_Data):


        Cache = self.cache_dict

        print("this is a write cache miss")

        slot = self.get_slot_for_miss()
        if Cache[slot].address is not None:
            self.write_back(Cache[slot].data, Cache[slot].address, Cache[slot].state)
       

        Cache[slot].address = Address
        Cache[slot].data = Ram[Address]
        Cache[slot].state = "M"

        print(
            "We have Ram's data in cache right now, now we will write to that datA"
        )

        Cache[slot].data = Write_Data

        #print("We are writing the data to RAM as well")

        Cache[slot].order = powder
    # Ram[Address] = Write_Data (we are not evicting now)
    def Cache_Read_Miss(self,Address):
        global Read_Data
        Cache = self.cache_dict
        slot = self.get_slot_for_miss()
        if Cache[slot].address is not None:
            self.write_back(Cache[slot].data, Cache[slot].address, Cache[slot].state)
        Read_Data = Ram[Address]
        print(f"this is a read cache miss")
        Cache[slot].address = Address
        Cache[slot].data = Read_Data
        Cache[slot].state = "E"
        Cache[slot].order = powder
  
   



# pre execution phase




c0 = Core(0)
cache0 = Cache(0)
load_cache_csv(cache0)
print(" before execution is is how the cache looks like \n")
print("")

for k, v in cache0.cache_dict.items():

        addr_str = f"{v.address:06b}" if isinstance(v.address, int) else "None"
        data_str = f"0x{v.data:08X}" if isinstance(v.data, int) else "None"

        print(f"Slot {k}: Address={addr_str}, Data={data_str}, State={v.state}, Order={v.order}")





# EXECUTION phase
for i in range(3):
    Request = c0.generate_request()
    Write_Data = c0.generate_write_data()
    c0.process_request()



    cache0.recieve_request(Request,Write_Data)
    Control = cache0.request >> 6 
    Address  = cache0.request & 0b00111111
    hit_slot = cache0.find_cache_slot(Address)

    if hit_slot is not None:
        print("this is a cache hit")

        if not(Control):
            cache0.Write_Cache(hit_slot, Write_Data)
        else:
            cache0.Read_Cache(hit_slot)

    else:
        if not(Control):
            cache0.Cache_Write_Miss(Address, Write_Data)
        else:
            cache0.Cache_Read_Miss(Address)

        powder = powder + 1

    print(i, "th iteration")



# post execution phase
    for k, v in cache0.cache_dict.items():

        addr_str = f"{v.address:06b}" if isinstance(v.address, int) else "None"
        data_str = f"0x{v.data:08X}" if isinstance(v.data, int) else "None"

        print(f"Slot {k}: Address={addr_str}, Data={data_str}, State={v.state}, Order={v.order}")


    time.sleep(3)

    print("Now we will save the cache into cache.csv file")
    print(" ")
    print(" ")

    time.sleep(1)

    save_cache_csv(cache0.cache_dict)



save_ram_csv(Ram)
save_cache_csv(cache0.cache_dict)



            









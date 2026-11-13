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


class Cache :
    def __init__ (self,cache_id,request,control,write_data):
        self.cache_id = cache_id    
        self.cache_block = Cache_Block() 
        self.request = request 
        self.control = control 
        self.write_data = write_data
        self.flag = 0b0 #0 stands for snoop mode, 1 stands for reply mode , 1 bit data
        self.state = 0b0 # this is a 1 byte state register
        self.cache_dict = {i: Cache_Block() for i in range(4)}

    
    def find_cache_slot(self,addr):
        for slot, block in Cache.items():
            if block.address == addr and block.state != "I":
                return slot
        return None


    def get_slot_for_miss():
        for slot, block in Cache.items():
            if block.state == "I" or block.address is None:
                return slot
        return min(Cache)


    def Write_Cache(slot, Write_Data):
        Cache[slot].data = Write_Data
        Cache[slot].state = "M"
        print("this is a write cache hit")
        


    def Read_Cache(slot):
        global Read_Data
        Read_Data = Cache[slot].data
        print("this is a read cache hit")

    def min(Cache_dict):
        min = 100000
        for slot in Cache_dict.keys():
            if Cache_dict[slot].order<min:
                min = Cache_dict[slot].order
                slt = slot

        return slt
            

            


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

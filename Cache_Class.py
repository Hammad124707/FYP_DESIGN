
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


class Cache:

    def __init__(self, cache_id):
        self.cache_id = cache_id
       

        self.flag = 0b0
        self.state = 0b0

        self.cache_dict = {
            i: Cache_Block() for i in range(4)
        }


    def recieve_request(self,request,write_data):
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

        return self.find_oldest_slot()

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

        
        Eviction_Data = Cache[slot].data
        Eviction_Address = Cache[slot].address
        return slt

#writeback method is missing


first_cache = Cache(0,0b0001011,1,0b00)
print(first_cache.flag)
print(first_cache.state)

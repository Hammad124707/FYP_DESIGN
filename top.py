import csv
import os
import random
import time
File_Name = "memory.csv"
CACHE_FILE = "cache.csv" 
eviction_log = []
powder = -1


"""  
I = 0b00 | Control = 1 (this means we are writing) | 00 = write req
S = 0b01 | Control = 0 (this means we are reading) | 01 = Upgrade
E = 0b10                                           | 10  = PutM
M = 0b11                                           | 11 = read req

"""
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


class Hub: 

    def __init__(self,cache):
        self.request_buffer =None 
        self.return_block = None
        self.cache = cache
    def recieve_request(self,control,address,data):
        self.control = control 
        self.address = address
        self.data = data

    def process_request(self):
        if (self.control == 0b10):
            print("this is a PutM request")
            Ram[self.address] =  self.data
            print(" the data has been installed in the Ram")
            return 1
        elif(self.control == 0b11):
            print("this is a write request")
            self.return_block =  self.cache.snoop_by_hub(0b1,self.address)


    

class Cache_Block:

    def __init__(self):
        self.address = None
        self.order = 0
        self.state = 0b00
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
        self.return_read_data = None  #what will we get on the CCD line
        self.return_write_validation = None  #what will we get on the ccd line
        self.permission = 1 # permission will be given if the data has been received through the ccd line (data of the previous request)
        self.flag = None # this flag will check what to expect in axi stream return. Expect data or expect write validation
        
    def generate_request(self):
        if(self.permission):
             
            self.request = random.randint(0, 0b1111111)
            #1 bits of what to do 
            #6 bits of the address
            return self.request

    def generate_write_data(self):
        if(self.permission):
            self.write_data = random.randint(0, 0xffffffff)
            return self.write_data
 
    def process_request(self):
        time.sleep(3)
        
        print("The core Has a new Request \n we are now about to process a new request")
        print("  ")
        print(" ")
        request_address = self.request & (0b0111111)
        print(f"this is the requested address bin({request_address:06b})")
        request_control = self.request >> 6
        print(f"{request_control:01b} these are the control bits")

        if  not(request_control):
            self.flag = 0 # expect write validation
            print(f"this is the Write Request and the data to be written is \n hex {self.write_data:08x}")
        else:
            self.flag = 1 #expect read validation
            print(" this is a read request") 
        print(" the request will now go out of core to the Cache")
        self.permission = 0
        print(" ")

    def cache_to_core(self): #update the name of cachetocore to ccd

        if self.flag == 0:

            if self.return_write_validation is None:
                print("Core is waiting for write validation")

            else : 
                self.return_write_validation == 1:
                print("Core: Write transaction completed successfully")
                self.permission = 1 

            

        else :

            if self.return_read_data is None:
                print("Core is waiting for read data")
               
                

            else:
                print(f"Core has received the data: {self.return_read_data}, End the transaction")
                self.permission = 1
   


class Cache:

    def __init__(self, cache_id,hub):
        self.cache_id = cache_id
        self.hub = hub 
       

        self.flag = 0b0 # 1 bit #1 means cache is expecting a reply , 0 means cache is expecting a snoop
        self.state = 0b0 # 8 bits
    
        self.ht = 0b0 #1 means hub is waiting
        self.gc = 0b0 

        self.cache_dict = {
            i: Cache_Block() for i in range(4)
        } # 4 cache blocks being instansiated

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

    def get_slot_for_miss(self): #this is for finding the empty block (from the 4 blocks) so we can process a miss request
        for slot, block in self.cache_dict.items():
            if block.state == "I" or block.address is None: 
                return slot # block found 

        return self.min() # block not found , evict something

    def Write_Cache(self, slot, Write_Data):
        
        self.cache_dict[slot].data = Write_Data
        self.cache_dict[slot].state = "M"
        print("This is a write cache hit")
        return 1  #write validation sent to the core
        

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

    def write_back(self,data,address,event): # AXI REQ, this needs a change aswell
        print(f"we are giving hub the block so it will write back")
        self.hub.recieve_request(0b10,address,data) # our PutM request
        self.hub.process_request()
        print("eviction done")
        log_cache_event(address,data,event)

    
    def Cache_Write_Miss(self, Address, Write_Data):
    
    
            Cache = self.cache_dict
    
            print("this is a write cache miss")
    
            slot = self.get_slot_for_miss()
            if Cache[slot].address is not None:
                result = self.write_back(Cache[slot].data, Cache[slot].address, Cache[slot].state)

            # now that we have space we will give hub our Write request, means we will ask hub to find the block for us 

            self.hub.recieve_request(0b00,Address,Write_Data)
            self.hub.process_request()
            """
            Cache[slot].address = Address
            Cache[slot].data = Ram[Address]
            Cache[slot].state = "M"
    
            print(
                "We have Ram's data in cache right now, now we will write to that datA"
            )
    
            Cache[slot].data = Write_Data
    
            #print("We are writing the data to RAM as well")
    
            Cache[slot].order = powder
            return 1  
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
            return Read_Data
    
            """




    

    def check_golden_case(self,request):
        Control = self.request >> 6
        Address = self.request & 0b0111111
        for slot , block in self.cache_dict.items():
            if(Control) :
                if(block.address == Address and (block.state != 0b00 or block.state != 0b01 ))h:
                    print("this is a golden case")
                    self.gc = 1
            else :
                if(block.address == Address and block.state != 0b00) :
                    print("this is a golden case")
                    self.gc = 1

                 
        

        
    def snoop_by_hub (self,control,address):
        for slot, block in self.cache_dict.items():
            if(block.address == address):
                print("The required block by the hub is in the cache")
                if(control == 0):
                    print("MC cache wants to read, make the state shared")
                    block.state = 0b10
                    return block.data
                else:
                    print("MC cache wants to write, make the state invalid")
                    block.state = 0b00
                    return block.data

  
    def process_request(self, core):

        global powder

        # 1. Get request information
        Control = self.request >> 6
        Address = self.request & 0b0111111

        while (self.ht == 1) :
            print("we are waiting for the hub to finish the snoop")

    


        print(f"Cache is processing address: {Address:06b}") #next optimisation would be to complete the whole request rather than just making gc =1 
        self.check_golden_case(self.request)

        # 2. Check whether address exists in cache
        hit_slot = self.find_cache_slot(Address)

        # 3. Process cache hit
        if hit_slot is not None:

            print("CACHE HIT")

            if Control == 0:
                # Write request
                core.return_write_validation = self.Write_Cache(
                    hit_slot, self.write_data
                    
                )

            else:
                # Read request
                core.return_read_data = self.Read_Cache(hit_slot)

            self.cache_dict[hit_slot].order = powder
            return 1

        # 4. Process cache miss
        else:
            return 0 

           





# pre execution phase




c0 = Core(0)
hub = Hub()
cache0 = Cache(0,hub)
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
    print("Request:", cache0.request)

    if cache0.process_request(c0) != 1 :
        print("we have a cache miss")


   
    c0.cache_to_core()




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



            









class Cache:

    # Hub transaction opcodes
    WRITE = 0b00
    READ = 0b01
    PUTM = 0b10
    UPGRADE = 0b11

    # MESI states
    I = "I"
    S = "S"
    E = "E"
    M = "M"

    def __init__(self, cache_id):

        self.cache_id = cache_id

        # Four cache lines
        self.cache_dict = {
            i: Cache_Block() for i in range(4)
        }

        # Cache-to-Hub transaction flag
        # Set only after Hub grants the request.
        self.flag = 0

        # Core request waiting inside the Cache
        self.pending_core_request = None

        # Request currently being sent to the Hub
        self.pending_hub_request = None

        # Response received from the Hub
        self.hub_response = None

        # Response that will be returned to the Core
        self.core_response = None

        self.hub_response = None

        # FIFO counter
        self.fifo_counter = 0

    # --------------------------------------------------
    # 1. RECEIVE REQUEST FROM CORE
    # --------------------------------------------------


    def prepare_hub_response(self, response_type, address, data=None):

        self.hub_response = {
            "cache_id": self.cache_id,
            "address": address,
            "response_type": response_type,
            "data": data
        }

        return self.hub_response



    def receive_core_request(self, control, address, write_data=None):

        if self.pending_core_request is not None:
            raise RuntimeError("Cache already has a pending Core request.")

        if control not in (0, 1):
            raise ValueError("Core control must be 0 or 1.")

        if not 0 <= address < 64:
            raise ValueError("Address must be a 6-bit value.")

        self.pending_core_request = {
            "control": control,
            "address": address,
            "write_data": write_data
        }

    # --------------------------------------------------
    # 2. FIND A CACHE LINE
    # --------------------------------------------------

    def find_cache_slot(self, address):

        for slot, block in self.cache_dict.items():

            if block.address == address and block.state != self.I:
                return slot

        return None

    # --------------------------------------------------
    # 3. FIND AN EMPTY SLOT OR FIFO VICTIM
    # --------------------------------------------------

    def get_slot_for_miss(self):

        # Prefer an invalid/empty slot
        for slot, block in self.cache_dict.items():

            if block.state == self.I:
                return slot

        # Otherwise, replace the oldest block
        return min(
            self.cache_dict,
            key=lambda slot: self.cache_dict[slot].order
        )

    # --------------------------------------------------
    # 4. DECIDE WHAT THE CORE REQUEST REQUIRES
    # --------------------------------------------------

    def process_core_request(self):

        if self.pending_core_request is None:
            return None

        request = self.pending_core_request

        control = request["control"]
        address = request["address"]
        write_data = request["write_data"]

        slot = self.find_cache_slot(address)

        # ---------------- READ ----------------

        if control == 0:

            # Read hit
            if slot is not None:

                block = self.cache_dict[slot]

                self.core_response = {
                    "type": "READ_COMPLETE",
                    "data": block.data
                }

                self.pending_core_request = None
                return self.core_response

            # Read miss
            return self.prepare_hub_request(
                self.READ, address
            )

        # ---------------- WRITE ----------------

        if control == 1:

            # Write hit
            if slot is not None:

                block = self.cache_dict[slot]

                # Already have exclusive modified ownership
                if block.state == self.M:

                    block.data = write_data

                    self.core_response = {
                        "type": "WRITE_COMPLETE"
                    }

                    self.pending_core_request = None
                    return self.core_response

                # Shared copy needs an Upgrade
                if block.state == self.S:

                    return self.prepare_hub_request(
                        self.UPGRADE, address
                    )

                # Exclusive copy can be modified locally.
                # E -> M is the standard MESI transition.
                if block.state == self.E:

                    block.state = self.M
                    block.data = write_data

                    self.core_response = {
                        "type": "WRITE_COMPLETE"
                    }

                    self.pending_core_request = None
                    return self.core_response

            # Write miss
            return self.prepare_hub_request(
                self.WRITE, address
            )

    # --------------------------------------------------
    # 5. PREPARE A REQUEST FOR THE HUB
    # --------------------------------------------------

    def prepare_hub_request(self, opcode, address, data=None):

        # First beat: 2-bit opcode + 6-bit address
        first_beat = (opcode << 6) | address

        beats = [first_beat]

        # PutM has an additional 32-bit data beat
        if opcode == self.PUTM:

            if data is None:
                raise ValueError("PutM requires 32-bit data.")

            beats.append(data)

        self.pending_hub_request = {
            "opcode": opcode,
            "address": address,
            "beats": beats
        }

        return self.pending_hub_request

    # --------------------------------------------------
    # 6. HUB GRANTS THE REQUEST
    # --------------------------------------------------

    def hub_grant_received(self):

        if self.pending_hub_request is None:
            raise RuntimeError("No Hub request is waiting for a grant.")

        self.flag = 1

    # --------------------------------------------------
    # 7. COMPLETE THE HUB TRANSACTION
    # --------------------------------------------------

    def complete_hub_transaction(self):

        self.flag = 0
        self.pending_hub_request = None
        self.hub_response = None

    # --------------------------------------------------
    # 8. RECEIVE A SNOOP FROM THE HUB
    # --------------------------------------------------

    def handle_snoop(self, address, snoop_type):

        slot = self.find_cache_slot(address)

        # Cache does not have this line
        if slot is None:

            return {
                "response": "NO_COPY",
                "data": None
            }

        block = self.cache_dict[slot]

        # ---------------- READ SNOOP ----------------

        if snoop_type == "READ":

            # Only E/M holders supply data
            if block.state in (self.E, self.M):

                data = block.data

                # Dirty data must be written back by Hub
                dirty = block.state == self.M

                # Both copies become Shared
                block.state = self.S

                return {
                    "response": "HAVE_COPY",
                    "data": data,
                    "dirty": dirty
                }

            # S means RAM is the owner
            return {
                "response": "NO_COPY",
                "data": None
            }

        # ---------------- WRITE SNOOP ----------------

        if snoop_type == "WRITE":

            data = None
            dirty = False

            # Modified cache must provide its latest data
            if block.state == self.M:

                data = block.data
                dirty = True

            # Invalidate the line
            self.cache_dict[slot] = Cache_Block()

            return {
                "response": "INVALIDATE_DONE",
                "data": data,
                "dirty": dirty
            }

        raise ValueError("Unknown snoop type.")

    # --------------------------------------------------
    # 9. INSTALL A LINE RECEIVED FROM THE HUB
    # --------------------------------------------------

    def install_block(self, address, data, state):

        if state not in (self.S, self.E, self.M):
            raise ValueError("Invalid state for an installed block.")

        slot = self.get_slot_for_miss()

        self.cache_dict[slot] = Cache_Block()

        block = self.cache_dict[slot]

        block.address = address
        block.data = data
        block.state = state

        self.fifo_counter += 1
        block.order = self.fifo_counter

        return slot

    # --------------------------------------------------
    # 10. HANDLE PUTM EVICTION
    # --------------------------------------------------

    def prepare_putm(self, slot):

        block = self.cache_dict[slot]

        if block.state != self.M:
            raise RuntimeError("PutM is only required for an M block.")

        return self.prepare_hub_request(
            self.PUTM,
            block.address,
            block.data
        )

    # --------------------------------------------------
    # 11. CLEAR AN EVICTED BLOCK
    # --------------------------------------------------

    def evict_block(self, slot):

        self.cache_dict[slot] = Cache_Block()

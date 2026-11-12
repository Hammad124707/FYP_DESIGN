
import random
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
            self.request = random.randint(0, 0b1111111)
            return self.request

    def generate_write_data(self):
        if(self.permission):
            self.write_data = random.randint(0, 0xffffffff)
            return self.write_data

    def process_request(self):
        self.permission = 0 
        request_address = self.request & (0b0111111)
        print(f"this is the requested address bin({request_address:06b})")
        request_control = self.request >> 6
        print(request_control)

        if request_control:
            print(f"this is the Write Request and the data to be written is \n hex {self.write_data:08x}")
        else:
            print(" this was the read request") 
        self.permission = 1 

    def cache_to_core(self):
        if self.return_read_data :
            print(f"Core has recieved the data and the data is {self.return_read_data}")
        elif(self.return_write_validation):
            print("we have successfully written the data to the Ram")



c1 = Core(0)

c1.generate_request()
c1.generate_write_data()
c1.process_request()

            

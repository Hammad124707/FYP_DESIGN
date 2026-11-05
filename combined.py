import random

Ram = {
    0b000000: 0x0E1F1E21,
    0b000001: 0xA65CEFE5,
    0b000010: 0xA6D46916,
    0b000011: 0xB42221B1,
    0b000100: 0x154D6FCD,
    0b000101: 0xAB013F3A,
    0b000110: 0xBAD2685A,
    0b000111: 0xF9BCC126,
    0b001000: 0xC4E326B6,
    0b001001: 0x0A9162B0,
    0b001010: 0x2EFCAD5A,
    0b001011: 0x0FE3D4D9,
    0b001100: 0x5051D0A1,
    0b001101: 0x95AE040D,
    0b001110: 0xB7605052,
    0b001111: 0x810D7FB1,
    0b010000: 0x9A034270,
    0b010001: 0xE9AEA512,
    0b010010: 0xC87692CC,
    0b010011: 0x3806F3BE,
    0b010100: 0x176DF5A2,
    0b010101: 0x163928C4,
    0b010110: 0x82A88B37,
    0b010111: 0x500A2FDA,
    0b011000: 0x856B87E7,
    0b011001: 0x1ECD0DD0,
    0b011010: 0x550DF371,
    0b011011: 0x94E06FE8,
    0b011100: 0x27001F54,
    0b011101: 0xE33B6D74,
    0b011110: 0xB7B715C6,
    0b011111: 0x13975FD6,
    0b100000: 0xDBC924B5,
    0b100001: 0xF5339E9E,
    0b100010: 0xBAE62EE8,
    0b100011: 0xC01A58F8,
    0b100100: 0xD11C1A5F,
    0b100101: 0xC9845D3A,
    0b100110: 0x274EE0C0,
    0b100111: 0x6B4E2286,
    0b101000: 0x95C70D63,
    0b101001: 0xA402FFD0,
    0b101010: 0xD79C4659,
    0b101011: 0x1AC36937,
    0b101100: 0x0E595334,
    0b101101: 0x7F79B638,
    0b101110: 0x5BFA2B97,
    0b101111: 0xEA25E1BF,
    0b110000: 0x224D7563,
    0b110001: 0x71A08AAB,
    0b110010: 0xECD8A789,
    0b110011: 0x5AEB2F9F,
    0b110100: 0x56531953,
    0b110101: 0x80F829BD,
    0b110110: 0xDEDE01DF,
    0b110111: 0x5FBCC6E1,
    0b111000: 0xBB74EB58,
    0b111001: 0xDB791A69,
    0b111010: 0xBA031A92,
    0b111011: 0x9D14AFD5,
    0b111100: 0xB9945AF6,
    0b111101: 0xEFB3DDE5,
    0b111110: 0x73B28E45,
    0b111111: 0xCB88855A,
}

Read_Request = random.randint(0,0b1111111)
Write_Data = random.randint(0,0xffffffff)

Read_Request_Address =  Read_Request & (0b0111111)
print(bin(Read_Request_Address))
Read_Request_Control = Read_Request >> 6 
print(Read_Request_Control)
Read_Data = 0

if(Read_Request_Control) :
    print(f"this is the Write Request and the data to be written is \n {hex(Write_Data)}")
else :
    print(" this was the read request")
    Read_Data = Ram[Read_Request_Address]



print(f"the R_DATA is 0x{Read_Data:08X}")









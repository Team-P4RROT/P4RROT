import socket
import struct

server_addr = ('192.168.11.1',5555)
s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

print('A simple accumulator...')

while True:
    guess = int(input('next value to add (uint32_t)> '))

    s.sendto(struct.Struct('!I').pack(guess),server_addr)
    
    r,_ = s.recvfrom(256)
    r = struct.Struct('!I').unpack(r)[0]
    
    print('Result:',r)
    print()
